from sqlalchemy.orm import Session
from app import models, schemas



# def create_request(db: Session, request: schemas.RepairRequestCreate):
# 	new_request = models.RepairRequest(**request.dict())
# 	db.add(new_request)
# 	db.commit()
# 	db.refresh(new_request)
# 	return new_request




from app.models import RepairRequest

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