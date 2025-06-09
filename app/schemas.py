from pydantic import BaseModel, ConfigDict, validator
from datetime import datetime
from typing import Optional, Annotated, List

from sqlalchemy import Column


class RepairRequestCreate(BaseModel):
	# name: str
	phone: int
	description: str
	city_id: int


class RepairRequestBase(BaseModel):
	name: str
	# phone: str
	description: str
	city_id: int
	# status: str
	# created_at: datetime

	model_config = {
		"from_attributes": True  # В pydantic v2 вместо orm_mode
	}


class RepairRequestUpdate(BaseModel):
	status: str


class ServiceCreate(BaseModel):
	name: str
	price: int
	city_id: int


class AdminCreate(BaseModel):
	username: str
	password: str


class RepairRequestOut(BaseModel):
	id: int
	name: str
	phone: str
	description: str
	city_id: int


class Config:
	orm_mode = True


# orm_mode = ConfigDict(from_attributes=True)


class CityCreate(BaseModel):
	# id = int
	name: str
	address: str
	phone: str


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
		from_attributes = True


class ApplicationBase(BaseModel):
	name: str
	phone: str
	description: Optional[str] = None
	city_id: int


# code: str


class ApplicationCreate(ApplicationBase):
	pass


class ApplicationOut(ApplicationBase):
	id: int
	code: str

	class Config:
		from_attributes = True


class ProductsCreate(BaseModel):
	id: str
	name: str
	category_id: str
	description: str
	price: int
	city_id: int


class RepairServiceBase(BaseModel):
	id: str
	name: str
	description: str
	duration: str
	price: float
	category_id: str


class RepairRequestTelegram(BaseModel):
	product_id: str
	service_id: str
	name: str
	phone: str
	city_id: int


class RepairServiceCreate(RepairServiceBase):
	product_id: str


class RepairServiceRead(RepairServiceBase):
	pass


class ProductBase(BaseModel):
	id: str
	title: str
	link: str
	category_id: str
	description: str
	image: str


class ProductCreate(ProductBase):
	repair_services: List[RepairServiceCreate]


class ProductRead(ProductBase):
	repair_services: List[RepairServiceRead]


class ProductCreate(BaseModel):
	id: str
	name: str
	title: str
	link: Optional[str]
	category_id: str
	description: Optional[str]
	image: Optional[str]


class ProductPriceCreate(BaseModel):
	id: int
	name: str
	city_id: int
	price: int
	description: str
	duration: str


class ProductPriceSchema(BaseModel):
	product_id: str
	city_id: int
	price: int


class ProductPriceOut(BaseModel):
	id: int
	name: str
	price: int
	city_id: int
	description: str
	duration: str

	@validator("city_id", pre=True)
	def parse_city_id(cls, v):
		try:
			return int(v)
		except (TypeError, ValueError):
			raise ValueError(f"Invalid city_id value: {v}")

	class Config:
		orm_mode = True


class ProductCreateSchema(BaseModel):
	id: str
	title: str
	link: str
	category_id: int
	description: str
	image: str
	prices: List[ProductPriceSchema]


class AdminLoginSchema(BaseModel):
	username: str
	password: str


class TokenSchema(BaseModel):
	access_token: str
	token_type: str
