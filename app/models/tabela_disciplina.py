from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# class Model_Disciplina(Base):
#     __tablename__ = 'disciplina'

#     dia_semana = Column(String, nullable=False)
#     horario = Column(String, nullable=False)
#     nome = Column(String, nullable=False)
#     sala = Column(String, nullable=False)
#     nome_prof = Column(String, nullable=False)

#     # Relacionamento com a tabela de associação (aluno_disciplina)
#     alunos = relationship("Model_AlunoDisciplina", back_populates="disciplina")

#     # Relacionamento com dias da semana (se necessário)
#     dias_semana = relationship("Dias_da_Semana", back_populates="disciplina")
    
class Model_Disciplina(Base):
    __tablename__ = 'disciplina'

    dia_semana = Column(String, nullable=False)
    nome = Column(String, primary_key=True, nullable=False)
    sala = Column(String, nullable=False)
    nome_prof = Column(String, nullable=False)
    horario = Column(String, nullable=False)

    # Relacionamento com a tabela de associação (aluno_disciplina)
    alunos = relationship("Model_AlunoDisciplina", back_populates="disciplina")