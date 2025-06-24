from pydantic import BaseModel, ConfigDict, validator
from datetime import datetime
from typing import Optional, Annotated, List
import phonenumbers
from pydantic import BaseModel, validator, Field
from sqlalchemy import Column, Integer, ForeignKey


class RepairRequestCreate(BaseModel):
	# name: str
	phone: str
	description: str
	city_id: int

	@validator("phone")
	def validate_phone(cls, value):
		try:
			parsed = phonenumbers.parse(value, "RU")
			if not phonenumbers.is_valid_number(parsed):
				raise ValueError()
		except Exception:
			raise ValueError("Некорректный номер телефона")
		return value


class RepairRequestTelegram(BaseModel):
	product_id: str
	service_id: str
	name: str
	phone: str
	city_id: int
	description: str
	duration: str
	price: int
	category_id: str

	@validator("phone")
	def validate_phone(cls, value):
		try:
			parsed = phonenumbers.parse(value, "RU")
			if not phonenumbers.is_valid_number(parsed):
				raise ValueError()
		except Exception:
			raise ValueError("Некорректный номер телефона")
		return value


class RepairRequestBase(BaseModel):
	name: str
	# phone: str
	description: str
	city_id: int
	# status: str
	# created_at: datetime

	model_config = {
		"from_attributes": True
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

	model_config = {
		"from_attributes": True
	}


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

	model_config = {
		"from_attributes": True
	}


class ProductsCreate(BaseModel):
	id: str
	name: str
	category_id: str
	description: str
	price: int
	city_id: int


class ProductUpdate(BaseModel):
	id: Optional[int]
	title: Optional[str]
	name: Optional[str]
	link: Optional[str]
	category_id: Optional[int]
	description: Optional[str]
	image: Optional[str]


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
	description: str
	duration: str
	price: int
	category_id: str


class RepairServiceCreate(RepairServiceBase):
	product_id: str


class RepairServiceRead(RepairServiceBase):
	pass


class RepairServiceCreate(BaseModel):
	id: int
	name: str
	service_id: str
	price: int
	city_id: int
	description: str
	duration: str


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
	product_id: str
	service_id: str
	name: str
	city_id: int
	price: int
	description: str
	duration: str
	category_id: str


class ProductPriceSchema(BaseModel):
	product_id: str
	city_id: int
	price: int


class ProductPriceOut(BaseModel):
	id: int
	name: str
	# product_id: str
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

	model_config = {
		"from_attributes": True
	}


class ProductCreateSchema(BaseModel):
	id: str
	title: str
	link: str
	category_id: str
	description: str
	image: str
	prices: List[ProductPriceSchema]


class AdminLoginSchema(BaseModel):
	username: str
	password: str


class TokenSchema(BaseModel):
	access_token: str
	token_type: str


class RepairServicePatch(BaseModel):
	name: Optional[str]
	description: Optional[str]
	duration: Optional[str]
	price: Optional[int]
	product_id: Optional[str]
	category_id: Optional[str]
	city_id: Optional[int]
