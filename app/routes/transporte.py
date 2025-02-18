from fastapi import APIRouter

transporte_router = APIRouter()  # Instanciando como uma rota do FastAPI


@transporte_router.get("/transporte/publico")
def obter_horarios_050():

    return


@transporte_router.get("/transporte/intercampi")
def obter_horarios_intercampi():

    return
