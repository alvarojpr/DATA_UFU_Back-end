from fastapi import FastAPI, Depends, status
from app.models import tabela_disciplina, tabela_editais, tabela_feedback, tabela_fichas, tabela_transporte, tabela_usuario
from app.routes.rota_disciplinas_e_grade import disciplina_router
from app.routes.rota_feedback import feedback_router
from app.routes.rota_transporte import transporte_router
from app.routes.rota_usuario import usuario_router
from app.routes.rota_editais import router_editais
from app.routes.rota_fichas import router_fichas

from app.services.obter_disciplinas import salvar_disciplinas_no_bd
from app.services.obter_editais import salvar_editais_no_bd
from app.services.obter_fichas import salvar_fichas_no_bd
from app.services.obter_transporte_050 import preview_050_com_cache
from app.services.obter_transporte_Intercampi import preview_intercampi_com_cache

from database import engine
from fastapi.middleware.cors import CORSMiddleware
from app import models
from database import get_db

import threading
import asyncio
import time
import schedule
from datetime import datetime

# criando/abrindo as tabelas
tabela_disciplina.Base.metadata.create_all(bind=engine)
tabela_editais.Base.metadata.create_all(bind=engine)
tabela_feedback.Base.metadata.create_all(bind=engine)
tabela_transporte.Base.metadata.create_all(bind=engine)
tabela_usuario.Base.metadata.create_all(bind=engine)
tabela_fichas.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    'http://localhost:5173'
]

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
app.include_router(router_fichas)


async def atualiza_bd():
    db = next(get_db())
    print(f"Executando atualização do banco de dados em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if (salvar_editais_no_bd(db)):
        print("Editais Atualizados")
    if salvar_disciplinas_no_bd(db):
        print("Disciplinas Atualizadas")
    if salvar_fichas_no_bd(db):
        print("Fichas Atualizadas")
    if preview_intercampi_com_cache(db):
        print("Horarios Intercampi Atualizados")
    print("Banco de dados atualizado.")

def executa_atualizacao():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(atualiza_bd())


threading.Thread(target=executa_atualizacao).start()
horario_agendado = "05:00"
schedule.every().monday.at(horario_agendado).do(lambda: threading.Thread(target=executa_atualizacao).start())

def rodar_agendamentos():
    while True:
        schedule.run_pending()
        time.sleep(60)

@app.on_event("startup")
def start_scheduler():
    thread = threading.Thread(target=rodar_agendamentos, daemon=True)
    thread.start()

















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
