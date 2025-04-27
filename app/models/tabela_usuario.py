from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates, relationship
from database import Base
import bcrypt

class Model_Aluno(Base):
    __tablename__ = 'aluno'

    matricula = Column(String, primary_key=True, nullable=False)
    senha = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    # Relacionamento com a tabela de associação (aluno_disciplina)
    disciplinas = relationship("Model_AlunoDisciplina", back_populates="aluno")

    # Relacionamento com Feedback
    feedbacks = relationship("Model_Feedback", back_populates="aluno", passive_deletes=True)


    def check_password(self, senha):
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha.encode('utf-8'))
    
