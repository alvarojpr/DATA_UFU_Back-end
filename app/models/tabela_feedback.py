from sqlalchemy import Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from database import Base


class Model_Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, nullable=False)
    data = Column(Date, nullable=False, default=func.current_date())
    matricula_aluno = Column(String, ForeignKey('aluno.matricula'), nullable=False)
    texto = Column(String, nullable=False)

    # Relacionamento com Model_Aluno
    aluno = relationship("Model_Aluno", back_populates="feedbacks")
