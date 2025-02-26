from pydantic import BaseModel
from typing import List, Optional


# 1. Modelo Base para Transporte
class TransporteBase(BaseModel):
    nome: str

# 2. Modelo de Criação para Transporte


class TransporteCreate(TransporteBase):
    pass  # Herda de TransporteBase

# 3. Para a Resposta de Transporte (retornando ID e relacionamentos)


class TransporteResponse(TransporteBase):
    id: int
    pontos: List[str]  # Lista de pontos associados

    class Config:
        orm_mode = True  # Permite que o Pydantic converta objetos ORM diretamente


class TransporteUpdate(TransporteBase):
    nome: Optional[str] = None
    sala: Optional[str] = None
    nome_prof: Optional[str] = None
    periodo: Optional[int] = None


# 4. Modelo Base para Ponto
class PontoBase(BaseModel):
    ponto: str
    transporte_id: int  # Relacionamento com Transporte

# 5. Modelo de Criação para Ponto


class PontoCreate(PontoBase):
    pass  # Herda de PontoBase

# 6. Para a Resposta de Ponto


class PontoResponse(PontoBase):
    id: int
    horarios: List[str]  # Lista de horários associados ao ponto

    class Config:
        orm_mode = True  # Permite que o Pydantic converta objetos ORM diretamente


# 7. Modelo Base para Horário
class HorarioBase(BaseModel):
    horario: str
    ponto_id: int  # Relacionamento com Ponto

# 8. Modelo de Criação para Horário


class HorarioCreate(HorarioBase):
    pass  # Herda de HorarioBase

# 9. Para a Resposta de Horário


class HorarioResponse(HorarioBase):
    id: int

    class Config:
        orm_mode = True  # Permite que o Pydantic converta objetos ORM diretamente
