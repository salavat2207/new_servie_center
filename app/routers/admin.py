from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
import shutil
import os

from app import schemas, crud
from app.database import get_db
from app.models import Product, ProductPrice, User, Admin, RepairService, City
from app.routers.auth import get_current_user
from app.schemas import ProductCreate, ProductPriceCreate, ProductPriceSchema, AdminLoginSchema, ProductCreateSchema, \
    RepairServicePatch, ProductPriceOut
from app.auth import verify_password, create_access_token, get_current_admin, get_password_hash, get_current_admin_user
from app.database import SessionLocal, Base, engine
from app.models import User
from app.auth import get_password_hash
from app.schemas import ProductUpdate
from typing import Optional, List


UPLOAD_DIR = "static/uploads"
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

#
# @router.post("/admin/products")
# def create_product(
# 		product_data: ProductCreateSchema,
# 		db: Session = Depends(get_db),
# 		_: dict = Depends(get_current_admin_user),
# ):
# 	if db.query(Product).filter_by(id=product_data.id).first():
# 		raise HTTPException(status_code=400, detail="Product already exists")
#
# 	product = Product(
# 		id=product_data.id,
# 		name=product_data.name,
# 		category=product_data.category,
# 		title=product_data.title,
# 		link=product_data.link,
# 		category_id=product_data.category_id,
# 		description=product_data.description,
# 		image=product_data.image
# 	)
# 	db.add(product)
# 	db.commit()





"""
Добавление услуг
"""
@router.post("/add_service")
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

#


"""
Добавление пользователей
"""

@router.post("/admin/create")
def create_admin():
    # Создаём таблицы, если их ещё нет
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    username = input("Введите имя суперадмина: ").strip()
    password = input("Введите пароль суперадмина: ").strip()

    existing_user = db.query(User).filter_by(username=username).first()
    if existing_user:
        print("❌ Пользователь с таким именем уже существует.")
        return

    hashed_password = get_password_hash(password)
    admin = Admin(username=username, password=hashed_password, is_superadmin=True)
    db.add(admin)
    db.commit()
    print("✅ Суперадмин успешно создан.")


if __name__ == "__main__":
    create_admin()




"""
Авторизация
"""


