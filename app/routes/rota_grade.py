from fastapi import APIRouter

grade_router = APIRouter()  # Instanciando como uma rota do FastAPI

grade_router.post("/grade/adicionar") #Adiciona uma disciplina à grade do aluno.
def adicionar_disciplina():
    return


grade_router.delete("/grade/remover") #Remove uma disciplina da grade do aluno.
def remover_disciplina():
    return


grade_router.get("/grade/minha") #Retorna a grade horária do aluno autenticado.
def get_grade():
    return