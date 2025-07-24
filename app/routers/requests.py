import threading
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

import os


from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import crud, schemas
from app.models import Application, City, RepairRequest, Product, RepairService, User, Master
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





@router.post('/')
async def send_repair_request(request: RepairRequestTelegram, db: Session = Depends(get_db)):
    if request.city_id not in city_cache:
        city = db.query(City).get(request.city_id)
        if city:
            city_cache[request.city_id] = city
        else:
            raise HTTPException(status_code=404, detail="Город не найден")

    product = db.query(Product).filter(Product.id == request.product_id).first()
    service = db.query(RepairService).filter(
        RepairService.product_id == request.product_id,
        RepairService.id == request.service_id
    ).first()
    if not product or not service:
        raise HTTPException(status_code=404, detail="Продукт или услуга не найдены")


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
        f"🙍‍♂️ <b>Имя:</b> {app.name}\n"
        f"📞 <b>Телефон:</b> {app.phone}"
    )


    masters = db.query(Master).filter_by(city_id=request.city_id).all()
    for master in masters:
        if master.telegram_id:
            await TelegramBotService.send_message(chat_id=master.telegram_id, text=message)

    return {"message": "Заявка успешно отправлена"}




