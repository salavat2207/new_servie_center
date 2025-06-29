import json
from sqlalchemy.orm import Session
from app.models import Service, RepairService
from app.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

def load_services():
    with open("services.json", encoding="utf-8") as f:
        data = json.load(f)

    db: Session = SessionLocal()
    for item in data:
        model = item["model"]
        url = item["url"]
        for s in item["services"]:
            service = Service(
                service = RepairService(
                model=model,
                url=url,
                name=s["service"],
                price=s["price"],
                description=s["description"]
            ))
            db.add(service)
    db.commit()

if __name__ == "__main__":
    load_services()