from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import RepairService

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import RepairService, RepairPrice




# Словарь product_id'ов по моделям
manual_map = {
    "iPhone X": "iphone-x",
    "iPhone XR": "iphone-xr",
    "iPhone XS": "iphone-xs",
    "iPhone XS Max": "iphone-xs-max",
    "iPhone 11": "iphone-11",
    "iPhone 11 Pro": "iphone-11-pro",
    "iPhone 11 Pro Max": "iphone-11-pro-max",
    "iPhone 12": "iphone-12",
    "iPhone 12 mini": "iphone-12-mini",
    "iPhone 12 Pro": "iphone-12-pro",
    "iPhone 12 Pro Max": "iphone-12-pro-max",
    "iPhone 13": "iphone-13",
    "iPhone 13 mini": "iphone-13-mini",
    "iPhone 13 Pro": "iphone-13-pro",
    "iPhone 13 Pro Max": "iphone-13-pro-max",
    "iPhone 14": "iphone-14",
    "iPhone 14 Plus": "iphone-14-plus",
    "iPhone 14 Pro": "iphone-14-pro",
    "iPhone 14 Pro Max": "iphone-14-pro-max",
    "iPhone 15": "iphone-15",
    "iPhone 15 Plus": "iphone-15-plus",
    "iPhone 15 Pro": "iphone-15-pro",
    "iPhone 15 Pro Max": "iphone-15-pro-max",
    "iPhone SE (2020)": "iphone-se-2020",
    "iPhone SE (2022)": "iphone-se-2022",
    "iPad 8": "ipad-8",
    "iPad 9": "ipad-9",
    "iPad 10": "ipad-10",
    "iPad Air (2020)": "ipad-air-2020",
    "iPad Air (2022)": "ipad-air-2022",
    "iPad Pro 11 (2020)": "ipad-pro-11-2020",
    "iPad Pro 11 (2021)": "ipad-pro-11-2021",
    "iPad Pro 11 (2022)": "ipad-pro-11-2022",
    "iPad Pro 11 (2024)": "ipad-pro-11-2024",
    "iPad Pro 12.9 (2020)": "ipad-pro-12.9-2020",
    "iPad Pro 12.9 (2021)": "ipad-pro-12.9-2021",
    "iPad Pro 12.9 (2022)": "ipad-pro-12.9-2022",
    "iPad Pro 12.9 (2024)": "ipad-pro-12.9-2024",
    "Samsung S20": "samsung-s20",
    "Samsung S20+": "samsung-s20+",
    "Samsung S20 Ultra": "samsung-s20-ultra",
    "Samsung S21": "samsung-s21",
    "Samsung S21+": "samsung-s21+",
    "Samsung S21 Ultra": "samsung-s21-ultra",
    "Samsung S22": "samsung-s22",
    "Samsung S22+": "samsung-s22+",
    "Samsung S22 Ultra": "samsung-s22-ultra",
    "Samsung S23": "samsung-s23",
    "Samsung S23+": "samsung-s23+",
    "Samsung S23 Ultra": "samsung-s23-ultra",
    "Samsung S24": "samsung-s24",
    "Samsung S24+": "samsung-s24+",
    "Samsung S24 Ultra": "samsung-s24-ultra",
    "Samsung A32": "samsung-a32",
    "Samsung A52": "samsung-a52",
    "Samsung A72": "samsung-a72",
    "Samsung A33": "samsung-a33",
    "Samsung A53": "samsung-a53",
    "Samsung A73": "samsung-a73",
    "Samsung A34": "samsung-a34",
    "Samsung A54": "samsung-a54",
    "Samsung Z Flip": "samsung-z-flip",
    "Samsung Z Flip 3": "samsung-z-flip-3",
    "Samsung Z Fold": "samsung-z-fold",
    "Samsung Z Fold 3": "samsung-z-fold-3",
    "Xiaomi Mi 10": "xiaomi-mi-10",
    "Xiaomi Mi 10T": "xiaomi-mi-10t",
    "Xiaomi Mi 11": "xiaomi-mi-11",
    "Xiaomi Mi 11 Lite": "xiaomi-mi-11-lite",
    "Xiaomi Mi 11 Ultra": "xiaomi-mi-11-ultra",
    "Xiaomi 12": "xiaomi-12",
    "Xiaomi 12 Pro": "xiaomi-12-pro",
    "Xiaomi 12T": "xiaomi-12t",
    "Xiaomi 13": "xiaomi-13",
    "Xiaomi 13 Pro": "xiaomi-13-pro",
    "Xiaomi 13T": "xiaomi-13t",
    "Xiaomi 14": "xiaomi-14",
    "Xiaomi 14 Ultra": "xiaomi-14-ultra",
    "Redmi Note 9": "redmi-note-9",
    "Redmi Note 10": "redmi-note-10",
    "Redmi Note 11": "redmi-note-11",
    "Redmi Note 12": "redmi-note-12",
    "Redmi Note 13": "redmi-note-13",
    "Poco X3": "poco-x3",
    "Poco X3 Pro": "poco-x3-pro",
    "Poco X4 Pro": "poco-x4-pro",
    "Poco X5": "poco-x5",
    "Poco X5 Pro": "poco-x5-pro",
    "Poco X6": "poco-x6",
    "Poco X6 Pro": "poco-x6-pro",
}

# Запуск сессии
db: Session = SessionLocal()

# Услуги без привязки к продукту
services = db.query(RepairService).filter(RepairService.product_id == None).order_by(RepairService.id).all()
product_ids = list(manual_map.values())

updated = 0
unmatched = []

i = 0
for idx, service in enumerate(services):
    if i >= len(product_ids):
        unmatched.append(service.title)
        continue

    service.product_id = product_ids[i]
    updated += 1

    # Каждые 4 услуги — следующий продукт
    if (idx + 1) % 4 == 0:
        i += 1

db.commit()

print(f"Автоматически обновлено записей: {updated}")
if unmatched:
    print("Не сопоставлены product_id:", len(unmatched))
    for title in unmatched:
        print(title)






# Настрой стандартные цены по умолчанию
default_prices = {
    'CHE': 8990,
    'MGN': 9490,
    'EKB': 9990
}

# Получаем все услуги без цен
services = db.query(RepairService).all()
added = 0

for service in services:
    if not service.prices or len(service.prices) == 0:
        for city_code, price in default_prices.items():
            db.add(RepairPrice(
                repair_id=service.id,
                city_code=city_code,
                price=price
            ))
        added += 1

db.commit()
print(f"✅ Добавлены цены для {added} услуг без цен.")