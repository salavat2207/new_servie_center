from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models import Product, City, ProductPrice




Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

cities = [
    City(id=1, name="Челябинск", phone="+79049351111", adress="Свердловский проспект, 80", code="CHE"),
    City(id=2, name="Магнитогорск", phone="+73519393312", adress="проспект Карла Маркса, 153", code="MGN"),
    City(id=3, name="Екатеринбург", phone="79995896666", adress="проспект Ленина, 46", code="EKB"),
]

db.add_all(cities)
db.commit()
db.close()

print("Города добавлены.")