# from app.database import SessionLocal, engine, Base
# from app.models import Category, Product, City, ProductPrice, Admin, Master, RepairService, RepairPrice
# Base.metadata.create_all(bind=engine)
#
# # db = SessionLocal()
#
#
# categories = [
#     Category(id="apple-iphone", name="Смартфон"),
#     Category(id="apple-ipad", name="Планшет"),
# ]
#
# db.add_all(categories)
# db.commit()
#
# # Города
# cities = [
#     City(
#         id=1,
#         code="CHE",
#         name="Челябинск",
#         adress="Свердловский проспект, 80",
#         phone="+7 (904) 935-11-11",
#         hours="09:00 - 22:00",
#         image="D5Image",
#         coordinates=[55.156323, 61.388919]
#     ),
#     City(
#         id=2,
#         code="MGN",
#         name="Магнитогорск",
#         adress="проспект Карла Маркса, 153",
#         phone="+7 (3519) 39-33-12",
#         hours="10:00 - 21:00",
#         image="D7Image",
#         coordinates=[53.379132, 58.980157]
#     ),
#     City(
#         id=3,
#         code="EKB",
#         name="Екатеринбург",
#         adress="проспект Ленина, 46",
#         phone="+7 (999) 589-66-66",
#         hours="10:00 - 21:00",
#         image="D9Image",
#         coordinates=[56.839173, 60.614462]
#     ),
# ]
#
# db.add_all(cities)
# db.commit()
#
#
#
#
# products = [
#     Product(
#         id="iphone-16-pro",
#         title="iPhone 16 Pro",
#         slug="iphone-16-pro",
#         category_id="apple-iphone",  # Ссылка на категорию через id
#         description="Ремонт iPhone 16 Pro",
#         image="/src/assets/apple/iphone/16pro.jpg"
#     ),
#     Product(
#         id="iphone-16-pro-max",
#         title="iPhone 16 Pro Max",
#         slug="iphone-16-pro-max",
#         category_id="apple-iphone",
#         description="Ремонт iPhone 16 Pro Max",
#         image="/src/assets/apple/iphone/16promax.jpg"
#     ),
# ]
#
# db.add_all(products)
# # db.commit()
#
# # Пример добавления цены на продукт в конкретном городе
# product_prices = [
#     ProductPrice(product_id="iphone-16-pro", city_id=1, price=8490),
#     ProductPrice(product_id="iphone-16-pro", city_id=2, price=8590),
#     ProductPrice(product_id="iphone-16-pro", city_id=3, price=8690),
#     ProductPrice(product_id="iphone-16-pro-max", city_id=1, price=8990),
# ]
#
# db.add_all(product_prices)
# db.commit()
#
# # Мастера
# masters = [
#     Master(id=1, name='Тест', telegram_id=908977119, city_id=1),
# ]
#
# db.add_all(masters)
# db.commit()
#
# # Админ
# from app.auth import get_password_hash
#
# admin = Admin(id=1, username='admin', password=get_password_hash('admin'), is_superadmin=True)
# db.add(admin)
# db.commit()
#
# db.close()
#
# print('База создана')



