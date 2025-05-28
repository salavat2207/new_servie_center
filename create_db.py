from app.database import engine, Base
# from app import models
from app.models import *

print("Создание базы данных...")

Base.metadata.create_all(bind=engine)

print("База данных создана.")