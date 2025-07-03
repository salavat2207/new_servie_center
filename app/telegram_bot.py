import logging
import os
from dotenv import load_dotenv
import json
import httpx
from app.database import SessionLocal
from app.models import Master, RepairRequest, City
import requests
from dotenv import load_dotenv
import os
from sqlalchemy import event
from datetime import datetime
from fastapi import FastAPI, Request

load_dotenv()

logging.basicConfig(
	filename="bot.log",
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] %(message)s"
)

BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = FastAPI()


async def send_telegram_message_async(message: str):
	url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
	payload = {
		"chat_id": TELEGRAM_CHAT_ID,
		"text": message,
		"parse_mode": "HTML"
	}
	try:
		async with httpx.AsyncClient() as client:
			response = await client.post(url, json=payload)
			response.raise_for_status()  # чтобы отлавливать ошибки Telegram API
	except httpx.HTTPError as e:
		print("Ошибка отправки в Telegram:", e)


def notify_city_masters(city_id, requests_data):
	db = SessionLocal()
	masters = db.query(Master).filter(Master.city_id == city_id).all()

	# Формируем текст с номером заявки
	text = (
		f'🛠 Заявка: {requests_data.request_number}'
		f'\n📱 Телефон: {requests_data.phone}'
		f'\n🗒 ️Модель / Неисправность: {requests_data.description}'
	)

	for master in masters:
		chat_id = master.telegram_id

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

			if req.status.strip().lower() != "новая заявка":
				requests.post(
					f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
					json={
						"chat_id": chat_id,
						"text": f"❗ Заявка {req.request_number} уже в работе или завершена."
					}
				)
			else:
				req.status = "В работе"
				req.accepted_by = str(chat_id)
				db.commit()

				# Сообщение о принятии в работу
				work_msg = requests.post(
					f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
					json={
						"chat_id": chat_id,
						"text": f"✅ Заявка {req.request_number} принята в работу."
					}
				)
				work_message_id = work_msg.json().get("result", {}).get("message_id")

				requests.post(
					f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
					json={
						"chat_id": chat_id,
						"text": f"🛠 Вы можете завершить заявку {req.request_number}, когда работа будет выполнена.",
						"reply_markup": {
							"inline_keyboard": [
								[{"text": "✔️ Завершить", "callback_data": f"done_{req.id}_{work_message_id}"}]
							]
						}
					}
				)

				requests.post(
					f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageReplyMarkup",
					json={
						"chat_id": chat_id,
						"message_id": message_id,
						"reply_markup": {"inline_keyboard": []}
					}
				)

	elif data.startswith("done_"):
		parts = data.split("_")
		req_id = int(parts[1])
		work_message_id = int(parts[2]) if len(parts) > 2 else None
		req = db.query(RepairRequest).get(req_id)

		if req:
			if str(chat_id) != str(req.accepted_by):
				requests.post(
					f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
					json={
						"chat_id": chat_id,
						"text": f"⛔ Заявку {req.request_number} может завершить только тот, кто её принял."
					}
				)
			elif req.status == "Завершено":
				requests.post(
					f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
					json={
						"chat_id": chat_id,
						"text": f"ℹ️ Заявка {req.request_number} уже завершена."
					}
				)
			else:
				req.status = "Завершено"
				db.commit()

				requests.post(
					f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
					json={
						"chat_id": chat_id,
						"message_id": message_id
					}
				)

				if work_message_id:
					requests.post(
						f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
						json={
							"chat_id": chat_id,
							"message_id": work_message_id
						}
					)

				requests.post(
					f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
					json={
						"chat_id": chat_id,
						"text": f"✅ Заявка {req.request_number} завершена."
					}
				)

	db.close()


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
