from fastapi import FastAPI
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
from app.services.obter_transportes import salvar_horarios_no_bd

from database import engine
from fastapi.middleware.cors import CORSMiddleware
from database import get_db

import threading
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


def atualiza_bd():
    db = next(get_db())
    print("##############################################################################################")
    print(f"Executando atualização do banco de dados em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    salvar_editais_no_bd(db)
    print("Editais Atualizados")
    salvar_disciplinas_no_bd(db)
    print("Disciplinas Atualizadas")
    salvar_fichas_no_bd(db)
    print("Fichas Atualizadas")
    salvar_horarios_no_bd(db, "municipal")
    print("Horarios Municipal Atualizados")
    salvar_horarios_no_bd(db, "intercampi")
    print("Horarios Intercampi Atualizados")
    print("##############################################################################################")
    
    print("Banco de dados atualizado.")

def rodar_agendamentos():
    while True:
        schedule.run_pending()
        time.sleep(30)

@app.on_event("startup")
def start_scheduler():
    horario_agendado = "05:00"
    atualiza_bd()
    schedule.every().friday.at(horario_agendado).do(lambda: threading.Thread(target=atualiza_bd).start())
    thread = threading.Thread(target=rodar_agendamentos, daemon=True)
    thread.start()





#####  BRANCHES  #####

# criar branch:
# git checkout -b alvaro 

# mudar de branch:
# git checkout alvaro 

# commitar branch:
# git add .
# git commit -m "sua mensagem"
# git push -u origin alvaro 

# agregar branch na main:
# git checkout main
# git pull origin main

# git checkout alvaro 
# git merge main

# deletar branch:
#  git branch -d alvaro           # LOCAL**
# git push origin --delete alvaro  # REMOTO**





# uvicorn app.main:app --reload --root-path server
# uvicorn main:app --reload # GERALMENTE É ESSE AQUI.

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
