from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import SessionLocal
from app.models import Feedback as FeedbackModel


router = APIRouter(prefix='/feedback')

class FeedbackCreate(BaseModel):
	name: str
	phone: str
	message: str

@router.post('/')
def create_feedback(feedback: FeedbackCreate):
	db = SessionLocal()
	db_feedback = FeedbackModel(**feedback.dict())
	db.add(db_feedback)
	db.commit()
	db.refresh(db_feedback)
	db.close()
	return {"message": "Обратная связь получена"}
