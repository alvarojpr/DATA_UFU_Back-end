from fastapi import APIRouter

usuario_router = APIRouter()  # Instanciando como uma rota do FastAPI


@usuario_router.post("/usuario")  # criar um usuário
def criar_usuario():

    return


@usuario_router.get("/usuario/{matricula}")  # consultar perfil do usuario
def consultar_usuario():

    return


@usuario_router.put("/usuario/{matricula}")  # atualizar perfil do usuario
def atualizar_perfil():

    return


@usuario_router.get("/usuario/{matricula}")  # excluir usuário
def excluir_usuário():

    return
