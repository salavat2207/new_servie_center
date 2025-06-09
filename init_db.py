import os

from sqlalchemy.orm import Session
from app.auth import get_password_hash
from app.database import SessionLocal, Base, engine
from app.models import Product, City, ProductPrice, Admin, RepairService, User, Master


Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()


TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

cities = [
    City(id=1, name="Челябинск", phone="+79049351111", adress="Свердловский проспект, 80", code="CHE"),
    City(id=2, name="Магнитогорск", phone="+73519393312", adress="проспект Карла Маркса, 153", code="MGN"),
    City(id=3, name="Екатеринбург", phone="79995896666", adress="проспект Ленина, 46", code="EKB"),
]


admin = [
    Admin(id=1, username='admin', password=get_password_hash('admin'), is_superadmin=True)
]


repair_services = [
    RepairService(id=1,
                  city_id=1,
                  service_id="iphone-16-pro-screen-repair",
                  name="Замена дисплея",
                  description="Замена дисплея",
                  duration="1-2 часа",
                  price=8490,
                  category_id="apple iphone",
                  product_id="iphone-16-pro",

    ),
    RepairService(id=2,
                  city_id=1,
                  service_id="iphone-16-pro- battery-replacement",
                  name="Замена аккумулятора",
                  description="Замена аккумулятора",
                  duration="30-60 минут",
                  price=4990,
                  category_id="apple iphone",
                  product_id="iphone-16-pro",
                  ),
]



masters = [
    Master(id=1,
         name='Тест',
         telegram_id='908977119',
         city_id=1
           )
]





products = [
    Product(id="iphone-16-pro", title="Apple iPhone 16 Pro", description='Ремонт iPhone 16 Pro')
]




db.add_all(cities)
db.add_all(admin)
db.add_all(repair_services)
db.add_all(masters)
db.add_all(products)
db.commit()
db.close()

print("База данных обновлена")