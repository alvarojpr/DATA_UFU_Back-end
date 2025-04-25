from sqlalchemy import Column, String
from database import Base

class Model_Edital(Base):
    __tablename__ = 'edital'
    link = Column(String, primary_key=True, nullable=False)
    orgao_responsavel = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    data = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    num_edital = Column(String, nullable=False)
