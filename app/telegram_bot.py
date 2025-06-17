from app.database import SessionLocal
from app.models import Master, RepairRequest
import requests
from dotenv import load_dotenv
import os

load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
#
# def notify_city_masters(city_id, request_data):
#     db = SessionLocal()
#     masters = db.query(Master).filter(Master.city_id == city_id).all()
#     text = f"Новая заявка:\nИмя: {request_data.name}\nТел: {request_data.phone}\nПроблема: {request_data.description}"
#
#     for master in masters:
#         requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={
#             # "chat_id": master.telegram_id,
#             "chat_id": CHAT_ID,
#             "text": text
#         })


def notify_city_masters(city_id, requests_data):
    print(f"[DEBUG] Отправка уведомлений по городу ID: {city_id}")
    print(f"[DEBUG] Заявка: {requests_data.phone}, {requests_data.description}")

    db = SessionLocal()
    masters = db.query(Master).filter(Master.city_id == city_id).all()
    print(f"[DEBUG] Найдено мастеров: {len(masters)}")

    text = (
        f'🛠 Заявка на консультацию:'
        # f'\nИмя: {requests_data.name}'
            f'\n📍 Город: {requests_data.city.name}'
            f'\n📱 Телефон: {requests_data.phone}'
            f'\n📱 Модель / Неисправность: {requests_data.description}')

    for master in masters:
        chat_id = master.telegram_id
        response = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": chat_id, "text": text}
        )
        print(f"Response for {chat_id}: {response.status_code} {response.text}")


#
# def notify_city_masters(city_id, requests_data):
#     print(f"[DEBUG] Отправка уведомлений по городу ID: {city_id}")
#     print(f"[DEBUG] Заявка: {requests_data.phone}, {requests_data.description}")
#
#     db = SessionLocal()
#     masters = db.query(Master).filter(Master.city_id == city_id).all()
#     print(f"[DEBUG] Найдено мастеров: {len(masters)}")
#
#     text = (
#         f'🔧 Новая заявка:\n'
#         f'📱 Телефон: {requests_data.phone}\n'
#         f'📝 Описание: {requests_data.description}'
#     )
#
#     for master in masters:
#         chat_id = master.telegram_id
#         response = requests.get(
#             f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
#             params={"chat_id": chat_id, "text": text}
#         )
#         print(f"Response for {chat_id}: {response.status_code} {response.text}")