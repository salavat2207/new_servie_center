from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session, joinedload
import shutil
import os

from uuid import uuid4

from app import schemas, crud
from app.database import get_db
from app.models import Product, ProductPrice, User, Admin, RepairService, City, RepairPrice
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


"""
Получение списка товаров и услуг
"""

@router.get("/services")
def get_services(city_code: str = Query(...), db: Session = Depends(get_db)):
    city = db.query(City).filter(City.code == city_code.upper()).first()
    if not city:
        raise HTTPException(status_code=404, detail="Город не найден")

    services = db.query(RepairService).filter(RepairService.city_id == city.id).all()

    product_map = {}
    for service in services:
        product = service.product
        if not product:
            continue

        if product.id not in product_map:
            product_map[product.id] = {
                "id": product.id,
                "title": product.title,
                "slug": product.slug,
                "categoryId": product.category_id,
                "description": product.description,
                "image": product.image,
                "repairServices": []
            }

        price_dict = {}
        for price in service.prices:
            price_dict[price.city_code] = price.price

        selected_price = price_dict.get(city_code.upper())

        product_map[product.id]["repairServices"].append({
            "id": service.id,
            "title": service.name,
            "description": service.description,
            "price": price_dict,
            "selectedPrice": selected_price,
            "duration": service.duration,
            "warranty": service.warranty,
            "categoryId": product.category_id
        })

    return list(product_map.values())






"""
Добавление услуг (Старый код)
"""
# @router.post("/add_service")
# def add_product(product: ProductPriceCreate, db: Session = Depends(get_db)):
#     existing_product = db.query(RepairService).filter(RepairService.id == product.id).first()
#     if existing_product:
#         raise HTTPException(status_code=400, detail="Товар с таким ID уже существует")
#
#     new_product = RepairService(
#         id=product.id,
#         title=product.title,
#         description=product.description,
#         price=product.price,
#         duration=product.duration,
#         warranty=product.warranty,
#         category_id=product.category_id,
#
#         # name=product.name,
#         # service_id=product.service_id,
#         # city_id=product.city_id,
#         # product_id=product.product_id,
#         # model=product.model,
#
#     )
#     try:
#         db.add(new_product)
#         db.commit()
#         db.refresh(new_product)
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Ошибка при добавлении: {str(e)}")
#
#     return {"message": "Товар успешно добавлен", "product": {
#         "id": new_product.id,
#         "name": new_product.name,
#         'service_id': new_product.service_id,
#         "price": new_product.price,
#         "city_id": new_product.city_id,
#         "description": new_product.description,
#         "duration": new_product.duration,
#         'product_id': new_product.product_id,
#         'category_id': new_product.category_id
#     }}

""""
Новый вариант
"""
# @router.post("/admin/add_service")
# def add_service(data: ProductPriceCreate, db: Session = Depends(get_db)):
#     # 1. Сначала ищем сам продукт:
#     product = db.query(Product).filter(Product.id == data.product_id).first()
#     if not product:
#         raise HTTPException(404, "Product not found")
#
#     new_price = RepairService(
#         id=product.id,
#         city_id=data.city_code,
#         product_id=data.product_id,
#         name=product.name,         # берём название из БД
#         title=product.title,       # берём заголовок из БД
#         model=product.model,       # и модель из БД, если она там есть
#         description=product.description,
#         duration="1-2 часа",       # или из запроса, если нужно
#         warranty="6 месяцев",
#         category_id=product.category_id,
#     )
#     db.add(new_price)
#     db.add(RepairPrice(
#         repair_id=new_price.id,
#         city_code=data.city_code,
#         price=data.price
#     ))
#     db.commit()
#     return {"status": "ok"}








