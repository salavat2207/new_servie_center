from fastapi import APIRouter, Depends

from app import schemas, models
from app.database import get_db
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.models import Product, RepairService
from app.schemas import (ProductOut, ProductWithServicesResponse, RepairServiceResponse)


router = APIRouter(
    prefix="/products",
    tags=["products"])


@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()




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


