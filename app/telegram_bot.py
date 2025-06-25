import logging

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

import json
from app.database import SessionLocal
from app.models import Master, RepairRequest, City
import requests
from dotenv import load_dotenv
import os
from sqlalchemy import event
from datetime import datetime
from fastapi import FastAPI, Request

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

app = FastAPI()

def notify_city_masters(city_id, requests_data):
    db = SessionLocal()
    masters = db.query(Master).filter(Master.city_id == city_id).all()
    logging.info(f"[DEBUG] Найдено мастеров: {len(masters)}")

    # Формируем текст с номером заявки
    text = (
        f'🛠 Заявка: {requests_data.request_number}'
        f'\n📱 Телефон: {requests_data.phone}'
        f'\n🗒 ️Модель / Неисправность: {requests_data.description}'
    )

    for master in masters:
        chat_id = master.telegram_id

        # Кнопки только если заявка ещё не в работе
        if requests_data.status in ["В работе", "Завершено"]:
            reply_markup = None
        else:
            reply_markup = {
                "inline_keyboard": [
                    [
                        {"text": "✅ Принять", "callback_data": f"start_{requests_data.id}"},
                        {"text": "✔️ Завершить", "callback_data": f"done_{requests_data.id}"}
                    ]
                ]
            }

        # Отправляем сообщение с заявкой
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "reply_markup": reply_markup
            }
        )
        logging.info(f"Response for {chat_id}: {response.status_code} {response.text}")

    db.close()



def handle_callback(callback):
    chat_id = callback["message"]["chat"]["id"]
    message_id = callback["message"]["message_id"]
    data = callback["data"]

    db = SessionLocal()

    if data.startswith("start_"):
        req_id = int(data.split("_")[1])
        req = db.query(RepairRequest).get(req_id)
        if req:
            logging.info(f"Текущий статус заявки {req_id}: {req.status}")
            if req.status and req.status != "Новая заявка":
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": "❗ Заявка уже в работе или завершена."}
                )
            else:
                req.status = "В работе"
                req.accepted_by = str(chat_id)
                db.commit()
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": "✅ Заявка принята в работу."}
                )
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "🛠 Вы можете завершить заявку, когда работа будет выполнена.",
                        "reply_markup": {
                            "inline_keyboard": [
                                [{"text": "✔️ Завершить", "callback_data": f"done_{req.id}"}]
                            ]
                        }
                    }
                )
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",
                    json={"chat_id": chat_id, "message_id": message_id, "reply_markup": {"inline_keyboard": []}}
                )


    # elif data.startswith("done_"):
    #     req_id = int(data.split("_")[1])
    #     req = db.query(RepairRequest).get(req_id)
    #     if req:
    #         req.status = "Завершено"
    #         db.commit()
    #         requests.post(
    #             f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",
    #             json={"chat_id": chat_id, "message_id": message_id, "reply_markup": {"inline_keyboard": []}}
    #         )
    #         requests.post(
    #             f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    #             json={"chat_id": chat_id, "text": "✅ Заявка завершена."}
    #         )
    # db.close()
    elif data.startswith("done_"):
        req_id = int(data.split("_")[1])
        req = db.query(RepairRequest).get(req_id)
        if req:
            if str(chat_id) != str(req.accepted_by):
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": "⛔ Завершить заявку может только тот, кто её принял."}
                )
            elif req.status == "Завершено":
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": "ℹ️ Заявка уже завершена."}
                )
            else:
                req.status = "Завершено"
                db.commit()
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",
                    json={"chat_id": chat_id, "message_id": message_id, "reply_markup": {"inline_keyboard": []}}
                )
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": "✅ Заявка завершена."}
                )

def start_polling():
    logging.info("Starting polling...")
    offset = None
    while True:
        try:
            params = {"timeout": 25}
            if offset is not None:
                params["offset"] = offset
            resp = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
                params=params,
                timeout=30
            )
            result = resp.json()
            if not result.get("ok"):
                logging.error(f"Polling error: {result}")
                continue
            updates = result.get("result", [])
            for update in updates:
                logging.info("[DEBUG] Incoming update: %s", update)
                if "callback_query" in update:
                    handle_callback(update["callback_query"])
                offset = update["update_id"] + 1
        except Exception as e:
            logging.exception(f"Polling exception: {e}")

@event.listens_for(RepairRequest, "before_insert")
def generate_request_data(mapper, connect, target):
    db = SessionLocal()
    city = db.query(City).filter_by(id=target.city_id).first()
    city_code = city.code if city else "XXX"
    count = db.query(RepairRequest).count()
    target.request_number = f"{city_code}-{count + 1:04d}"
    target.accepted_at = datetime.utcnow()
    db.close()


if __name__ == "__main__":
    start_polling()