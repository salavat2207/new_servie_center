from sqlalchemy import Column, Integer, String, ForeignKey,Text, Enum, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


"""
Город сервисного центра
"""
class City(Base):
	__tablename__ = 'cities'
	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True)
	phone = Column(String)
	adress = Column(String)
	masters = relationship("Master", back_populates="city")
	requests = relationship("RepairRequest", back_populates="city")
	code = Column(String(3), unique=True, nullable=False)


"""
Запрос на ремонт
"""
class RepairRequest(Base):
	__tablename__ = 'requests'
	id = Column(Integer, primary_key=True)
	city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
	phone = Column(String, nullable=False)
	description = Column(String, nullable=False)
	request_number = Column(String, unique=True, index=True)
	# name = Column(String, default='Новая заявка')

	city = relationship("City", back_populates="requests")

class Service(Base):
	__tablename__ = 'services'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	price = Column(Integer)
	city_id = Column(Integer, ForeignKey('cities.id'))


"""
Заявки на ремонт
"""
# class RepairRequest(Base):
# 	__tablename__ = 'requests'
# 	id = Column(Integer, primary_key=True)
# 	name = Column(String)
# 	phone = Column(Text)
# 	description = Column(Text)
# 	city_id = Column(Integer, ForeignKey('cities.id'))
# 	status = Column(String, default='Новая заявка')


"""
Мастер
"""
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
	name = Column(String, nullable=False)
	phone = Column(String, nullable=False)
	message = Column(String, nullable=False)



"""
Админ
"""
# class Admin(Base):
# 	__tablename__ = 'admin'
# 	id = Column(Integer, primary_key=True, index=True)
# 	name = Column(String, nullable=False)
# 	phone = Column(String)
# 	# telegram_id = Column(Integer)
# 	telegram_id = 908977119




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


class Category(Base):
	__tablename__ = 'categories'
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, index=True)










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
	#
	code = Column(String, unique=True, index=True)

	city = relationship("City")



class Product(Base):
	__tablename__ = "products"
	id = Column(String, primary_key=True)
	title = Column(String, unique=True, index=True)
	link = Column(String, index=True)
	category_id = Column(Integer, ForeignKey("categories.id"))
	description = Column(String, nullable=True)
	image = Column(String)

	repair_services = relationship("RepairService", back_populates="product")
	prices = relationship("ProductPrice", back_populates="product")




"""
Модель ProductPrice, которая будет связывать Product и City с конкретной ценой
"""
class ProductPrice(Base):
	__tablename__ = "product_prices"
	id = Column(Integer, primary_key=True, index=True)
	product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
	city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
	price = Column(Integer, nullable=False)

	product = relationship("Product", back_populates="prices")
	city = relationship("City")


class RepairService(Base):
	__tablename__ = "repair_services"
	id = Column(String,primary_key=True, nullable=True)
	city = Column(String)
	name = Column(String, nullable=False)
	description = Column(String, nullable=False)
	duration = Column(String, nullable=False)
	price = Column(Integer, nullable=False)
	category_id = Column(String, ForeignKey("categories.id"))
	product_id = Column(String, ForeignKey("products.id"))

	product = relationship("Product", back_populates="repair_services")




