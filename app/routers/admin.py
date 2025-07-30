from fastapi import Query
from fastapi.security import OAuth2PasswordBearer

import shutil
import os

from uuid import uuid4

from app.models import RepairService, City, Master, Application, Product

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Path
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.routers.requests import city_cache
from app.schemas import RepairRequestTelegram

from sqlalchemy.orm import joinedload




router = APIRouter(prefix="/admin", tags=["admin"])

UPLOAD_DIR = "/app/images"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")




@router.get("/services")
def get_services(city_code: str = Query(...), db: Session = Depends(get_db)):
    """Получение списка товаров и услуг"""
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

            "duration": service.duration,
            "warranty": service.warranty,
            "categoryId": product.category_id
        })

    return list(product_map.values())






router = APIRouter(prefix="/admin", tags=["admin"])
UPLOAD_DIR = "static/images"


@router.get("/products/full", response_model=List[schemas.ProductWithServicesResponse])
def get_all_products_with_services(db: Session = Depends(get_db)):
    """Получить список продуктов с услугами и ценами по городам"""
    products = db.query(models.Product).options(
        joinedload(models.Product.repair_services)
        .joinedload(models.RepairService.prices)
    ).all()

    response = []
    for product in products:
        services_data = []

        for service in product.repair_services:
            prices_by_city = {code: 0 for code in ['CHE', 'MGN', 'EKB']}
            for price in service.prices:
                if price.city_code in prices_by_city:
                    prices_by_city[price.city_code] = price.price

            services_data.append(schemas.RepairServiceResponse(
                service_id=service.service_id or "undefined",
                title=service.title,
                description=service.description or "",
                duration=service.duration or "",
                warranty=service.warranty or "",
                price=prices_by_city
            ))

        response.append(schemas.ProductWithServicesResponse(
            id=product.id,
            title=product.title,
            slug=product.slug,
            categoryId=product.category_id,
            description=product.description,
            image=product.image,
            repairServices=services_data
        ))

    return response



