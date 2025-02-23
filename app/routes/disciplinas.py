from fastapi import APIRouter

disciplinas_router = APIRouter()  # Instanciando como uma rota do FastAPI


@disciplinas_router.get("/disciplina")  # Listar disciplinas disponíveis
def listar_disciplinas():

    return



@disciplinas_router.post("/disciplina/matricular") # Matricular-se em disciplina
def matricular_em_disciplinas():

    return



@disciplinas_router.delete("/disciplina/remover") # Remover disciplina da matrícula
def remover_disciplinas():

    return


@disciplinas_router.get("/disciplina/ementas")  # Obter ementas das disciplinas
def obter_ementas():

    return
