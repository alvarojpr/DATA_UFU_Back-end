from fastapi import APIRouter

feedback_router = APIRouter()


@feedback_router.post("/feedback")  # usuario envia feedback
def enviar_feedback():

    return


@feedback_router.get("/feedback")  # administrador olha feedback
def consultar_feedbacks():

    return
