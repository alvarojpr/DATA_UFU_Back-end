from fastapi import APIRouter

feedback_router = APIRouter()


@feedback_router.post("/feedback")
def enviar_feedback():

    return


@feedback_router.get("/feedback")
def consultar_feedbacks():

    return
