from fastapi import APIRouter

grade_router = APIRouter()  # Instanciando como uma rota do FastAPI


# Consultar grade de horários do usuário
@grade_router.get("/grade/{matricula}")
def obter_horarios_050():

    return
