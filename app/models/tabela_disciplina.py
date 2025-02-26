from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Model_Disciplina(Base):
    __tablename__ = 'disciplina'
    # Corrigido para 'cod_disciplina'
    cod_disciplina = Column(String, primary_key=True, nullable=False)
    nome = Column(String, nullable=False)
    sala = Column(String, nullable=False)
    nome_prof = Column(String, nullable=False)
    periodo = Column(Integer, nullable=False)

    # Relacionamento
    dias_semana = relationship("Dias_da_Semana", back_populates="disciplina")


class Dias_da_Semana(Base):
    __tablename__ = 'dias_da_semana'
    id = Column(Integer, primary_key=True, autoincrement=True)
    horario = Column(Time, nullable=False)
    cod_disciplina = Column(String, ForeignKey(
        'disciplina.cod_disciplina'), nullable=False)  # Corrigido para 'cod_disciplina'
    dia = Column(String, nullable=False)

    # Relacionamento
    disciplina = relationship("Model_Disciplina", back_populates="dias_semana")
