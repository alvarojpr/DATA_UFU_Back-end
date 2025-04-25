# schemas definem e validam os dados que a api recebe.
from pydantic import BaseModel
from typing import Optional
from datetime import time

# 1. Definindo o modelo base para Disciplina
class DisciplinaBase(BaseModel):
    nome: str
    sala: str
    nome_prof: str
    dia_semana: str
    horario: str

# 2. Para criação de uma nova Disciplina, com cod_disciplina
class DisciplinaCreate(DisciplinaBase):
    nome: str

# 3. Para atualização de Disciplina, campos são opcionais
class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    sala: Optional[str] = None
    nome_prof: Optional[str] = None
    dia_semana: Optional[str] = None
    horario: Optional[str] = None


class DisciplinaResponse(DisciplinaBase):
    nome: str

    class Config:
        from_attributes = True  # Para que o Pydantic converta os objetos ORM diretamente


class GradeResponse(BaseModel):
    nome: str
    dia_semana: str
    horario: time