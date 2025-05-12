from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/add_admin")
def add_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud.create_admin(db, admin)