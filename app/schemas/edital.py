from pydantic import BaseModel
from typing import Optional


# 1. Modelo Base para Edital
class EditalBase(BaseModel):
    orgao_responsavel: str
    titulo: str
    data: str
    tipo: str
    num_edital: int

# 2. Para criação de um Edital, inclui o link (que é o campo chave primária)


class EditalCreate(EditalBase):
    link: str

# 3. Para atualização de Edital, campos são opcionais


class EditalUpdate(BaseModel):
    orgao_responsavel: Optional[str] = None
    titulo: Optional[str] = None
    data: Optional[str] = None
    tipo: Optional[str] = None
    num_edital: Optional[int] = None

# 4. Para a resposta do Edital, incluindo o link como campo de retorno


class EditalResponse(EditalBase):
    link: str  # Campo chave primária

    class Config:
        orm_mode = True  # Para que o Pydantic converta os objetos ORM diretamente