#
# import os
# import json
# from sqlalchemy.orm import Session
# from uuid import uuid4
#
# from app.auth import get_password_hash
# from app.database import SessionLocal, Base, engine
# from app.models import Product, City, ProductPrice, Admin, RepairService, Master, Service
#
# Base.metadata.create_all(bind=engine)
#
# db: Session = SessionLocal()
#
# cities = [
# 	City(id=1,
# 		code="CHE",
# 		name="Челябинск",
# 		adress="Свердловский проспект, 80",
# 		phone="+7 (904) 935-11-11",
# 		hours="09:00 - 22:00",
# 		image="D5Image",
# 		coordinates=[55.156323, 61.388919]),
#
# 	City(id=2,
# 		code="MGN",
# 		name="Магнитогорск",
# 		adress="проспект Карла Маркса, 153",
# 		phone="+7 (3519) 39-33-12",
# 		hours="10:00 - 21:00",
# 		image="D7Image",
# 		coordinates=[53.379132, 58.980157]),
#
# 	City(id=3,
# 		code="EKB",
# 		name="Екатеринбург",
# 		adress="проспект Ленина, 46",
# 		phone="+7 (999) 589-66-66",
# 		hours="10:00 - 21:00",
# 		image="D9Image",
# 		coordinates=[56.839173, 60.614462])
# ]
#
#
# admin = [
# 	Admin(id=1, username='admin', password=get_password_hash('admin'), is_superadmin=True)
# ]
#
# masters = [
# 	Master(id=1, name='Тест', telegram_id='908977119', city_id=1)
# ]
#
# products = [
# 		Product(
# 			id="iphone-16-pro",
# 			title="Apple iPhone 16 Pro",
# 			slug="iphone-16-pro",
# 			category_id="apple-iphone",
# 			description="Ремонт iPhone 16 Pro",
# 			image="/src/assets/apple/iphone/16pro.jpg"
# 		),
# 		Product(
# 			id="iphone-16-pro-max",
# 			title="Apple iPhone 16 Pro Max",
# 			slug="iphone-16-pro-max",
# 			category_id="apple-iphone",
# 			description="Ремонт iPhone 16 Pro Max",
# 			image="/src/assets/apple/iphone/16promax.jpg"
# 		),
# 	]
#
#
# repair_services = [
# 		RepairService(
# 			id=1,
# 			city_id=1,
# 			product_id="iphone-16-pro",
# 			model ='iphone 16 pro',
# 			description='Замена дисплея на  iPhone 16 pro',
# 			duration='1-2 часа',
# 			warranty='6 месяцев',
# 			category_id='iphone-16-pro-battery-replacement'
# 		),
#
# 		RepairService(
# 			id=2,
# 			city_id=2,
# 			product_id="iphone-16-pro",
# 			model ='iphone 16 pro',
# 			description='Замена дисплея на  iPhone 16 pro',
# 			duration='1-2 часа',
# 			warranty='6 месяцев',
# 			category_id='iphone-16-pro-battery-replacement'
# 		)
# ]
#
#
# product_prices = [
# 	ProductPrice(product_id="iphone-16-pro",  city_id=1, service_id='iphone-16-pro-battery-replacement', price=8490),
# 	ProductPrice(product_id="iphone-16-pro",  city_id=2, service_id='iphone-16-pro-battery-replacement', price=8590),
# 	ProductPrice(product_id="iphone-16-pro", city_id=3, service_id='iphone-16-pro-battery-replacement', price=8690),
# 	ProductPrice(product_id="iphone-16-pro-max", city_id=1, service_id='iphone-16-pro-battery-replacement', price=8990),
# ]
#
#
#
#
# db.add_all(cities)
# db.add_all(admin)
# db.add_all(masters)
# db.add_all(repair_services)
# db.add_all(products)
# db.add_all(product_prices)
# db.commit()
# db.close()
#
# print("База данных обновлена")

# init_db.py







# import os
# from sqlalchemy.orm import Session
# from uuid import uuid4
#
# from app.auth import get_password_hash
# from app.database import SessionLocal, Base, engine
# from app.models import (
#     Category, Product, City, ProductPrice,
#     Admin, Master, RepairService, ServicePrice
# )
#
# # Пересоздаём всю схему
# # Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
#
# db: Session = SessionLocal()
#
# # Категории
# categories = [
#     Category(id="apple-iphone", name="Смартфон"),
#     Category(id="apple-ipad", name="Планшет"),
# ]
#
# # Города
# cities = [
#     City(
#         id=1,
#         code="CHE",
#         name="Челябинск",
#         adress="Свердловский проспект, 80",
#         phone="+7 (904) 935-11-11",
#         hours="09:00 - 22:00",
#         image="D5Image",
#         coordinates=[55.156323, 61.388919]
#     ),
#     City(
#         id=2,
#         code="MGN",
#         name="Магнитогорск",
#         adress="проспект Карла Маркса, 151/1",
#         phone="+7 (3519) 39-33-12",
#         hours="10:00 - 21:00",
#         image="D7Image",
#         coordinates=[53.380025, 58.979878]
#
#     ),
#     City(
#         id=3,
#         code="EKB",
#         name="Екатеринбург",
#         adress="проспект Ленина, 46",
#         phone="+7 (999) 589-66-66",
#         hours="10:00 - 21:00",
#         image="D9Image",
#         coordinates=[56.839173, 60.614462]
#     ),
# ]
#
# products = [
#     Product(
#         id="iphone-16-pro",
#         name="Apple iPhone 16 Pro",
#         slug="Apple iPhone 16 Pro",
#         title="iPhone",
#         category_id="apple-iphone",
#         description="Ремонт iPhone 16 Pro",
#         image="/src/assets/apple/iphone/16pro.jpg"
#     ),
# ]
#
# # Админ
# admin = [
#     Admin(id=1, username='admin', password=get_password_hash('admin'), is_superadmin=True)
# ]
#
# # Мастера
# masters = [
#     Master(id=1, name='Тест', telegram_id=908977119, city_id=1)
# ]
#
# # Сервисы ремонта
# repair_services = [
#     RepairService(
#         id="iphone-16-pro-screen-repair",
#         name='Замена дисплея iPhone 16 Pro',
#         description='Замена дисплея на iPhone 16 Pro',
#         duration='1-2 часа',
#         product_id='iphone-16-pro',
#         model="iphone 16 pro",
#         title='iphone 16 pro',
#         category_id='apple-iphone',
#         city_id=1,
#         warranty="6 месяцев",
#     ),
#     RepairService(
#         id="iphone-16-pro-mgn-screen-repair",
#         name='Замена дисплея iPhone 16 Pro (Магнитогорск)',
#         description='Замена дисплея на iPhone 16 Pro в Магнитогорске',
#         duration='1-2 часа',
#         product_id='iphone-16-pro',
#         category_id='apple-iphone',
#         city_id=2
#     ),
# ]
#
# # Цены на сервисы по городам
# service_prices = []
# for svc in repair_services:
#     # используем именно id каждого сервиса, а не статичную строку
#     sid = str(svc.id)
#     service_prices.append(ServicePrice(service_id=sid, city_code='CHE', price=8490))
#     service_prices.append(ServicePrice(service_id=sid, city_code='MGN', price=10000))
#     service_prices.append(ServicePrice(service_id=sid, city_code='EKB', price=8690))
#
# # Цены на продукты по городам (если используются)
# product_prices = [
#     ProductPrice(id=1, product_id='iphone-16-pro', city_code='CHE', price=8490),
#     ProductPrice(id=2, product_id='iphone-16-pro', city_code='MGN', price=8590),
#     ProductPrice(id=3, product_id='iphone-16-pro', city_code='EKB', price=8690),
#     ProductPrice(id=4, product_id='iphone-16-pro-max', city_code='CHE', price=8990),
# ]
#
# # Сохраняем все
# for collection in (categories, cities, products, admin, masters, repair_services, service_prices, product_prices):
#     db.add_all(collection)
#
# db.commit()
# db.close()
#
# print("База данных успешно инициализирована")








