from app.database import engine
from app.models import Base

def create_all():
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы.")

if __name__ == "__main__":
    create_all()