from app.database import SessionLocal
from app.models import Master

def seed_master():
    db = SessionLocal()
    test_master = Master(
        name="Тестовый мастер",
        phone="+79991234567",
        city_id=1,
        telegram_id=908977119  # Подставь свой Telegram ID
    )
    db.add(test_master)
    db.commit()
    db.close()
    print("✅ Тестовый мастер добавлен!")

if __name__ == "__main__":
    seed_master()