from fastapi import APIRouter

grade_router = APIRouter()  # Instanciando como uma rota do FastAPI



@grade_router.get("/grade/{matricula}") # Consultar grade de horários do usuário
def obter_horarios_050():

    return
