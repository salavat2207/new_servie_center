from pydantic import BaseModel
from datetime import datetime
from typing import Annotated

from sqlalchemy import Column


class RepairRequestCreate(BaseModel):
		name: str
		phone: int
		description: str
		city_id: int




class RepairRequestUpdate(BaseModel):
	status: str

class ServiceCreate(BaseModel):
	name: str
	price: int
	city_id: int

class AdminCreate(BaseModel):
	name: str
	phone: str
	telegram_id: int

class RepairRequestOut(BaseModel):
	id: int
	name: str
	phone: str
	description: str
	city_id: int

class Config:
	orm_mode = True

class CityCreate(BaseModel):
    name: str


class MasterCreate(BaseModel):
	name: str
	phone: str
	telegram_id: int
	city_id: int


class FeedbackCreate(BaseModel):
	name: str
	phone: str
	message: str


class MasterCreate(BaseModel):
	name: str
	telegram_id: int
	city_id: int

class MasterOut(BaseModel):
	id: int
	name: str
	telegram_id: int
	city_id: int

	class Config:
		orm_mode = True