from sqlalchemy.orm import Session
from app import models, schemas
from app.models import RepairRequest, RepairService
from app.schemas import RepairRequestCreate, RepairRequestTelegram


# def create_request(db: Session, request: schemas.RepairRequestCreate):
# 	new_request = models.RepairRequest(**request.dict())
# 	db.add(new_request)
# 	db.commit()
# 	db.refresh(new_request)
# 	return new_request



def create_request(db: Session, request_data: schemas.RepairRequestCreate):
    db_request = RepairRequest(**request_data.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(**admin.dict())
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


# def create_master(db: Session, master: schemas.MasterCreate):
#     db_master = models.Master(
#         name=master.name,
#         phone=master.phone,
#         telegram_id=master.telegram_id,
#         city_id=master.city_id
#     )
#     db.add(db_master)
#     db.commit()
#     db.refresh(db_master)
#     return db_master
#
#
# def get_masters_by_city(db: Session, city_id: int):
#     return db.query(models.Master).filter(models.Master.city_id == city_id).all()

def create_master(db: Session, master: schemas.MasterCreate):
    db_master = models.Master(**master.dict())
    db.add(db_master)
    db.commit()
    db.refresh(db_master)
    return db_master

def get_masters_by_city(db: Session, city_id: int):
    return db.query(models.Master).filter(models.Master.city_id == city_id).all()



