# schemas definem e validam os dados que a api recebe.
from pydantic import BaseModel
from typing import List, Optional
from datetime import time

# 1. Definindo o modelo base para Disciplina


class DisciplinaBase(BaseModel):
    nome: str
    sala: str
    nome_prof: str
    periodo: int

# 2. Para criação de uma nova Disciplina, com cod_disciplina


class DisciplinaCreate(DisciplinaBase):
    cod_disciplina: str

# 3. Para atualização de Disciplina, campos são opcionais


class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    sala: Optional[str] = None
    nome_prof: Optional[str] = None
    periodo: Optional[int] = None

# 4. Para resposta (quando retornar os dados da disciplina), inclui dias_da_semana


class DiasDaSemanaBase(BaseModel):
    horario: time
    dia: str


class DisciplinaResponse(DisciplinaBase):
    cod_disciplina: str
    dias_semana: List[DiasDaSemanaBase]  # Relacionamento com os dias da semana

    class Config:
        orm_mode = True  # Para que o Pydantic converta os objetos ORM diretamente

# 5. Para dias da semana, para quando retornado separadamente


class DiasDaSemanaResponse(BaseModel):
    id: int
    horario: time
    dia: str
    cod_disciplina: str

    class Config:
        orm_mode = True
