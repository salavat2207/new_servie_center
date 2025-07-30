from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db

from sqlalchemy.orm import joinedload
from collections import defaultdict
from app.schemas import MenuItem, SubItem, ProductOut

router = APIRouter()


@router.get("/categories", response_model=List[schemas.CategoryOut])
def list_categories(with_products: bool = False, db: Session = Depends(get_db)):
    """Получить список категорий"""
    if with_products:
        return db.query(models.Category).options(joinedload(models.Category.products)).all()
    return db.query(models.Category).all()



@router.post("/categories", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Добавление категорий"""
    cat = models.Category(**payload.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat



@router.patch("/categories/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: str, payload: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    """Изменение категорий"""
    cat = db.get(models.Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in payload.dict(exclude_none=True).items():
        setattr(cat, field, value)
    db.commit()
    db.refresh(cat)
    return cat





@router.get("/menu", response_model=List[MenuItem])
def get_menu(db: Session = Depends(get_db)):
    categories = db.query(models.Category).options(joinedload(models.Category.products)).all()

    grouped = defaultdict(list)

    for cat in categories:
        products = [
            ProductOut.from_orm(p) for p in cat.products
        ]
        product = cat.products[0] if cat.products else None

        image = f"/images/{product.image.lstrip('/')}" if product and product.image else ""
        sub_item = SubItem(
            id=cat.id,
            title=cat.name,
            slug=cat.id,
            image=f"/images/{product.image.lstrip('/')}" if product and product.image else "",
            categoryId=cat.id,
            products=products
        )
        grouped[cat.brand or "Без бренда"].append(sub_item)

    menu = [
        MenuItem(
            title=brand,
            slug=brand.lower().replace(" ", "-"),
            subitems=sorted(sub_items, key=lambda s: s.title) if sub_items else []
        )
        for brand, sub_items in grouped.items()
    ]

    return sorted(menu, key=lambda m: m.title)