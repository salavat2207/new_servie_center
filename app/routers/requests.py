from fastapi import APIRouter, Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app import crud, schemas, telegram_bot

router = APIRouter(prefix='/requests')

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()



@router.post('/Обратная связь')
def submit_request(request: schemas.RepairRequestCreate, db: Session = Depends(get_db)):
	new_request = crud.create_request(db, request)
	telegram_bot.notify_city_masters(new_request.city_id, new_request)
	return {'status': 'Ваша заявка принята, ожидайте звонка от мастера'}



@router.post("/manual")
def create_request_manually(request: schemas.RepairRequestCreate, db: Session = Depends(get_db)):
	new_request = crud.create_repair_request(db, request)
	return {"status": "Заявка добавлена вручную", "data": new_request}