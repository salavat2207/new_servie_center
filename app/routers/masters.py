from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db

router = APIRouter(
    prefix="/masters",
    tags=["Мастера"]
)

@router.post("/Создание мастеров", response_model=schemas.MasterOut)
def create_master(master: schemas.MasterCreate, db: Session = Depends(get_db)):
    existing_master = db.query(models.Master).filter_by(telegram_id=master.telegram_id).first()
    if existing_master:
        raise HTTPException(status_code=400, detail="Мастер с таким Telegram ID уже существует")

    new_master = models.Master(
        name=master.name,
        telegram_id=master.telegram_id,
        city_id=master.city_id
    )
    db.add(new_master)
    db.commit()
    db.refresh(new_master)
    return new_master





@router.get("/city/{city_id}", response_model=list[schemas.MasterOut])
def get_masters_by_city(city_id: int, db: Session = Depends(get_db)):
    """
    Получить список мастеров по городу
    """
    return crud.get_masters_by_city(db, city_id)