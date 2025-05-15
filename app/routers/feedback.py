from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import SessionLocal
from app.models import Feedback as FeedbackModel
from app.schemas import FeedbackCreate

router = APIRouter(prefix='/feedback')


@router.post('/обратная связь')
def create_feedback(feedback: FeedbackCreate):
	db = SessionLocal()
	db_feedback = FeedbackModel(**feedback.dict())
	db.add(db_feedback)
	db.commit()
	db.refresh(db_feedback)
	db.close()
	return {"message": "Заявка успешно создана"}
