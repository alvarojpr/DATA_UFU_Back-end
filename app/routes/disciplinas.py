from fastapi import APIRouter

disciplinas_router = APIRouter()  # Instanciando como uma rota do FastAPI


@disciplinas_router.get("/disciplina")  # Listar disciplinas disponíveis
def listar_disciplinas():

    return


# Matricular-se em disciplina
@disciplinas_router.post("/disciplina/matricular")
def matricular_em_disciplinas():

    return


# Remover disciplina da matrícula
@disciplinas_router.delete("/disciplina/remover")
def remover_disciplinas():

    return


@disciplinas_router.get("/disciplina/ementas")  # Obter ementas das disciplinas
def obter_ementas():

    return
