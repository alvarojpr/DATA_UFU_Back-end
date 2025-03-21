from pydantic import BaseModel
from typing import Optional
from datetime import date


# 1. Modelo Base para Feedback
class FeedbackBase(BaseModel):
    matricula_aluno: str
    texto: str
    # Data é opcional e será preenchida automaticamente, caso não seja informada
    data: Optional[date] = None

# 2. Para criação de Feedback, inclui o campo obrigatório de matrícula


class FeedbackCreate(FeedbackBase):
    pass  # Herda todos os campos de FeedbackBase, sem modificações

# 3. Para atualização de Feedback, todos os campos são opcionais


class FeedbackUpdate(BaseModel):
    matricula_aluno: Optional[str] = None
    texto: Optional[str] = None
    data: Optional[date] = None

# 4. Para a resposta de Feedback, inclui o ID e matrícula do aluno


class FeedbackResponse(FeedbackBase):
    id: int
    matricula_aluno: str
    texto: str
    data: date

    class Config:
        from_attributes = True  # Permite que o Pydantic converta objetos ORM diretamente
