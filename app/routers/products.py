from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from app import crud, schemas, telegram_bot, models
from typing import List
from app.models import Application, City, Master, RepairRequest, Product
from app.schemas import ApplicationCreate, ApplicationOut, ProductRead
from app.telegram_bot import notify_city_masters


router = APIRouter()

# def get_db():
# 	db = SessionLocal()
# 	try:
# 		yield db
# 	finally:
# 		db.close()



# @router.post('/products')
# def get_product(product: schemas.ProductsCreate, db: Session = Depends(get_db)):
# 	db_product = models.Produts(**product.dict())
# 	db.add(db_product)
# 	db.commit()
# 	db.refresh(db_product)
# 	return db_product



@router.get("/products", response_model=List[ProductRead])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products