from sqlalchemy import Column, Integer, String, ForeignKey,Text, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class City(Base):
	__tablename__ = 'cities'
	id = Column(Integer, primary_key=True)
	name = Column(String, unique=True)
	phone = Column(String)
	adress = Column(String)

class Service(Base):
	__tablename__ = 'services'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	price = Column(Integer)
	city_id = Column(Integer, ForeignKey('cities.id'))

class RepairRequest(Base):
	__tablename__ = 'requests'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	phone = Column(Text)
	description = Column(Text)
	city_id = Column(Integer, ForeignKey('cities.id'))
	status = Column(String, default='Новая заявка')

class Master(Base):
	__tablename__ = 'masters'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	city_id = Column(Integer, ForeignKey('cities.id'))
	telegramm_id = Column(Integer)

class Feedback(Base):
	__tablename__ = 'feedbacks'
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	phone = Column(String, nullable=False)
	message = Column(String, nullable=False)


class Admin(Base):
	__tablename__ = 'admin'
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	phone = Column(String)
	telegram_id = Column(Integer)