from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import City, Service

router = APIRouter(prefix='/cities')

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@router.get('/')
def cities(db: Session = Depends(get_db)):
	return db.query(City).all()

@router.get('/{city_id}/info')
def get_city_info(city_id: int, db: Session = Depends(get_db)):
	city = db.query(City).filter(City.id == city_id).first()
	services = db.query(Service).filter(Service.city_id == city_id).all()
	return {'city': city, 'services': services}
