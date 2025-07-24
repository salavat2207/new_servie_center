from datetime import datetime
from typing import Optional, Annotated, List, TypedDict, Literal

from pydantic import BaseModel, validator, Field

from typing import Dict, List, Literal

CityCode = Literal['CHE', 'MGN', 'EKB']


class PriceDict(TypedDict):
    CHE: int
    MGN: int
    EKB: int



class RepairRequestCreate(BaseModel):
    # name: str
    phone: str
    description: str
    city_id: int




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




class RepairRequestBase(BaseModel):
    name: str
    # phone: str
    description: str
    city_id: int

    # status: str
    # created_at: datetime

    class Config:
        orm_mode = True


class RepairRequestUpdate(BaseModel):
    status: str



class ServiceCreate(BaseModel):
    id: str
    model: Optional[str] = None
    # url: str
    title: str
    price: PriceDict
    description: str


class RepairPriceOut(BaseModel):
    id: int
    city_id: int
    price: int

    class Config:
        orm_mode = True

    class Config:
        orm_mode = True


class ServiceOut(BaseModel):
    # id: int
    service_id: Optional[str] = None
    title: str
    description: Optional[str]
    duration: Optional[str]
    warranty: Optional[str]
    # product_id: Optional[str]
    price: PriceDict

    class Config:
        orm_mode = True


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
        orm_mode = True


class ApplicationBase(BaseModel):
    name: str
    phone: str
    description: Optional[str] = None
    city_id: int





class ApplicationCreate(ApplicationBase):
    pass


class ApplicationOut(ApplicationBase):
    id: int
    code: str

    class Config:
        orm_mode = True


class ProductsCreate(BaseModel):
    id: str
    name: str
    category_id: str
    description: str
    price: Optional[int] = None
    city_id: int


class ProductUpdate(BaseModel):
    id: Optional[str]
    title: Optional[str]
    name: Optional[str]
    link: Optional[str]
    category_id: Optional[str]
    description: Optional[str]
    image: Optional[str]


class ServicePriceOut(BaseModel):
    city_code: str
    price: int

    class Config:
        orm_mode = True


class RepairServiceBase(BaseModel):
    # id: str
    name: str
    description: str
    duration: str
    price: List[ServicePriceOut]
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



class RepairServiceRead(RepairServiceBase):
    pass


class RepairServiceCreate(BaseModel):
    title: str
    service_id: str
    description: Optional[str] = None
    duration: Optional[str] = None
    warranty: Optional[str] = None
    product_id: str
    price: PriceDict



class RepairService(BaseModel):
    id: str
    title: str
    description: str
    price: PriceDict
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


class ProductOut(BaseModel):
    id: str
    # name: str
    title: Optional[str]
    slug: Optional[str]
    # link: Optional[str]
    category_id: Optional[int]
    description: Optional[str]
    image: Optional[str]
    city_id: Optional[int]
    price: Optional[int]
    duration: Optional[str]
    category_id: Optional[str] = None
    city_id: Optional[int] = None
    price: Optional[float] = None
    duration: Optional[int] = None

    class Config:
        orm_mode = True



class ProductBase(BaseModel):
    id: str
    title: str
    slug: str
    category_id: str = Field(..., alias="categoryId")
    description: str
    image: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ProductCreate(ProductBase):
    repair_services: List[RepairServiceCreate]


class ProductRead(ProductBase):
    repair_services: List[RepairServiceRead]


class ProductCreate(BaseModel):
    id: str
    # name: str
    title: str
    slug: Optional[str] = None
    # link: Optional[str]
    categoryId: str
    description: Optional[str]
    image: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

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
    title: Optional[str]
    model: str
    city_code: str
    duration: str
    warranty: str


class ProductPriceSchema(BaseModel):
    product_id: str
    city_id: int
    price: Optional[int] = None


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


class ProductWithPricesOut(BaseModel):
    id: str
    title: str
    slug: str
    categoryId: str
    description: str
    image: str
    prices: List[ProductPriceOut]
    city_code: Optional[str] = None

    class Config:
        orm_mode = True


class ProductCreateSchema(BaseModel):
    id: str
    title: str
    link: Optional[str]
    category_id: str
    description: str
    image: str
    prices: List[ProductPriceSchema]



class SubItems(BaseModel):
    id: str
    title: str
    slug: str
    image: Optional[str]
    categoryId: str

    class Config:
        orm_mode = True




class SubItem(BaseModel):
    id: str
    title: str
    slug: str
    image: str
    categoryId: str


class MenuItem(BaseModel):
    title: str
    slug: str
    subitems: List[SubItems]

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True

    @validator("city", pre=True, always=True)
    def get_city_name(cls, v, values):
        # v — это объект City, если вы делаете .from_orm
        return v.name if hasattr(v, "name") else v


class CategoryBase(BaseModel):
    name: str
    brand: str


class CategoryCreate(CategoryBase):
    id: str  # обязательный
    name: str
    brand: str


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class ServiceBase(BaseModel):
    # name: str
    description: Optional[str] = None
    duration: Optional[str] = None  # в минутах


class ServiceCreate(ServiceBase):
    # price: int
    city_id: int


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[float] = None
    city_id: Optional[int] = None

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str
    brand: str


class CategoryUpdate(BaseModel):
    id: str
    name: Optional[str] = None
    brand: Optional[str] = None


class CategoryOut(BaseModel):
    id: str
    name: Optional[str] = None
    image: Optional[str] = None
    brand: Optional[str] = None

    class Config:
        orm_mode = True





class RepairServiceResponse(BaseModel):
    service_id: str
    title: str
    description: str
    duration: str
    warranty: str
    price: PriceDict


class ProductWithServicesResponse(BaseModel):
    id: str
    title: str
    slug: str
    categoryId: str
    description: str
    image: Optional[str] = None
    repairServices: List[RepairServiceResponse]
