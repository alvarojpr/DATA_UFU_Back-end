from fastapi import FastAPI
import model
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

model.Base.metadata.create_all(bind=engine)

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

# Incluindo as rotas da pasta routes_n_functions
app.include_router(upload_router)
app.include_router(category_router)
app.include_router(truncade_router)


# uvicorn app.main:app --reload --root-path server

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