# Products
@router.get("/products", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    """Получить список продуктов"""
    return db.query(models.Product).all()


@router.post("/products", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product_in: schemas.ProductBase, db: Session = Depends(get_db)):
    """Добавление продуктов"""
    new_product = models.Product(
        id=product_in.id,
        title=product_in.title,
        slug=product_in.slug,
        category_id=product_in.category_id,
        description=product_in.description,
        image=product_in.image,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    """Удаление продуктов"""
    prod = db.get(models.Product, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(prod)
    db.commit()
    return {"detail": "Продукт удален"}



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


@router.post("/services", response_model=schemas.ServiceOut)
def create_service(service_data: schemas.RepairServiceCreate, db: Session = Depends(get_db)):
    """Создание услуг"""
    service = models.RepairService(
        service_id=service_data.service_id,
        title=service_data.title,
        description=service_data.description,
        duration=service_data.duration,
        warranty=service_data.warranty,
        product_id=service_data.product_id
    )
    db.add(service)
    db.commit()
    db.refresh(service)


    for city_code, price in service_data.price.items():
        sp = models.RepairPrice(
            repair_id=service.id,
            city_code=city_code,
            price=price
        )
        db.add(sp)

    db.commit()

    prices_by_city = {code: 0 for code in ['CHE', 'MGN', 'EKB']}
    for sp in service.prices:
        prices_by_city[sp.city_code] = sp.price

    return schemas.ServiceOut(
        service_id=service.service_id,
        title=service.title,
        description=service.description,
        duration=service.duration,
        warranty=service.warranty,
        price=prices_by_city
    )


@router.patch("/services/{service_id}/description", response_model=schemas.ServiceOut)
def update_service_description(
    service_id: str = Path(..., description="ID услуги (текстовый service_id)"),
    description: str = Query(..., description="Новое описание"),
    db: Session = Depends(get_db)
):
    """Редактирование описания"""
    service = db.query(models.RepairService)\
        .options(joinedload(models.RepairService.prices))\
        .filter_by(service_id=service_id).first()  # ✅ тут главное изменение

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.description = description
    db.commit()
    db.refresh(service)

    prices_by_city = {code: 0 for code in ['CHE', 'MGN', 'EKB']}
    for price in service.prices:
        if price.city_code in prices_by_city:
            prices_by_city[price.city_code] = price.price

    return schemas.ServiceOut(
        service_id=service.service_id,
        title=service.title,
        description=service.description,
        duration=service.duration,
        warranty=service.warranty,
        price=prices_by_city
    )


@router.delete("/products/{product_id}/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_service(product_id: str, service_id: str, db: Session = Depends(get_db)):
    """Удаление услуги"""
    srv = db.query(models.RepairService).filter_by(service_id=service_id, product_id=product_id).first()
    if not srv:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(srv)
    db.commit()




@router.patch("/services/{service_id}", response_model=schemas.ServiceOut)
def add_service_to_product(
    product_id: str,
    service_data: schemas.RepairServiceCreate,
    db: Session = Depends(get_db)
):
    """Изменение услуг"""
    srv = models.RepairService(
        service_id=service_data.service_id,
        title=service_data.title,
        description=service_data.description,
        duration=service_data.duration,
        warranty=service_data.warranty,
        product_id=product_id
    )
    db.add(srv)
    db.commit()
    db.refresh(srv)

    for city_code, price in service_data.price.items():
        price_entry = models.RepairPrice(
            repair_id=srv.id,
            city_code=city_code,
            price=price
        )
        db.add(price_entry)

    db.commit()
    db.refresh(srv)

    prices_dict = {price.city_code: price.price for price in srv.prices}

    return schemas.ServiceOut(
        service_id=srv.service_id,
        title=srv.title,
        description=srv.description,
        duration=srv.duration,
        warranty=srv.warranty,
        price=prices_dict
    )


@router.patch("/services/{service_id}/price", response_model=schemas.ServiceOut)
def update_service_price(
    service_id: str,
    product_id: str,
    city_code: str,
    new_price: int,
    db: Session = Depends(get_db)
):
    """Изменение цены на услугу для конкретного продукта и города"""
    service = db.query(models.RepairService)\
        .options(joinedload(models.RepairService.prices))\
        .filter(
            models.RepairService.service_id == service_id,
            models.RepairService.product_id == product_id
        ).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    price_record = next((p for p in service.prices if p.city_code == city_code), None)

    if price_record:
        price_record.price = new_price
    else:
        price_record = models.RepairPrice(
            repair_id=service.id,
            product_id=product_id,
            city_code=city_code,
            price=new_price
        )
        db.add(price_record)

    db.commit()
    db.refresh(service)

    prices_by_city = {code: 0 for code in ['CHE', 'MGN', 'EKB']}
    for p in service.prices:
        prices_by_city[p.city_code] = p.price

    return schemas.ServiceOut(
        service_id=service.service_id,
        product_id=service.product_id,
        title=service.title,
        description=service.description,
        duration=service.duration,
        warranty=service.warranty,
        price=prices_by_city
    )



@router.post('/')
async def send_repair_request(request: RepairRequestTelegram, db: Session = Depends(get_db)):
    if request.city_id not in city_cache:
        city = db.query(City).get(request.city_id)
        if city:
            city_cache[request.city_id] = city
        else:
            raise HTTPException(status_code=404, detail="Город не найден")

    product = db.query(Product).filter(Product.id == request.product_id).first()

    service = db.query(RepairService).filter(
        RepairService.product_id == request.product_id,
        RepairService.service_id == request.service_id  # <-- исправлено!
    ).first()

    if not product or not service:
        raise HTTPException(status_code=404, detail="Продукт или услуга не найдены")

    app = Application(
        phone=request.phone,
        description=request.description,
        city_id=request.city_id,
        name=request.name,
        code=str(uuid4())[:8],
        status="Новая заявка"
    )
    db.add(app)
    db.commit()
    db.refresh(app)

    message = (
        f"🛠 <b>Заявка на ремонт</b>\n"
        f"📱 <b>Модель:</b> {product.title}\n"
        f"🔧 <b>Услуга:</b> {service.title}\n"
        f"📝 <b>Описание услуги:</b> {service.description}\n"
        f"🙍‍♂️ <b>Имя:</b> {app.name}\n"
        f"📞 <b>Телефон:</b> {app.phone}"
    )

    # Разослать мастерам
    masters = db.query(Master).filter_by(city_id=request.city_id).all()
    for master in masters:
        if master.telegram_id:
            await TelegramBotService.send_message(chat_id=master.telegram_id, text=message)

    return {"message": "Заявка успешно отправлена"}




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




@router.put("/categories/{category_id}/image")
def update_category_image(
    category_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Загрузка изображений для категорий"""
    category = db.query(models.Category).filter_by(id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    filename = file.filename
    file_path = os.path.join("images", filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    category.image = f"/images/{filename}"
    db.commit()
    db.refresh(category)

    return {"image": category.image}




@router.delete("/categories/{category_id}/image")
def delete_category_image(category_id: str, db: Session = Depends(get_db)):
    """Удаление изображения категории"""
    category = db.query(models.Category).filter_by(id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    if category.image:
        image_path = category.image.lstrip("/")
        if os.path.exists(image_path):
            os.remove(image_path)

    category.image = None
    db.commit()
    db.refresh(category)

    return {"message": "Изображение удалено"}



@router.put("/products/{product_id}/image")
def update_product_image(
    product_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Загрузка изображений для продуктов"""
    product = db.query(models.Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    filename = file.filename
    file_path = os.path.join("images", filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    product.image = f"/images/{filename}"
    db.commit()
    db.refresh(product)

    return {"image": product.image}



@router.delete("/products/{product_id}/image")
def delete_product_image(product_id: str, db: Session = Depends(get_db)):
    """Удаление изображения продукта"""
    product = db.query(models.Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    if product.image:
        image_path = product.image.lstrip("/")
        if os.path.exists(image_path):
            os.remove(image_path)

    product.image = None
    db.commit()
    db.refresh(product)

    return {"message": "Изображение удалено"}