@router.post("/admin/login")
def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter_by(username=form_data.username, is_superadmin=True).first()
    if not admin or not verify_password(form_data.password, admin.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = create_access_token({"sub": admin.username})
    return {"access_token": token, "token_type": "bearer"}




"""
Редактирование цены товара для города
"""


# @router.put("/admin/product-price", dependencies=[Depends(get_current_admin)])
# def update_price(product_id: str, city_id: int, price: int, db: Session = Depends(get_db)):
# 	price_entry = db.query(ProductPrice).filter_by(product_id=product_id, city_id=city_id).first()
# 	if not price_entry:
# 		raise HTTPException(status_code=404, detail="Цена не найдена")
# 	price_entry.price = price
# 	db.commit()
# 	return {"message": "Цена обновлена"}

 # обязательно импортировать



"""
Обновленное редактирование товара
"""
# @router.put("/admin/products/{product_id}", dependencies=[Depends(get_current_admin)])
# def update_product(product_id: str, update_data: ProductUpdate, db: Session = Depends(get_db)):
# 	product = db.query(Product).filter_by(id=product_id).first()
# 	if not product:
# 		raise HTTPException(status_code=404, detail="Продукт не найден")
#
#
# 	if update_data.name is not None:
# 		product.name = update_data.name
# 	if update_data.category is not None:
# 		product.category = update_data.category
# 	if update_data.title is not None:
# 		product.title = update_data.title
# 	if update_data.link is not None:
# 		product.link = update_data.link
# 	if update_data.category_id is not None:
# 		product.category_id = update_data.category_id
# 	if update_data.description is not None:
# 		product.description = update_data.description
# 	if update_data.image is not None:
# 		product.image = update_data.image
#
# 	db.commit()
# 	db.refresh(product)
#
# 	return {"message": "Товар обновлён", "product": {
# 		"id": product.id,
# 		"name": product.name,
# 		"category": product.category,
# 		"title": product.title,
# 		"link": product.link,
# 		"category_id": product.category_id,
# 		"description": product.description,
# 		"image": product.image,
# 	}}
#
#
# """
# РАБОЧИЙ ВАРИАНТ РЕДАКТИРОВАНИЯ УСЛУГИ
# """
# @router.put("/admin/repair-service/{service_id}", dependencies=[Depends(get_current_admin)])
# def update_repair_service(service_id: str, update_data: ProductPriceCreate, db: Session = Depends(get_db)):
#     service = db.query(RepairService).filter_by(service_id=service_id).first()
#     if not service:
#         raise HTTPException(status_code=404, detail="Услуга не найдена")
#
#     service.name = update_data.name
#     service.description = update_data.description
#     service.duration = update_data.duration
#     service.price = update_data.price
#     service.product_id = update_data.product_id
#     service.category_id = update_data.category_id
#     service.city_id = update_data.city_id
#
#     db.commit()
#     db.refresh(service)
#
#     return {
#         "message": "Услуга обновлена",
#         "service": {
#             "id": service.id,
#             "name": service.name,
#             "service_id": service.service_id,
#             "description": service.description,
#             "duration": service.duration,
#             "price": service.price,
#             "product_id": service.product_id,
#             "category_id": service.category_id,
#             "city_id": service.city_id
#         }
#     }

"""
Частичное обновление услуги (рабочий)
"""
@router.patch("/admin/repair-service/{service_id}", dependencies=[Depends(get_current_admin)])
def patch_repair_service(service_id: str, update_data: RepairServicePatch, db: Session = Depends(get_db)):
    service = db.query(RepairService).filter_by(service_id=service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)

    return {
        "message": "Услуга частично обновлена",
        "service": {
            "id": service.id,
            "name": service.name,
            "service_id": service.service_id,
            "description": service.description,
            "duration": service.duration,
            "price": service.price,
            "product_id": service.product_id,
            "category_id": service.category_id,
            "city_id": service.city_id
        }
    }





"""
Удаление товара
"""


# @router.delete("/admin/products/{product_id}", dependencies=[Depends(get_current_admin)])
# def delete_product(product_id: str, db: Session = Depends(get_db)):
#     product = db.query(RepairService).filter_by(id=product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Продукт не найден")
#
#     for price in product.prices:
#         db.delete(price)
#
#     db.delete(product)
#     db.commit()
#     return {"message": "Продукт удалён"}
@router.delete("/admin/repair-services/{product_id}", dependencies=[Depends(get_current_admin)])
def delete_repair_service_by_product(product_id: str, db: Session = Depends(get_db)):
    service = db.query(RepairService).filter_by(product_id=product_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Услуга с таким product_id не найдена")

    for price in service.prices:
        db.delete(price)

    db.delete(service)
    db.commit()
    return {"message": "Услуга и связанные с ней цены удалены"}


# @router.get("/products")
# def get_products(
#     city_id: Optional[int] = None,
#     db: Session = Depends(get_db),
#     _ = Depends(get_current_admin)
# ):
#     query = db.query(Product)
#     if city_id is not None:
#         query = query.join(ProductPrice).filter(ProductPrice.city_id == city_id)
#     return query.all()
@router.get("/", response_model=List[ProductPriceOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(RepairService).all()

# Загрузка изображений
@router.post("/admin/upload-image")
def upload_image(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"url": f"/{file_path}"}


# Получение цен по городам для товара
# @router.get("/admin/product-price/{product_id}", dependencies=[Depends(get_current_admin)])
# def get_prices_by_product(product_id: str, db: Session = Depends(get_db)):
#     prices = db.query(ProductPrice).filter_by(product_id=product_id).all()
#     return [{"city_id": p.city_id, "price": p.price} for p in prices]



# @router.get("/admin/product-price/{service_id}", dependencies=[Depends(get_current_admin)])
# def get_prices_by_service_id(service_id: str, db: Session = Depends(get_db)):
#     service = db.query(RepairService).filter_by(service_id=service_id).first()
#
#     if not service:
#         raise HTTPException(status_code=404, detail="Услуга не найдена")
#
#     print(f"[DEBUG] Услуга: {service.service_id} — {service.name}")
#
#     result = []
#
#     for price in service.prices:
#         print(f"[DEBUG] Цена: {price.price}, город: {price.city_code}")
#         city = db.query(City).filter(City.code == price.city_code).first()
#         result.append({
#             "city": city.name if city else price.city_code,
#             "price": price.price
#         })
#
#     return {
#         "service_id": service.service_id,
#         "service_name": service.name,
#         "prices": result
#     }
@router.get("/admin/product-price/{service_id}", dependencies=[Depends(get_current_admin)])
def get_prices_by_service_id(service_id: str, db: Session = Depends(get_db)):
    service = db.query(RepairService).filter_by(service_id=service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Услуга не найдена")

    cities = db.query(City).all()
    prices_by_city = {price.city_code: price.price for price in service.prices}

    result = []
    for city in cities:
        result.append({
            "city": city.name,
            "city_code": city.code,
            "price": prices_by_city.get(city.code)
        })

    return {
        "service_id": service.service_id,
        "service_name": service.name,
        'result': result
    }


#
# router.post("/admin/requests/{request_id}/status", dependencies=[Depends(get_current_admin)])
# def update_request_status(request_id: int, data: dict, db: Session = Depends(get_db)):
#     request = db.query(Request).filter_by(id=request_id).first()
#     if not request:
#         raise HTTPException(status_code=404, detail="Заявка не найдена")
#     request.status = data.get("status")
#     db.commit()
#     return {"message": "Статус обновлён", "status": request.status}



