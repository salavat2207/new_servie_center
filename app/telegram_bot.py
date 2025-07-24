import logging
import os
from dotenv import load_dotenv
import httpx
from app.database import SessionLocal
from app.models import Master, RepairRequest, City
from sqlalchemy import event
from datetime import datetime

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(
	filename="bot.log",
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("telegram")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

if not logger.handlers:
	logger.addHandler(console_handler)


async def send_telegram_message_async(chat_id: str, message: str):
	url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
	payload = {
		"chat_id": chat_id,
		"text": message,
		"parse_mode": "HTML"
	}
	try:
		async with httpx.AsyncClient() as client:
			response = await client.post(url, json=payload)
			response.raise_for_status()
			logger.info(f"📤 Message sent to {chat_id}")
	except httpx.HTTPError as e:
		logger.error(f"❌ Failed to send message to {chat_id}: {e}")


def notify_city_masters(city_id: int, request_data: RepairRequest):
	db = SessionLocal()
	masters = db.query(Master).filter(Master.city_id == city_id).all()

	text = (
		f'🛠 Заявка: {request_data.request_number}\n'
		f'📱 Телефон: {request_data.phone}\n'
		f'📄 Имя/Неисправность: {request_data.description}\n'
	)

	for master in masters:
		chat_id = master.telegram_id
		if chat_id:
			try:
				httpx.post(
					f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
					json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
				)
				# logger.info(f"✅ Заявка отправлена мастеру {chat_id}")
			except Exception as e:
				logger.error(f"❌ Ошибка отправки мастеру {chat_id}: {e}")
	db.close()


@event.listens_for(RepairRequest, "before_insert")
def generate_request_data(mapper, connect, target):
	db = SessionLocal()
	city = db.query(City).filter_by(id=target.city_id).first()
	city_code = city.code if city else "XXX"
	count = db.query(RepairRequest).count()
	target.request_number = f"{city_code}-{count + 1:04d}"
	target.accepted_at = datetime.utcnow()
	db.close()


logger = logging.getLogger("telegram")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
if not logger.handlers:
	logger.addHandler(console_handler)


class TelegramBotService:
	BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

	@classmethod
	async def send_message(cls, chat_id: str, text: str, parse_mode: str = "HTML") -> None:
		payload = {
			"chat_id": chat_id,
			"text": text,
			"parse_mode": parse_mode
		}

		try:
			async with httpx.AsyncClient() as client:
				resp = await client.post(cls.BASE_URL, json=payload)
				resp.raise_for_status()
				logger.info(f"📤 Message sent to {chat_id}")
		except httpx.HTTPError as e:
			logger.error(f"❌ Failed to send message to {chat_id}: {e}")
