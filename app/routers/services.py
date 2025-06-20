from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import RepairService, RepairServicePrice

router = APIRouter()


@router.get("/services/")
def get_services(city_code: str = Query(...), db: Session = Depends(get_db)):
    services = db.query(RepairService).all()
    result = []

    for service in services:
        price_entry = next((p for p in service.prices if p.city_code == city_code), None)
        price = price_entry.price if price_entry else None

        result.append({
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "duration": service.duration,
            "product_id": service.product_id,
            "price": price,
        })

    return result








@router.get("/products/{product_id}/services111")
def get_services_for_product(product_id: str, city_code: str, db: Session = Depends(get_db)):
    services = db.query(RepairService).filter(RepairService.product_id == product_id).all()
    result = []

    for service in services:
        print(f"Цены для {service.name}: {[ (p.city_code, p.price) for p in service.prices ]}")

        price_entry = next((p for p in service.prices if p.city_code.upper() == city_code.upper()), None)
        price = price_entry.price if price_entry else None

        result.append({
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "duration": service.duration,
            "price": price,
            "product_name": service.product.name if service.product else None
        })

    return result