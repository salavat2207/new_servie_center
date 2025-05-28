from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app import crud, schemas, telegram_bot, models
from typing import List
from app.models import Application, City, Master, RepairRequest
from app.schemas import ApplicationCreate, ApplicationOut, RepairRequestBase
from app.telegram_bot import notify_city_masters

router = APIRouter(prefix='/requests')

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()



# @router.post('/Обратная связь с сайта')
# def submit_request(request: schemas.RepairRequestCreate, db: Session = Depends(get_db)):
# 	new_request = crud.create_request(db, request)
# 	telegram_bot.notify_city_masters(new_request.city_id, new_request)
# 	return {'status': 'Ваша заявка принята, ожидайте звонка от мастера'}
#
# @router.post("/Форма заявки")
# def create_request(city_id: int, phone: str, description: str, db: Session = Depends(get_db)):
#     city = db.query(City).filter(City.id == city_id).first()
#     if not city:
#         raise HTTPException(status_code=404, detail="Город не найден")
#
#     total_requests = db.query(RepairRequest).count() + 1
#
#     city_codes = {
#         1: 'CHE',
#         2: 'MGN',
#         3: 'EKB'
#     }
#     city_code = city_codes.get(city_id, 'UNK')
#     request_number = f"{city_code}-{total_requests}"
#
#     new_request = RepairRequest(city_id=city_id, description=description, request_number=request_number)
#     db.add(new_request)
#     db.commit()
#     db.refresh(new_request)
#
#     return {
#         "id": new_request.id,
#         "request_number": new_request.request_number,
#         "description": new_request.description,
#         "city": city.name
#     }







#
# @router.post("/form")
# def create_request(city_id: int, phone: str, description: str, db: Session = Depends(get_db)):
#     # Проверяем существование города
#     city = db.query(City).filter(City.id == city_id).first()
#     if not city:
#         raise HTTPException(status_code=404, detail="Город не найден")
#
#     last_request = (
#         db.query(RepairRequest)
#         .filter(RepairRequest.request_number.like(f"{city.code}-%"))
#         .order_by(RepairRequest.id.desc())
#         .first()
#     )
#
#     if last_request and last_request.request_number:
#         last_number = int(last_request.request_number.split('-')[1])
#     else:
#         last_number = 0
#
#     new_number = last_number + 1
#     request_number = f"{city.code}-{new_number:05d}"  # 5 цифр с ведущими нулями
#
#     # Создаём заявку
#     new_request = RepairRequest(
#         city_id=city.id,
#         phone=phone,
#         description=description,
#         request_number=request_number
#     )
#     db.add(new_request)
#     db.commit()
#     db.refresh(new_request)
#
#     return {
#         "id": new_request.id,
#         "request_number": new_request.request_number,
#         "description": new_request.description,
#         "phone": new_request.phone,
#         "city": city.name
#     }
#




#
# @router.post("/requests/ФОРМА")
#
# def create_request(city_id: int, phone: str, description: str, db: Session = Depends(get_db)):
# 	city = db.query(City).filter(City.id == city_id).first()
# 	if not city:
# 		raise HTTPException(status_code=404, detail="Город не найден")
#
#
# 	city_requests_count = db.query(RepairRequest).filter(
# 		RepairRequest.request_number.like(f"{city.code}-%")
# 	).count() + 1
#
# 	request_number = f"{city.code}-{city_requests_count}"
#
# 	new_request = RepairRequest(
# 		city_id=city_id,
# 		phone=phone,
# 		description=description,
# 		request_number=request_number
# 	)
# 	db.add(new_request)
# 	db.commit()
# 	db.refresh(new_request)
#
# 	return {
# 		"id": new_request.id,
# 		"request_number": new_request.request_number,
# 		"description": new_request.description,
# 		"city": city.name
# 	}
#






