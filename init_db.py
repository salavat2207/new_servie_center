import os
import json
from sqlalchemy.orm import Session
from app.auth import get_password_hash
from app.database import SessionLocal, Base, engine
from app.models import Product, City, ProductPrice, Admin, RepairService, Master, Service

Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

cities = [
	City(id=1,
		code="CHE",
		name="Челябинск",
		adress="Свердловский проспект, 80",
		phone="+7 (904) 935-11-11",
		hours="09:00 - 22:00",
		image="D5Image",
		coordinates=[55.156323, 61.388919]),

	City(id=2,
		code="MGN",
		name="Магнитогорск",
		adress="проспект Карла Маркса, 153",
		phone="+7 (3519) 39-33-12",
		hours="10:00 - 21:00",
		image="D7Image",
		coordinates=[53.379132, 58.980157]),

	City(id=3,
		code="EKB",
		name="Екатеринбург",
		adress="проспект Ленина, 46",
		phone="+7 (999) 589-66-66",
		hours="10:00 - 21:00",
		image="D9Image",
		coordinates=[56.839173, 60.614462])
]


admin = [
	Admin(id=1, username='admin', password=get_password_hash('admin'), is_superadmin=True)
]

masters = [
	Master(id=1, name='Тест', telegram_id='908977119', city_id=1)
]

products = [
	Product(
		id="iphone-16-pro",
		name="iPhone 16 Pro",
		category="Смартфон",
		title="Apple iPhone 16 Pro",
		description="Ремонт iPhone 16 Pro",
	),
	Product(
		id="iphone-16-pro-max",
		name="iPhone 16 Pro Max",
		category="Смартфон",
		title="Apple iPhone 16 Pro Max",
		description="Ремонт iPhone 16 Pro Max",
	)
]

product_prices = [
	ProductPrice(product_id="iphone-16-pro", city_id=1, price=8490),
	ProductPrice(product_id="iphone-16-pro", city_id=2, price=8590),
	ProductPrice(product_id="iphone-16-pro", city_id=3, price=8690),
	ProductPrice(product_id="iphone-16-pro-max", city_id=1, price=8990),
]


def parse_price(price_str: str) -> int | None:
	try:
		cleaned = price_str.replace(" ", "").replace("-", "").replace(".", "")
		return int(cleaned)
	except (ValueError, TypeError):
		return None


def load_services():
	with open("services.json", encoding="utf-8") as f:
		data = json.load(f)

	db: Session = SessionLocal()
	for item in data:
		model = item.get("model")
		for s in item.get("services", []):
			price = parse_price(s["price"])
			service = RepairService(
				model=model,
				name=s["service"],
				price=price,
				description=s["description"],
				duration="~",
				city_id=s.get("city_id", 1),
			)
			db.add(service)
	db.commit()
	db.close()


if __name__ == "__main__":
	load_services()

	db.add_all(cities)
	db.add_all(admin)
	db.add_all(masters)
	db.add_all(products)
	db.add_all(product_prices)
	db.commit()
	db.close()

	print("База данных обновлена")
