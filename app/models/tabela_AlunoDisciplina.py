from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base

class Model_AlunoDisciplina(Base):
    __tablename__ = "relacionamento_aluno_disciplina"

    matricula = Column(String, ForeignKey("aluno.matricula"), primary_key=True)
    disciplina_id = Column(Integer, ForeignKey("disciplina.id"), primary_key=True)

    aluno = relationship("Model_Aluno", back_populates="disciplinas")
    disciplina = relationship("Model_Disciplina", back_populates="alunos")
