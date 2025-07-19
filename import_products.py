
import json
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product, RepairService, RepairPrice
from slugify import slugify

from init_db import db, product, product_data

FILENAME = "/Users/salavatgibadullin/Documents/service_center/new_servie_center/devices_with_link_services_final.json"

SERVICE_ID_MAP = {
    "Замена дисплея": "display_replacement",
    "Замена аккумулятора": "battery_replacement",
    "Замена камеры": "camera_replacement",
    "Замена задней крышки": "back_cover_replacement",
    # дополнить по необходимости
}


for service in product_data.get("repairServices", []):
    title = service["title"]
    service_obj = RepairService(
        title=title,
        description=service.get("description", ""),
        duration=service.get("duration", ""),
        warranty=service.get("warranty", ""),
        # product_id=product.id,
        service_id=SERVICE_ID_MAP.get(title, slugify(title))
    )


def load_data_from_file(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def import_data(session: Session, data: list):
    for product_data in data:
        existing_product = session.query(Product).filter_by(title=product_data["title"]).first()
        if existing_product:
            print(f"Пропущен: {product_data['title']} (уже существует)")
            continue

        product = Product(
            id=product_data["id"],
            title=product_data["title"],
            slug=product_data["slug"],
            # link=product_data["link"],
            # category=product_data["category"],
            category_id=product_data.get("category_id", "unknown"),
            description=product_data["description"],
            image=product_data["image"]
        )
        session.add(product)

        for service in product_data["repairServices"]:
            repair_service = RepairService(
                # id=service["id"],
                title=service["title"],
                # name=service["title"],
                description=service["description"],
                warranty=service["warranty"],
                duration=service["duration"],
                product_id=product.id,
                # model=product.name,
                # category_id=service["categoryId"],
            )

            for city_code, price in service["price"].items():
                repair_price = RepairPrice(
                    city_code=city_code,
                    price=price
                )
                repair_service.prices.append(repair_price)
            product.repair_services.append(repair_service)




def main():
    from sqlalchemy import create_engine
    from app.database import Base, SessionLocal
    engine = create_engine("sqlite://///Users/salavatgibadullin/Documents/service_center/new_servie_center/service_center.db")
    Base.metadata.bind = engine
    SessionLocal.configure(bind=engine)
    data = load_data_from_file(FILENAME)
    db = SessionLocal()

    try:
        import_data(db, data)
        db.commit()
        print("Импорт завершён успешно.")
    except Exception as e:
        db.rollback()
        print("Ошибка при импорте:", e)
    finally:
        db.close()

for service in db.query(RepairService).filter(RepairService.service_id == None).all():
    service.service_id = slugify(service.title)
db.commit()





if __name__ == "__main__":
    main()


