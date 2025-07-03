from pydantic import BaseModel, ConfigDict, validator, constr
from datetime import datetime
from typing import Optional, Annotated, List
import phonenumbers
from pydantic import BaseModel, validator, Field
from sqlalchemy import Column, Integer, ForeignKey
from uuid import UUID, uuid4
from typing import Dict, List, Literal

CityCode = Literal['CHE', 'MGN', 'EKB']


class RepairRequestCreate(BaseModel):
	# name: str
	phone: str
	description: str
	city_id: int



# @validator("phone")
# def validate_phone(cls, value):
# 	try:
# 		parsed = phonenumbers.parse(value, "RU")
# 		if not phonenumbers.is_valid_number(parsed):
# 			raise ValueError()
# 	except Exception:
# 		raise ValueError("Некорректный номер телефона")
# 	return value


class RepairRequestTelegram(BaseModel):
	name: str
	phone: str
	city_id: int
	category_id: str
	product_id: str
	service_id: str
	description: str
	duration: str
	price: int


# @validator("phone")
# def validate_phone(cls, value):
# 	try:
# 		parsed = phonenumbers.parse(value, "RU")
# 		if not phonenumbers.is_valid_number(parsed):
# 			raise ValueError()
# 	except Exception:
# 		raise ValueError("Некорректный номер телефона")
# 	return value


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


# class ServiceCreate(BaseModel):
# 	name: str
# 	price: int
# 	city_id: int

class ServiceCreate(BaseModel):
	model: str
	url: str
	name: str
	price: Optional[int] = None
	description: str


class ServiceOut(ServiceCreate):
	id: int

	class Config:
		from_attributes = True


class AdminCreate(BaseModel):
	username: str
	password: str


class RepairRequestOut(BaseModel):
	id: int
	name: str
	phone: str
	description: str
	city_id: int
	status: Optional[str] = None
	accepted_at: Optional[datetime] = None

	model_config = {
		"from_attributes": True
	}


class Config:
	from_attributes = True


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
	price: Optional[int] = None
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
	price: Optional[int] = None
	category_id: str


class RepairRequestTelegram(BaseModel):
	product_id: str
	service_id: str
	name: str
	phone: str
	city_id: int
	description: str
	duration: str
	price: Optional[int] = None
	category_id: str


class RepairServiceCreate(RepairServiceBase):
	product_id: str


class RepairServiceRead(RepairServiceBase):
	pass


class RepairServiceCreate(BaseModel):
	id: int
	name: str
	service_id: str
	price: Optional[int] = None
	city_id: int
	description: str
	duration: str


class RepairService(BaseModel):
	id: str
	title: str
	description: str
	price: Dict[CityCode, int]
	duration: str
	warranty: str
	categoryId: str


class Product(BaseModel):
	id: str
	title: str
	slug: str
	categoryId: str
	description: str
	image: str
	repairServices: List[RepairService]


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
	price: Optional[int] = None
	description: str
	duration: str
	category_id: str


class ProductPriceSchema(BaseModel):
	product_id: str
	city_id: int
	price: Optional[int] = None


class ProductPriceOut(BaseModel):
	id: int
	name: str
	# product_id: str
	price: Optional[int] = None
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
	price: Optional[int] = None
	product_id: Optional[str]
	category_id: Optional[str]
	city_id: Optional[int]


class FeedbackBase(BaseModel):
	city_id: int
	phone: str
	description: str


class FeedbackCreate(FeedbackBase):
	pass


class FeedbackBase(BaseModel):
    city_id: int
    phone: str
    description: str

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackRead(FeedbackBase):
    id: int
    code: str
    city: str

    model_config = {
        "from_attributes": True
    }

    @validator("city", pre=True, always=True)
    def get_city_name(cls, v, values):
        # v — это объект City, если вы делаете .from_orm
        return v.name if hasattr(v, "name") else v