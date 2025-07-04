# import threading
# from uuid import uuid4
#
# from aiogram.client import bot
# from aiogram.client.session import aiohttp
# from aiohttp import payload
# from fastapi import APIRouter, Depends, HTTPException
# from starlette.responses import JSONResponse
#
# from app.database import SessionLocal
# from sqlalchemy.orm import Session, joinedload, session
# from app import crud, schemas, telegram_bot, models
# from typing import List
# from app.models import Application, City, Master, RepairRequest, Product, RepairService, Feedback
# from app.schemas import ApplicationCreate, ApplicationOut, RepairRequestBase, RepairRequestTelegram, FeedbackRead
# from app.telegram_bot import notify_city_masters, send_telegram_message_async
# from fastapi import Request
#
# import httpx
# import os
# import asyncio
#
# router = APIRouter()
#
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
#
# city_cache = {}
#
#
# def get_db():
# 	db = SessionLocal()
# 	try:
# 		yield db
# 	finally:
# 		db.close()
#
#
#
#
#
# async def send_telegram_message_async(message: str):
# 	url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
# 	payload = {
# 		"chat_id": TELEGRAM_CHAT_ID,
# 		"text": message,
# 		"parse_mode": "HTML"
# 	}
# 	try:
# 		async with httpx.AsyncClient() as client:
# 			await client.post(url, json=payload)
# 	except httpx.RequestError as e:
# 		print("Ошибка отправки в Telegram:", e)
#
#
#
# """
# Итоговый рабочий вариант
# """
#
# # @router.post('/feedback')
# # async def submit_request(request: schemas.RepairRequestCreate, db: Session = Depends(get_db)):
# # 	new_request = crud.create_request(db, request)
# # 	threading.Thread(target=notify_city_masters, args=(new_request.city_id, new_request)).start()
# # 	return {'Ваша заявка принята, ожидайте звонка от мастера'}
#
# def _notify_in_thread(city_id, req):
#     # здесь мы внутри обычной функции, поэтому запускаем event loop
#     asyncio.run(notify_city_masters(city_id, req))
#
# @router.post('/feedback')
# async def submit_request(request: schemas.RepairRequestCreate, db: Session = Depends(get_db)):
#     new_request = crud.create_request(db, request)
#     threading.Thread(target=_notify_in_thread, args=(new_request.city_id, new_request)).start()
#     return {'detail': 'Ваша заявка принята, ожидайте звонка от мастера'}
#
#
#
#
#
#
#
# @router.post("/")
# def send_repair_request(request: RepairRequestTelegram, db: Session = Depends(get_db)):
# 	if request.city_id not in city_cache:
# 		city = db.query(City).filter(City.id == request.city_id).first()
# 		if city:
# 			city_cache[request.city_id] = city
# 		else:
# 			raise HTTPException(status_code=404, detail="Город не найден")
#
# 	product = db.query(Product).filter(Product.id == request.product_id).first()
# 	service = (
# 		db.query(RepairService)
# 		.filter(
# 			RepairService.product_id == request.product_id,
# 			RepairService.id == request.service_id
# 		)
# 		.first()
# 	)
# 	if not product or not service:
# 		raise HTTPException(status_code=404, detail="Продукт или услуга не найдены")
#
# 	new_application = Application(
# 		phone=request.phone,
# 		description=request.description,
# 		city_id=request.city_id,
# 		name=request.name,
# 		code=str(uuid4())[:8],
# 		status="Новая заявка"
# 	)
# 	db.add(new_application)
# 	db.commit()
# 	db.refresh(new_application)
#
# 	message = (
# 		f"🛠 <b>Заявка на ремонт</b>\n"
# 		f"📱 <b>Модель:</b> {product.name}\n"
# 		f"🔧 <b>Услуга:</b> {service.name}\n"
# 		f"📝 <b>Описание:</b> {service.description}\n"
# 		f"💰 <b>Стоимость:</b> {int(service.price)} ₽\n"
# 		f"🙍‍♂️ <b>Имя / Неисправность:</b> {request.name}\n"
# 		f"📞 <b>Телефон:</b> {request.phone}"
# 	)
#
# 	asyncio.create_task(send_telegram_message_async(message))
#
# 	return {"message": "Заявка успешно отправлена"}
#
#
#
#
#
#
#
# @router.get("/")
# def get_requests(db: Session = Depends(get_db)):
# 	return db.query(RepairRequest).all()







import threading
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse
import httpx
import os
import asyncio

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas
from app.models import Application, City, RepairRequest, Product, RepairService
from app.schemas import RepairRequestTelegram
from app.telegram_bot import notify_city_masters, send_telegram_message_async

router = APIRouter()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

city_cache = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _notify_in_thread(city_id, req):
    # просто синхронно уведомляем мастеров
    notify_city_masters(city_id, req)

@router.post('/feedback')
async def submit_request(request: schemas.RepairRequestCreate,
                         db: Session = Depends(get_db)):
    new_request = crud.create_request(db, request)
    threading.Thread(
        target=_notify_in_thread,
        args=(new_request.city_id, new_request),
        daemon=True,
    ).start()
    return {'detail': 'Ваша заявка принята, ожидайте звонка от мастера'}

@router.post('/requests')
def send_repair_request(request: RepairRequestTelegram, db: Session = Depends(get_db)):
    if request.city_id not in city_cache:
        city = db.query(City).get(request.city_id)
        if city:
            city_cache[request.city_id] = city
        else:
            raise HTTPException(status_code=404, detail="Город не найден")

    product = db.query(Product).get(request.product_id)
    service = db.query(RepairService).filter(
        RepairService.product_id == request.product_id,
        RepairService.id == request.service_id
    ).first()
    if not product or not service:
        raise HTTPException(status_code=404, detail="Продукт или услуга не найдены")

    # Создаём заявку
    app = Application(
        phone=request.phone,
        description=request.description,
        city_id=request.city_id,
        name=request.name,
        code=str(uuid4())[:8],
        status="Новая заявка"
    )
    db.add(app)
    db.commit()
    db.refresh(app)

    message = (
        f"🛠 <b>Заявка на ремонт</b>\n"
        f"📱 <b>Модель:</b> {product.name}\n"
        f"🔧 <b>Услуга:</b> {service.title}\n"
        f"📝 <b>Описание услуги:</b> {service.description}\n"
        f"🙍‍♂️ <b>Имя / Неисправность:</b> {app.name}\n"
        f"📞 <b>Телефон:</b> {app.phone}"
    )
    asyncio.create_task(send_telegram_message_async(message))
    return {"message": "Заявка успешно отправлена"}

@router.get('/requests')
def list_requests(db: Session = Depends(get_db)):
    return db.query(RepairRequest).all()