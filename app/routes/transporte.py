from fastapi import APIRouter

transporte_router = APIRouter()  # Instanciando como uma rota do FastAPI


@transporte_router.get("/transporte/publico")  # mostrar os horarios do 050
def obter_horarios_050():

    return



@transporte_router.get("/transporte/intercampi") # mostrar os horarios do intercampi
def obter_horarios_intercampi():

    return
