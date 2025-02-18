from fastapi import FastAPI
from app.models import disciplina, edital, feedback, transporte, usuario
from app.routes.autenticacao import autenticacao_router
from app.routes.disciplinas import disciplinas_router
from app.routes.feedback import feedback_router
from app.routes.grade import grade_router
from app.routes.transporte import transporte_router
from app.routes.usuario import usuario_router
from database import engine
from fastapi.middleware.cors import CORSMiddleware

# criando as tabelas
disciplina.Base.metadata.create_all(bind=engine)
edital.Base.metadata.create_all(bind=engine)
feedback.Base.metadata.create_all(bind=engine)
transporte.Base.metadata.create_all(bind=engine)
usuario.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Incluindo as rotas da pasta app/routes
app.include_router(autenticacao_router)
app.include_router(disciplinas_router)
app.include_router(feedback_router)
app.include_router(grade_router)
app.include_router(transporte_router)
app.include_router(usuario_router)


# uvicorn app.main:app --reload --root-path server
# uvicorn main:app --reload

# ATUALIZAR
# git fetch origin
# git pull origin main

# SUBIR MUDANÇAS
# git add .                 git add requirements.txt
# git commit -m "mensagem"
# git push origin main

# GERAR E INSATALAR requirements.txt
# pip freeze > requirements.txt
# pip install -r requirements.txt
