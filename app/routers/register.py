from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models import User, Admin
from app.auth import get_password_hash, verify_password, create_access_token

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")



@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(username=user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_pwd = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_pwd,
        is_superadmin=user.is_superadmin if hasattr(user, "is_superadmin") else False,
        city_id=user.city_id if hasattr(user, "city_id") else None
    )
    db.add(db_user)
    db.commit()
    return {"msg": "Пользователь создан"}








@router.post("/admin/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    access_token = create_access_token(data={"sub": user.username})
    role = "admin" if user.is_superadmin else "editor"

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "role": role
        }
    }