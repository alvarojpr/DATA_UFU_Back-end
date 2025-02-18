from fastapi import APIRouter

editais_router = APIRouter()  # Instanciando como uma rota do FastAPI


@editais_router.get("/editais")
def editais():

    return
