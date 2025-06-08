from sqlalchemy.orm import Session

from app.auth import get_password_hash
from app.database import SessionLocal, Base, engine
from app.models import Product, City, ProductPrice, Admin, RepairService

Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

cities = [
    City(id=1, name="Челябинск", phone="+79049351111", adress="Свердловский проспект, 80", code="CHE"),
    City(id=2, name="Магнитогорск", phone="+73519393312", adress="проспект Карла Маркса, 153", code="MGN"),
    City(id=3, name="Екатеринбург", phone="79995896666", adress="проспект Ленина, 46", code="EKB"),
]


admin = [
    Admin(id=1, username='admin', password=get_password_hash('admin'), is_superadmin=True)
]


# repair_services = [
#     RepairService(id=1, name="Замена стекла", price=5000, city_id=1),
#     RepairService(id=2, name="Замена аккумулятора", price=3000, city_id=1),
#     RepairService(id=3, name="Замена динамика", price=2000, city_id=1),
#     RepairService(id=4, name="Замена корпуса", price=4000, city_id=1),
#     RepairService(id=5, name="Замена экрана", price=6000, city_id=1),
#     RepairService(id=6, name="Замена камеры", price=7000, city_id=1),
#     RepairService(id=7, name="Замена микрофона", price=2500, city_id=1),
#     RepairService(id=8, name="Замена кнопки включения", price=1500, city_id=1),
#
#
# ]

db.add_all(cities)
db.add_all(admin)
db.commit()
db.close()

print("База данных обновлена")