#
# """
# Синхронизация id и номера заявок (id=1, CHE-1, id=2, MGN-2, id=3, EKB-3)
# """
# @router.post("/requests/ФОРМА")
# def create_request(city_id: int, phone: str, description: str, db: Session = Depends(get_db)):
#
#     city = db.query(City).filter(City.id == city_id).first()
#     if not city:
#         raise HTTPException(status_code=404, detail="Город не найден")
#
#     new_request = RepairRequest(
#         city_id=city_id,
#         phone=phone,
#         description=description
#     )
#     db.add(new_request)
#     db.commit()
#     db.refresh(new_request)
#
#     new_request.request_number = f"{city.code}-{new_request.id}"
#     db.commit()
#
#     return {
#         "id": new_request.id,
#         "request_number": new_request.request_number,
#         "description": new_request.description,
#         "city": city.name
#     }
#







# @router.post('/Ручное добавление заявки мастером')
# def create_request_manually(request: schemas.RepairRequestCreate, db: Session = Depends(get_db)):
# 	new_request = crud.create_repair_request(db, request)
# 	return {"status": "Заявка добавлена вручную", "data": new_request}


# """
# Старая версия
# """
# @router.get("/all{Получение списка заявок с бд}", response_model=List[schemas.RepairRequestOut])
# def get_all_requests(db: Session = Depends(get_db)):
# 	return crud.get_all_requests(db)


"""
Новая версия / Получение списка заявок с бд
"""
# @router.get("/requests/all", response_model=List[RepairRequestBase])
# def get_requests_all(db: Session = Depends(get_db)):
# 	# return crud.get_all_requests(db)
# 	# return db.query(RepairRequest).all()
# 	requests = db.query(RepairRequest).all()
# 	return requests

#
#
# @router.post("/заявка", response_model=schemas.ApplicationOut)
# def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
#
# 	db_app = models.Application(**application.dict(), code="")
# 	db.add(db_app)
# 	db.commit()
# 	db.refresh(db_app)
#
# 	# 2. Получаем код города
# 	city = db.query(models.City).filter(models.City.id == db_app.city_id).first()
# 	if not city:
# 		raise HTTPException(status_code=404, detail="City not found")
#
# 	db_app.code = f"{city.code}{db_app.id}"
# 	db.commit()
# 	db.refresh(db_app)
#
# 	return db_app



#
# С ОШИБКОЙ
#
# @router.post("/заявка", response_model=ApplicationOut)
# def create_application(
# 				app: ApplicationCreate, db: Session = Depends(get_db)):
# 	city = db.query(City).filter(City.id == app.city_id).first()
# 	if not city:
# 		raise HTTPException(status_code=404, detail="City not found")
#
# 	application = Application(
# 		phone=app.phone,
# 		description=app.description,
# 		city_id=app.city_id
# 	)
#
# 	db.add(application)
# 	db.flush()
#
# 	application.code = f"{city.code}-{application.id}"
# 	db.commit()
# 	db.refresh(application)
#
# 	masters = db.query(Master).filter(Master.city_id == city.id).all()
# 	if masters:
# 		message = (
# 			f'Новая заявка: {application.code}\n'
# 			f'Телефон: {application.phone}\n'
# 			f'Город: {city.name}\n'
# 			f'Описание: {application.description}'
# 		)
# 		for master in masters:
# 			if master.telegram_id:
# 				print(f"[DEBUG] Отправка уведомлений. Город ID: {application.city_id}, Телеграм ID мастера: {master.telegram_id}")
# 				# send_telegram_message(master.telegram_id, message)
# 				notify_city_masters(application.city_id, application)
#
# 	return application


"""
ИТОГОВАЯ Форма обратной связи с сохранением в бд
"""
@router.post('/Заявка на консультацию:')
def submit_request(
		request: schemas.RepairRequestCreate, db: Session = Depends(get_db)
):
	new_request = crud.create_request(db, request)
	telegram_bot.notify_city_masters(new_request.city_id, new_request)
	return {'Ваша заявка принята, ожидайте звонка от мастера'}

