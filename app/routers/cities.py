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

# city_id = {'1': 'Челябинск',
# 		'2': 'Магнитогорск',
# 		'3':'Екатеринбург'}


# @router.get('/info/{city_id}')
# def get_city_info(city_id: int, db: Session = Depends(get_db)):
# 	city = db.query(City).filter(City.id == city_id).first()
# 	services = db.query(Service).filter(Service.city_id == city_id).all()
# 	return {'city': city, 'services': services}

@router.get('/{city_id}')
def get_city_info(city_id: int):
	if city_id == 1:
		return {'city': 'Челябинск'}
	elif city_id == 2:
		return {'city': 'Магнитогорск'}
	elif city_id == 3:
		return {'city': 'Екатеринбург'}
	else:
		return {'error': 'Город не найден'}

