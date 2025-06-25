from fastapi import APIRouter, Depends, HTTPException
from app.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from app import crud, schemas, telegram_bot, models
from typing import List
from app.models import Application, City, Master, RepairRequest, Product, RepairService
from app.schemas import ApplicationCreate, ApplicationOut, ProductRead, ProductCreate, ProductPriceCreate, ProductPriceOut
# from app.telegram_bot import notify_city_masters
from app.telegram_bot import notify_city_masters

router = APIRouter(
    prefix="/products",
    tags=["products"])

# def get_db():
# 	db = SessionLocal()
# 	try:
# 		yield db
# 	finally:
# 		db.close()




# @router.get("/products", response_model=List[ProductRead])
# def get_all_products(db: Session = Depends(get_db)):
#     products = db.query(Product).all()
#     return products
#


"""
Добавление услуг
"""
@router.post("/add")
def add_product(product: ProductPriceCreate, db: Session = Depends(get_db)):
    existing_product = db.query(RepairService).filter(RepairService.id == product.id).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Товар с таким ID уже существует")

    new_product = RepairService(
        id=product.id,
        name=product.name,
        service_id=product.service_id,
        price=product.price,
        city_id=product.city_id,
        description=product.description,
        duration=product.duration,
        product_id=product.product_id,
        category_id=product.category_id
    )
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении: {str(e)}")

    return {"message": "Товар успешно добавлен", "product": {
        "id": new_product.id,
        "name": new_product.name,
        'service_id': new_product.service_id,
        "price": new_product.price,
        "city_id": new_product.city_id,
        "description": new_product.description,
        "duration": new_product.duration,
        'product_id': new_product.product_id,
        'category_id': new_product.category_id
    }}



@router.get("/", response_model=List[ProductPriceOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(RepairService).all()