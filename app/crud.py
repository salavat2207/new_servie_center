from sqlalchemy.orm import Session
from app import models, schemas
from app.models import RepairRequest, RepairService, City
from app.schemas import RepairRequestCreate, RepairRequestTelegram


def create_request(db: Session, request_data: schemas.RepairRequestCreate):
    db_request = RepairRequest(**request_data.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    db_request.city = db.query(City).filter(City.id == db_request.city_id).first()
    return db_request






def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(**admin.model_dump())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def get_all_requests(db: Session):
    return db.query(models.RepairRequest).all()

"""
Общая форма заявок с сайта
"""
def create_repair_request(db: Session, request: RepairRequestCreate):
    db_request = RepairRequest(
        name=request.name,
        phone=request.phone,
        description=request.description,
        city_id=request.city_id
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request




"""
Форма заявок с карточки товара
"""
def send_repair_request(db: Session, request: RepairRequestTelegram):
    db_request = RepairService(
        name=request.name,
        phone=request.phone,
        description=request.description,
        city_id=request.city_id,
        service_id=request.service_id,
        duration=request.duration,
        price=request.price,
        category_id=request.category_id,
        product_id=request.product_id
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request




def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city



def create_master(db: Session, master: schemas.MasterCreate):
    db_master = models.Master(**master.model_dump())
    db.add(db_master)
    db.commit()
    db.refresh(db_master)
    return db_master

def get_masters_by_city(db: Session, city_id: int):
    return db.query(models.Master).filter(models.Master.city_id == city_id).all()