import sys
from pathlib import Path
import json
from sqlalchemy.orm import Session

from app.auth import get_password_hash
from app.database import SessionLocal, engine, Base
from app.models import Product, RepairService, RepairPrice, Category, City, Admin

# Указываем корень проекта
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Создаём все таблицы
Base.metadata.create_all(bind=engine)

# Загружаем JSON
json_path = BASE_DIR / "devices_with_link_services_final.json"
with open(json_path, "r", encoding="utf-8") as f:
    products_data = json.load(f)

db: Session = SessionLocal()

# === ДОБАВЛЕНИЕ КАТЕГОРИЙ ===
unique_categories = {}
for product in products_data:
    cat_id = product["category_id"]
    cat_name = product["category"]
    if cat_id not in unique_categories:
        unique_categories[cat_id] = cat_name

for cat_id, cat_name in unique_categories.items():
    existing = db.query(Category).filter_by(id=cat_id).first()
    if not existing:
        db.add(Category(id=cat_id, name=cat_name))

# === ДОБАВЛЕНИЕ ПРОДУКТОВ И УСЛУГ ===
for product_data in products_data:
    existing_product = db.query(Product).filter_by(title=product_data["title"]).first()
    if existing_product:
        continue

    product = Product(
        id=product_data["id"],
        name=product_data["name"],
        title=product_data["title"],
        slug=product_data["slug"],
        link=product_data["link"],
        category=product_data["category"],
        category_id=product_data["category_id"],
        description=product_data["description"],
        image=product_data["image"]
    )
    db.add(product)

    for service in product_data["repairServices"]:
        repair_service = RepairService(
            id=service["id"],
            title=service["title"],
            name=service["title"],
            description=service["description"],
            warranty=service["warranty"],
            duration=service["duration"],
            product_id=product.id,
            model=product.name,
            category_id=service["categoryId"],
        )
        db.add(repair_service)

        for city_code, price in service["price"].items():
            db.add(RepairPrice(
                repair_id=repair_service.id,
                city_code=city_code,
                price=price
            ))

cities = [
    City(
        id=1,
        code="CHE",
        name="Челябинск",
        adress="Свердловский проспект, 80",
        phone="+7 (904) 935-11-11",
        hours="09:00 - 22:00",
        image="D5Image",
        coordinates=[55.156323, 61.388919]
    ),
    City(
        id=2,
        code="MGN",
        name="Магнитогорск",
        adress="проспект Карла Маркса, 151/1",
        phone="+7 (3519) 39-33-12",
        hours="10:00 - 21:00",
        image="D7Image",
        coordinates=[53.380025, 58.979878]

    ),
    City(
        id=3,
        code="EKB",
        name="Екатеринбург",
        adress="проспект Ленина, 46",
        phone="+7 (999) 589-66-66",
        hours="10:00 - 21:00",
        image="D9Image",
        coordinates=[56.839173, 60.614462]
    ),
]
for city in cities:
    existing = db.query(City).filter_by(id=city.id).first()
    if not existing:
        db.add(city)



existing_admin = db.query(Admin).filter_by(username="device_service").first()
if not existing_admin:
    admin = Admin(
        id=1,
        username='device_service',
        password=get_password_hash('Device@174'),
        is_superadmin=True
    )
    db.add(admin)



db.commit()
db.close()

print("✅ База данных и категории успешно созданы и заполнены.")
