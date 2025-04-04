from fastapi import FastAPI
from app.models import tabela_disciplina, tabela_editais, tabela_feedback, tabela_transporte, tabela_usuario
from app.routes.rota_disciplinas_e_grade import disciplina_router
from app.routes.rota_feedback import feedback_router
from app.routes.rota_transporte import transporte_router
from app.routes.rota_usuario import usuario_router
from app.routes.rota_editais import router_editais
from database import engine
from fastapi.middleware.cors import CORSMiddleware

# criando/abrindo as tabelas
tabela_disciplina.Base.metadata.create_all(bind=engine)
tabela_editais.Base.metadata.create_all(bind=engine)
tabela_feedback.Base.metadata.create_all(bind=engine)
tabela_transporte.Base.metadata.create_all(bind=engine)
tabela_usuario.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:5173'
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*']
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para teste, mas depois use domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo as rotas da pasta app/routes
app.include_router(disciplina_router)
app.include_router(feedback_router)
app.include_router(transporte_router)
app.include_router(usuario_router)
app.include_router(router_editais)

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
