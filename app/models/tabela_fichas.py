from sqlalchemy import Column, String
from database import Base

class Model_Fichas(Base):
    __tablename__ = 'fichas'

    codigo = Column(String, primary_key=True, nullable=False)
    periodo = Column(String, nullable=False)
    disciplina = Column(String, nullable=False)
    link = Column(String, nullable=False)
