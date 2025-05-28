from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import City, Service
from app.schemas import CityCreate

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



@router.get('/info/{city_id}')
def get_city_info(city_id: int, db: Session = Depends(get_db)):
	city = db.query(City).filter(City.id == city_id).first()
	services = db.query(Service).filter(Service.city_id == city_id).all()
	return {'city': city, 'services': services}




# @router.post('/создать город')
# def create_city(city: CityCreate, db: Session = Depends(get_db)):
# 	db_city = City(name=city.name, address=city.address, phone=city.phone)
# 	db.add(db_city)
# 	db.commit()
# 	db.refresh(db_city)
# 	return db_city


# @router.get('/{city_id}')
# def get_city_info(city_id: int):
# 	if city_id == 1:
# 		return {'city': 'Челябинск'}
# 	elif city_id == 2:
# 		return {'city': 'Магнитогорск'}
# 	elif city_id == 3:
# 		return {'city': 'Екатеринбург'}
# 	else:
# 		return {'error': 'Город не найден'}

