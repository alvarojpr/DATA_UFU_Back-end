from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Model_Transporte(Base):
    __tablename__ = 'transporte'
    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String, nullable=False) # intercampi ou municipal

    # Relacionamento: Um transporte pode ter vários pontos
    pontos = relationship("Model_Pontos", back_populates="transporte")


class Model_Pontos(Base):
    __tablename__ = 'pontos'
    id = Column(Integer, primary_key=True, nullable=False)
    ponto = Column(String, nullable=False)

    # Chave estrangeira para 'transporte'
    transporte_id = Column(Integer, ForeignKey(
        'transporte.id'), nullable=False)

    # Relacionamento: Um ponto pode ter vários horários
    horarios = relationship("Model_Horarios", back_populates="ponto")

    # Relacionamento bidirecional
    transporte = relationship("Model_Transporte", back_populates="pontos")


class Model_Horarios(Base):
    __tablename__ = 'horarios'
    id = Column(Integer, primary_key=True, nullable=False)
    horario = Column(String, nullable=False)

    # Chave estrangeira para 'pontos'
    ponto_id = Column(Integer, ForeignKey('pontos.id'), nullable=False)

    # Relacionamento bidirecional
    ponto = relationship("Model_Pontos", back_populates="horarios")
