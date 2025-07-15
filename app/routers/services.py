# from fastapi import APIRouter, Depends, Query, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.models import RepairService, City
#
# router = APIRouter()
#
#
# @router.get("/services/")
# def get_services(city_code: str = Query(...), db: Session = Depends(get_db)):
#     city = db.query(City).filter(City.code == city_code.upper()).first()
#     if not city:
#         raise HTTPException(status_code=404, detail="Город не найден")
#
#     services = db.query(RepairService).filter(RepairService.city_id == city.id).all()
#
#     product_map = {}
#     for service in services:
#         product = service.product
#         if not product:
#             continue
#
#         if product.id not in product_map:
#             product_map[product.id] = {
#                 "id": product.id,
#                 "title": product.title,
#                 "slug": product.slug,
#                 "categoryId": product.category_id,
#                 "description": product.description,
#                 "image": product.image,
#                 "repairServices": []
#             }
#
#         price_dict = {}
#         for price in service.prices:
#             price_dict[price.city_code] = price.price
#
#         selected_price = price_dict.get(city_code.upper())
#
#         product_map[product.id]["repairServices"].append({
#             "id": service.id,
#             "title": service.name,
#             "description": service.description,
#             "price": price_dict,
#             "selectedPrice": selected_price,
#             "duration": service.duration,
#             "warranty": service.warranty,
#             "categoryId": product.category_id
#         })
#
#     return list(product_map.values())
#
#
#
#
#
#
#
#
# @router.get("/products/{product_id}/services111")
# def get_services_for_product(product_id: str, city_code: str, db: Session = Depends(get_db)):
#     services = db.query(RepairService).filter(RepairService.product_id == product_id).all()
#     result = []
#
#     for service in services:
#         print(f"Цены для {service.name}: {[ (p.city_code, p.price) for p in service.prices ]}")
#
#         price_entry = next((p for p in service.prices if p.city_code.upper() == city_code.upper()), None)
#         price = price_entry.price if price_entry else None
#
#         result.append({
#             "id": service.id,
#             "name": service.name,
#             "description": service.description,
#             "duration": service.duration,
#             "price": price,
#             "product_name": service.product.name if service.product else None
#         })
#
#     return result