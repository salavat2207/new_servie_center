import json
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product, RepairService

def load_data_from_json():
    with open("app/data/repair_products_filtered_fixed.json", encoding="utf-8") as f:
        data = json.load(f)

    db: Session = SessionLocal()

    for product in data:
        product_obj = Product(
            id=product["id"],
            name=product["name"],
            # brand=product["brand"],
            category=product["category"]
        )
        db.add(product_obj)

        for service in product["services"]:
            service_obj = RepairService(
                id=service["id"],
                title=service["title"],
                description=service.get("description", ""),
                product_id=product["id"]
            )
            db.add(service_obj)

    db.commit()
    db.close()
    print("✅ Данные успешно загружены")

if __name__ == "__main__":
    load_data_from_json()