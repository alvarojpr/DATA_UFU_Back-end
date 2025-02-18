from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from database import Base
import bcrypt


class Model_Aluno(Base):
    __tablename__ = 'aluno'
    matricula = Column(String, primary_key=True, nullable=False)
    senha = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)

    @validates('senha')
    def hash_password(self, key, senha):
        # Gerar o salt e o hash da senha
        hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')  # Armazenar o hash como string

    def check_password(self, senha):
        # Verificar a senha
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha.encode('utf-8'))
