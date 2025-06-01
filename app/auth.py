from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User






"""
🛡JWT-защита
"""

SECRET_KEY = "секретный_ключ"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)




"""
Проверка токена
"""
def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
        return username
    except JWTError:
        raise HTTPException(status_code=401)



def get_current_admin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Недопустимый токен")
        user = db.query(User).filter_by(username=username).first()
        if user is None or not user.is_superadmin:
            raise HTTPException(status_code=403, detail="Недостаточно прав")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")




# Создаём контекст с алгоритмом bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция хеширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Функция проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)