from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from uuid import uuid4

"""
Город сервисного центра
"""


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    phone = Column(String)
    adress = Column(String)
    hours = Column(String)
    image = Column(String)
    coordinates = Column(JSON)

    feedbacks = relationship("Feedback", back_populates="city")
    requests = relationship('RepairRequest', back_populates='city')
    masters = relationship("Master", back_populates="city")
    code = Column(String(3))

"""
Запрос на ремонт
"""


class RepairRequest(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    phone = Column(String, nullable=False)
    description = Column(String, nullable=False)
    accepted_at = Column(DateTime, nullable=False)
    accepted_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='Новая заявка')

    city = relationship("City", back_populates="requests")

    # product = relationship("Product", back_populates="requests")



class RepairService(Base):
    __tablename__ = "repair_services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String, index=True)
    title = Column(String)
    description = Column(Text)
    duration = Column(String)
    warranty = Column(String)
    # price = Column(Integer, nullable=True)

    product_id = Column(String, ForeignKey("products.id"))

    product = relationship("Product", back_populates="repair_services")
    prices = relationship("RepairPrice", back_populates="repair_service", cascade="all, delete-orphan", lazy="joined")
    # repair_prices = relationship("RepairPrice", back_populates="repair_service")




class RepairPrice(Base):
    __tablename__ = "repair_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    repair_id = Column(Integer, ForeignKey("repair_services.id"), nullable=False)
    city_code = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    # repair_service = relationship("RepairService", back_populates="repair_prices")
    repair_service = relationship("RepairService", back_populates="prices")







class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    url = Column(String)
    name = Column(String)
    price = Column(String)
    description = Column(Text)
    model = Column(String)
    city_id = Column(Integer, ForeignKey('cities.id'))


class Master(Base):
    __tablename__ = 'masters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    telegram_id = Column(Integer)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    city = relationship("City", back_populates="masters")


"""
Обратная связь
"""
class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    city_id = Column(Integer, ForeignKey("cities.id"))
    request_number = Column(String)
    category_id = Column(String)
    product_id = Column(String)
    service_id = Column(String)

    description = Column(Text)
    duration = Column(String)
    price = Column(Integer)
    city = relationship("City", back_populates="feedbacks")



class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String(128), nullable=False)
    is_superadmin = Column(Boolean, default=True)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String(128), nullable=False)
    is_superadmin = Column(Boolean, default=False)
    city_id = Column(Integer, ForeignKey("cities.id"))







class Category(Base):
    __tablename__ = 'categories'
    id = Column(String, primary_key=True)
    image = Column(String)
    name = Column(String, unique=True, index=True)
    brand = Column(String, nullable=True)

    # products = relationship("Product", back_populates="category")


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    description = Column(String)
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("City")
    name = Column(String, nullable=False)
    assigned_master_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default='Новая заявка')
    assigned_master = relationship("User", foreign_keys=[assigned_master_id])

    code = Column(String, unique=True, index=True)

    city = relationship("City")



class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, nullable=False)
    # name = Column(String, primary_key=True, nullable=True)
    category_id = Column(String, ForeignKey("categories.id"))
    title = Column(String, index=True)
    # link = Column(String, index=True)
    # product_id = Column(String, ForeignKey("products.id"))
    description = Column(String, nullable=True)
    image = Column(String)
    slug = Column(String, index=True)

    repair_services = relationship("RepairService", back_populates="product", lazy="joined")
    prices = relationship("ProductPrice", back_populates="product", passive_deletes=True)






"""
Модель ProductPrice, которая будет связывать Product и City с конкретной ценой
"""


class ProductPrice(Base):
    __tablename__ = "product_prices"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.id", ondelete='CASCADE'), nullable=False)
    city_code = Column(String, ForeignKey("cities.id"), nullable=False)
    price = Column(Integer, nullable=False)
    name = Column(String)

    service_id = Column(Integer, ForeignKey("repair_services.id"))

    product = relationship("Product", back_populates="prices")
    city = relationship("City")
    service = relationship("RepairService", backref="product_prices")
