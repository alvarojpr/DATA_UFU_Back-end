from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base

class Model_AlunoDisciplina(Base):
    __tablename__ = 'aluno_disciplina'
    matricula = Column(String, ForeignKey('aluno.matricula'), primary_key=True)
    cod_disciplina = Column(String, ForeignKey('disciplina.cod_disciplina'), primary_key=True)

    aluno = relationship("Model_Aluno", back_populates="disciplinas")
    disciplina = relationship("Model_Disciplina", back_populates="alunos")

class Model_Aluno(Base):
    __tablename__ = 'aluno'
    matricula = Column(String, primary_key=True, nullable=False)
    senha = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)

    disciplinas = relationship("Model_AlunoDisciplina", back_populates="aluno")


class Model_Disciplina(Base):
    __tablename__ = 'disciplina'
    cod_disciplina = Column(String, primary_key=True, nullable=False)
    nome = Column(String, nullable=False)
    sala = Column(String, nullable=False)
    nome_prof = Column(String, nullable=False)
    periodo = Column(Integer, nullable=False)

    dias_semana = relationship("Dias_da_Semana", back_populates="disciplina")
    alunos = relationship("Model_AlunoDisciplina", back_populates="disciplina")
