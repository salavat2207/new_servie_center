from sqlalchemy.orm import Session

from app.auth import get_password_hash
from app.database import SessionLocal, Base, engine
from app.models import Product, City, ProductPrice, Admin

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




db.add_all(cities)
db.add_all(admin)
db.commit()
db.close()

print("База данных обновлена")