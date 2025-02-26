from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):  # UsuarioBase herda BaseModel
    matricula: str
    nome: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):  # UsuarioCreate herda UsuarioBase
    senha: str

# optional é que talvez o usuário não queira alterar tudo, apenas 1 dos campos


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None

# define como os dados do usuário serão retornados.


class UsuarioResponse(UsuarioBase):  # UsuarioResponse herda UsuarioBase
    matricula: str

    # converte objetos ORM (database) diretamente para o schema Pydantic
    class Config:
        from_attributes = True
