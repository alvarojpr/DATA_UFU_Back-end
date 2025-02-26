from sqlalchemy.orm import Session
from . import models, schemas


def criar_feedback(db: Session, feedback: schemas.FeedbackCreate):
    novo_feedback = models.Model_Feedback(**feedback.dict())
    db.add(novo_feedback)
    db.commit()
    db.refresh(novo_feedback)
    return novo_feedback


def listar_feedbacks(db: Session):
    return db.query(models.Model_Feedback).all()