"""
Добавление пользователей (рабочий вариант)
"""
#
# @router.post("/admin/create")
# def create_admin():
#     # Создаём таблицы, если их ещё нет
#     Base.metadata.create_all(bind=engine)
#
#     db = SessionLocal()
#     username = input("Введите имя суперадмина: ").strip()
#     password = input("Введите пароль суперадмина: ").strip()
#
#     existing_user = db.query(User).filter_by(username=username).first()
#     if existing_user:
#         print("❌ Пользователь с таким именем уже существует.")
#         return
#
#     hashed_password = get_password_hash(password)
#     admin = Admin(username=username, password=hashed_password, is_superadmin=True)
#     db.add(admin)
#     db.commit()
#     print("✅ Суперадмин успешно создан.")
#
#
# if __name__ == "__main__":
#     create_admin()




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
#
# """
# Частичное обновление услуги (рабочий)
# """
# @router.patch("/admin/repair-service/{service_id}", dependencies=[Depends(get_current_admin)])
# def patch_repair_service(service_id: str, update_data: RepairServicePatch, db: Session = Depends(get_db)):
#     service = db.query(RepairService).filter_by(service_id=service_id).first()
#     if not service:
#         raise HTTPException(status_code=404, detail="Услуга не найдена")
#
#     for field, value in update_data.dict(exclude_unset=True).items():
#         setattr(service, field, value)
#
#     db.commit()
#     db.refresh(service)
#
#     return {
#         "message": "Услуга частично обновлена",
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
#
#
#
#

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
# @router.delete("/admin/repair-services/{product_id}", dependencies=[Depends(get_current_admin)])
# def delete_repair_service_by_product(product_id: str, db: Session = Depends(get_db)):
#     service = db.query(RepairService).filter_by(product_id=product_id).first()
#     if not service:
#         raise HTTPException(status_code=404, detail="Услуга с таким product_id не найдена")
#
#     for price in service.prices:
#         db.delete(price)
#
#     db.delete(service)
#     db.commit()
#     return {"message": "Услуга и связанные с ней цены удалены"}


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
# @router.get("/", response_model=List[ProductPriceOut])
# def get_products(db: Session = Depends(get_db)):
#     return db.query(RepairService).all()
#
# # Загрузка изображений
# @router.post("/admin/upload-image")
# def upload_image(file: UploadFile = File(...)):
#     os.makedirs(UPLOAD_DIR, exist_ok=True)
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return {"url": f"/{file_path}"}


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
# #     }
# @router.get("/admin/product-price/{service_id}", dependencies=[Depends(get_current_admin)])
# def get_prices_by_service_id(service_id: str, db: Session = Depends(get_db)):
#     service = db.query(RepairService).filter_by(service_id=service_id).first()
#     if not service:
#         raise HTTPException(status_code=404, detail="Услуга не найдена")
#
#     cities = db.query(City).all()
#     prices_by_city = {price.city_code: price.price for price in service.prices}
#
#     result = []
#     for city in cities:
#         result.append({
#             "city": city.name,
#             "city_code": city.code,
#             "price": prices_by_city.get(city.code)
#         })
#
#     return {
#         "service_id": service.service_id,
#         "service_name": service.name,
#         'result': result
#     }


#
# router.post("/admin/requests/{request_id}/status", dependencies=[Depends(get_current_admin)])
# def update_request_status(request_id: int, data: dict, db: Session = Depends(get_db)):
#     request = db.query(Request).filter_by(id=request_id).first()
#     if not request:
#         raise HTTPException(status_code=404, detail="Заявка не найдена")
#     request.status = data.get("status")
#     db.commit()
#     return {"message": "Статус обновлён", "status": request.status}



"""
Остюда
"""

#
#
# @router.post("/add_product")
# def add_product(data: ProductCreate, db: Session = Depends(get_db)):
#     # Проверка — существует ли уже такой товар
#     existing = db.query(Product).filter(Product.id == data.id).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Product with this ID already exists")
#
#     new_product = Product(
#         id=data.id,
#         name=data.name,
#         title=data.title,
#         link=data.link,
#         description=data.description,
#         image=data.image,
#         slug=data.slug,
#         category_id=data.category_id,
#     )
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#
#     return {"status": "ok", "product": {"id": new_product.id, "name": new_product.name}}
#
#
#
#
# @router.post("/add_service")
# def add_service(data: ProductPriceCreate, db: Session = Depends(get_db)):
#     # Проверка города
#     city = db.query(City).filter(City.code == data.city_code.upper()).first()
#     if not city:
#         raise HTTPException(404, detail="Город с таким кодом не найден")
#
#     # Проверка продукта
#     product = db.query(Product).filter(Product.id == data.product_id).first()
#     if not product:
#         raise HTTPException(404, detail="Продукт не найден")
#
#     # Создание новой услуги
#     new_service = RepairService(
#         id=data.service_id,
#         city_id=city.id,
#         product_id=product.id,
#         name=data.name,
#         title=product.title,
#         # model=product.model,
#         description=data.description or product.description,
#         duration=data.duration,
#         warranty=data.warranty,
#         category_id=product.category_id,
#     )
#     db.add(new_service)
#     db.flush()  # чтобы new_service.id стал доступен
#
#     # Привязка цены к городу
#     new_price = RepairPrice(
#         repair_id=data.service_id,
#         city_code=data.city_code.upper(),
#         price=data.price
#     )
#     db.add(new_price)
#     db.commit()
#
#     return {"status": "ok", "service_id": new_service.id}
#
#
#
#
# @router.delete("/delete_product/{product_id}")
# def delete_product(product_id: str, db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Товар не найден")
#
#     db.query(ProductPrice).filter(ProductPrice.product_id == product_id).delete()
#     db.query(RepairService).filter(RepairService.product_id == product_id).delete()
#
#     db.delete(product)
#     db.commit()
#
#     return {"status": "ok", "message": f"Товар {product_id} удалён"}
#
#
# @router.delete("/delete_service/{service_id}")
# def delete_service(service_id: str, db: Session = Depends(get_db)):
#     # Найдём услугу
#     service = db.query(RepairService).filter(RepairService.id == service_id).first()
#     if not service:
#         raise HTTPException(status_code=404, detail="Услуга не найдена")
#
#     # Удалим связанные цены
#     db.query(RepairPrice).filter(RepairPrice.repair_id == service_id).delete()
#
#     # Удалим саму услугу
#     db.delete(service)
#     db.commit()
#
#     return {"status": "ok", "message": "Услуга успешно удалена"}







