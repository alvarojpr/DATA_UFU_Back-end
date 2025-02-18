from fastapi import APIRouter

disciplinas_router = APIRouter()  # Instanciando como uma rota do FastAPI


@disciplinas_router.get("/disciplina")  # y Listar disciplinas disponíveis
def obter_horarios_050():

    return


# Matricular-se em disciplina
@disciplinas_router.get("/disciplina/matricular")
def obter_horarios_050():

    return


# Remover disciplina da matrícula
@disciplinas_router.get("/disciplina/remover")
def obter_horarios_050():

    return


@disciplinas_router.get("/disciplina/ementas")  # Obter ementas das disciplinas
def obter_horarios_050():

    return
