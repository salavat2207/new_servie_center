from sqlalchemy import Column, Integer, String, ForeignKey,Text, Enum
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

class Service(Base):
	__tablename__ = 'services'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	price = Column(Integer)
	city_id = Column(Integer, ForeignKey('cities.id'))


"""
Заявки на ремонт
"""
class RepairRequest(Base):
	__tablename__ = 'requests'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	phone = Column(Text)
	description = Column(Text)
	city_id = Column(Integer, ForeignKey('cities.id'))
	status = Column(String, default='Новая заявка')


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
class Admin(Base):
	__tablename__ = 'admin'
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	phone = Column(String)
	# telegram_id = Column(Integer)
	telegram_id = 908977119