from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Path
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.utils import upload_image
import uuid

router = APIRouter(prefix="/admin", tags=["admin"])
UPLOAD_DIR = "static/images"

# Products
@router.get("/products", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    """Получить список продуктов"""
    return db.query(models.Product).all()

@router.post("/products", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Добавление продуктов"""
    db_product = models.Product(**payload.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    """Удаление продуктов"""
    prod = db.get(models.Product, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(prod)
    db.commit()

@router.patch("/products/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: str, payload: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """Обновление продуктов"""
    prod = db.get(models.Product, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in payload.dict(exclude_none=True).items():
        setattr(prod, field, value)
    db.commit()
    db.refresh(prod)
    return prod

# Services
@router.get("/services", response_model=List[schemas.ServiceOut])
def list_services(db: Session = Depends(get_db)):
    """Получить список услуг"""
    return db.query(models.RepairService).options(joinedload(models.RepairService.product)).all()

@router.post("/products/{product_id}/services", response_model=schemas.ServiceOut, status_code=status.HTTP_201_CREATED)
def add_service_to_product(
    product_id: str,
    payload: schemas.ServiceCreate,
    db: Session = Depends(get_db)
):
    """Добавление услуг"""

    prod = db.get(models.Product, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    # Создание RepairService, добавляем product_id
    # srv = models.RepairService(**payload.dict(), product_id=product_id)
    srv = models.RepairService(
        id=str(uuid.uuid4()),
        **payload.dict(),
        product_id=product_id
    )

    db.add(srv)
    db.commit()
    db.refresh(srv)

    return srv


@router.patch("/admin/services/{service_id}/description", response_model=schemas.ServiceOut)
def update_service_description(
    service_id: str = Path(..., description="ID услуги"),
    description: str = Query(..., description="Новое описание"),
    db: Session = Depends(get_db)
):
    """Редактирование описания"""
    service = db.query(models.RepairService).filter_by(id=service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.description = description
    db.commit()
    db.refresh(service)

    return service


@router.delete("/products/{product_id}/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_service(product_id: str, service_id: str, db: Session = Depends(get_db)):
    """Удаление услуг"""
    srv = db.query(models.RepairService).filter_by(id=service_id, product_id=product_id).first()
    if not srv:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(srv)
    db.commit()

@router.patch("/services/{service_id}", response_model=schemas.ServiceOut)
def update_service(service_id: str, payload: schemas.ServiceCreate, db: Session = Depends(get_db)):
    """Изменение услуг"""
    srv = db.get(models.RepairService, service_id)
    if not srv:
        raise HTTPException(status_code=404, detail="Service not found")
    for field, value in payload.dict(exclude_none=True).items():
        setattr(srv, field, value)
    db.commit()
    db.refresh(srv)
    return srv


@router.patch("/services/{service_id}/price", response_model=schemas.ServiceOut, operation_id="update_service_price_custom")
def update_service_price(
    service_id: str,
    city_code: str,
    new_price: int,
    db: Session = Depends(get_db)
):
    """Изменение цены услуги для конкретного города"""
    # Найти нужную запись в таблице ServicePrice
    sp = db.query(models.ServicePrice).filter_by(service_id=service_id, city_code=city_code).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Service price record not found")

    # Обновить цену
    sp.price = new_price
    db.commit()
    db.refresh(sp)

    # Вернуть саму услугу
    service = db.query(models.RepairService).filter_by(id=service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service



@router.patch("/services/{service_id}/price", response_model=schemas.ServiceOut)
def update_service_price(service_id: str, city_code: str, new_price: int, db: Session = Depends(get_db)):
    """Изменение цен"""
    sp = db.query(models.ServicePrice).filter_by(service_id=service_id, city_code=city_code).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Service price record not found")
    sp.price = new_price
    db.commit()
    db.refresh(sp)

    service = db.query(models.RepairService).filter_by(id=service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service

# Categories
@router.get("/categories", response_model=List[schemas.CategoryOut])
def list_categories(with_products: bool = False, db: Session = Depends(get_db)):
    """Получить список категорий"""
    if with_products:
        return db.query(models.Category).options(joinedload(models.Category.products)).all()
    return db.query(models.Category).all()

@router.post("/categories", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Добавление категорий"""
    cat = models.Category(**payload.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.patch("/categories/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: str, payload: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    """Изменение категорий"""
    cat = db.get(models.Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in payload.dict(exclude_none=True).items():
        setattr(cat, field, value)
    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    """Удааление услуг"""
    cat = db.get(models.Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()


@router.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"/{path}"}