from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.models import Product, ProductPrice, User
from app.routers.auth import get_current_user
from app.schemas import ProductCreate, ProductPriceCreate, ProductPriceSchema, AdminLoginSchema, ProductCreateSchema
from app.auth import verify_password, create_access_token, get_current_admin, get_password_hash, get_current_admin_user

#
router = APIRouter(prefix="/admin", tags=["Admin"])

#
# @router.post("/add_admin")
# def add_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
#     return crud.create_admin(db, admin)
#
#
# @router.post("/categories/")
# def add_category(name: str, user=Depends(get_current_user)):
#     if not user["is_superadmin"]:
#         raise HTTPException(status_code=403, detail="Not authorized")
#
#
# @router.get("/applications/")
# def get_applications(user=Depends(get_current_user)):
#     # Для мастеров — только свои заявки
#     if user["is_superadmin"]:
#         return crud.get_all_requests(db)
#     else:
#         return crud.get_requests_by_master(db, user["id"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")


@router.post("/products добавить")
def create_product(
		product_data: ProductCreateSchema,
		db: Session = Depends(get_db),
		_: dict = Depends(get_current_admin_user),
):
	if db.query(Product).filter_by(id=product_data.id).first():
		raise HTTPException(status_code=400, detail="Product already exists")

	product = Product(
		id=product_data.id,
		title=product_data.title,
		link=product_data.link,
		category_id=product_data.category_id,
		description=product_data.description,
		image=product_data.image
	)
	db.add(product)
	db.commit()


@router.post("/product-price")
def set_product_price(data: ProductPriceSchema, db: Session = Depends(get_db)):
	existing = db.query(ProductPrice).filter_by(
		product_id=data.product_id,
		city_id=data.city_id
	).first()

	if existing:
		existing.price = data.price
		db.commit()
		return {"message": "Цена обновлена"}
	else:
		new_price = ProductPrice(
			product_id=data.product_id,
			city_id=data.city_id,
			price=data.price
		)
		db.add(new_price)
		db.commit()
		return {"message": "Новая цена добавлена"}


"""
Добавление пользователей
"""


@router.post("/admin/create")
def create_admin(user: schemas.AdminCreate, db: Session = Depends(get_db)):
	hashed_password = get_password_hash(user.password)
	new_user = User(username=user.username, password=hashed_password, is_superadmin=True)
	db.add(new_user)
	db.commit()
	return {"message": "Admin created"}


"""
Создаем энпоинт admin/login:
"""


@router.post("/admin/login")
def login_admin(data: schemas.AdminLoginSchema, db: Session = Depends(get_db)):
	admin = db.query(User).filter_by(username=data.username, is_superadmin=True).first()
	if not admin or not verify_password(data.password, admin.password):
		raise HTTPException(status_code=401, detail="Неверный логин или пароль")

	token = create_access_token({"sub": admin.username})
	return {"access_token": token, "token_type": "bearer"}


"""
Редактирование цены товара для города
"""


@router.put("/admin/product-price", dependencies=[Depends(get_current_admin)])
def update_price(product_id: str, city_id: int, price: int, db: Session = Depends(get_db)):
	price_entry = db.query(ProductPrice).filter_by(product_id=product_id, city_id=city_id).first()
	if not price_entry:
		raise HTTPException(status_code=404, detail="Цена не найдена")
	price_entry.price = price
	db.commit()
	return {"message": "Цена обновлена"}


"""
Удаление товара
"""


@router.delete("/admin/products/{product_id}", dependencies=[Depends(get_current_admin)])
def delete_product(product_id: str, db: Session = Depends(get_db)):
	product = db.query(Product).filter_by(id=product_id).first()
	if not product:
		raise HTTPException(status_code=404, detail="Продукт не найден")
	db.delete(product)
	db.commit()
	return {"message": "Продукт удалён"}
