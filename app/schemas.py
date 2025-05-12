from pydantic import BaseModel

class RepairRequestCreate(BaseModel):
	name: str | None
	phone: str
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