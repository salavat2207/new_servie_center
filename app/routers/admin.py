from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.models import Product, ProductPrice
from app.routers.auth import get_current_user
from app.schemas import ProductCreate, ProductPriceCreate, ProductPriceSchema

#
# router = APIRouter(prefix="/admin", tags=["Admin"])
#
# @router.post("/add_admin")
# def add_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
#     return crud.create_admin(db, admin)
#
#
# @router.post("/categories/")
# def add_category(name: str, user=Depends(get_current_user)):
#     if not user["is_superadmin"]:
#         raise HTTPException(status_code=403, detail="Not authorized")
#
#
# @router.get("/applications/")
# def get_applications(user=Depends(get_current_user)):
#     # Для мастеров — только свои заявки
#     if user["is_superadmin"]:
#         return crud.get_all_requests(db)
#     else:
#         return crud.get_requests_by_master(db, user["id"])


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
	if db.query(Product).filter_by(id=product.id).first():
		raise HTTPException(status_code=400, detail="Product already exists")
	new_product = Product(**product.dict())
	db.add(new_product)
	db.commit()
	db.refresh(new_product)
	return new_product

# @router.post("/product-price")
# def set_product_price(price_data: ProductPriceCreate, db: Session = Depends(get_db)):
# 	existing = db.query(ProductPrice).filter_by(product_id=price_data.product_id, city_id=price_data.city).first()
# 	if existing:
# 		existing.price = price_data.price
# 	else:
# 		existing = ProductPrice(**price_data.dict())
# 		db.add(existing)
# 	db.commit()
# 	db.refresh(existing)
# 	return existing


@router.post("/product-price")
def set_product_price(data: ProductPriceSchema, db: Session = Depends(get_db)):
    existing = db.query(ProductPrice).filter_by(
        product_id=data.product_id,
        city_id=data.city_id
    ).first()

    if existing:
        # Обновляем цену
        existing.price = data.price
        db.commit()
        return {"message": "Цена обновлена"}
    else:
        # Создаём новую запись
        new_price = ProductPrice(
            product_id=data.product_id,
            city_id=data.city_id,
            price=data.price
        )
        db.add(new_price)
        db.commit()
        return {"message": "Новая цена добавлена"}