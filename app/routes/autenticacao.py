from fastapi import APIRouter

autenticacao_router = APIRouter()  # Instanciando como uma rota do FastAPI


@autenticacao_router.post("/auth/login")
def login():

    return


@autenticacao_router.post("/auth/logout")
def lgout():

    return


@autenticacao_router.post("/auth/refresh")
def refresh():

    return
