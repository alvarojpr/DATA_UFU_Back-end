from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from database import Base
from .usuario import Model_Aluno  # Importando o modelo correto


class Model_Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, nullable=False)
    data = Column(Date, nullable=False, default=text(
        "CURRENT_DATE"))  # Define a data automaticamente
    matricula_aluno = Column(String, ForeignKey(
        'aluno.matricula'), nullable=False)
    texto = Column(String, nullable=False)

    # Relacionamento com Model_Aluno
    # Corrigido para 'Model_Aluno'
    aluno = relationship("Model_Aluno", back_populates="feedbacks")


class Model_Aluno(Base):
    __tablename__ = 'aluno'

    matricula = Column(String, primary_key=True, nullable=False)
    nome = Column(String, nullable=False)

    # Relacionamento de volta para feedbacks
    # Relacionamento de volta
    feedbacks = relationship("Model_Feedback", back_populates="aluno")
