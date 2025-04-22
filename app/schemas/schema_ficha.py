from pydantic import BaseModel


# 1. Modelo Base para Edital
class FichaBase(BaseModel):
    codigo: str
    periodo: str
    disciplina: str
    link: str