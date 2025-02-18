from fastapi import APIRouter

usuario_router = APIRouter()  # Instanciando como uma rota do FastAPI


@usuario_router.post("/usuario")
def criar_usuario():

    return


@usuario_router.get("/usuario/{matricula}")
def criar_usuario():

    return


@usuario_router.get("/usuario/{matricula}")
def atualizar_perfil():

    return


@usuario_router.get("/usuario/{matricula}")
def excluir_usuário():

    return
