from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
    
class Model_Disciplina(Base):
    __tablename__ = 'disciplina'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # chave primária nova
    nome_disciplina = Column(String, nullable=False)  # agora pode ter nomes repetidos
    sala = Column(String, nullable=False)
    nome_prof = Column(String, nullable=False)
    dia_semana = Column(String, nullable=False)
    horario = Column(String, nullable=False)
    alunos = relationship("Model_AlunoDisciplina", back_populates="disciplina")
