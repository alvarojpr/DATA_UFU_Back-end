from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.tabela_usuario import Model_Aluno
from app.schemas.schema_usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, LoginRequest
import bcrypt
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
import random
import string
from dotenv import load_dotenv
import os

# Token de autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuario/login")

usuario_router = APIRouter()

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env') # caminho para  o .env
load_dotenv(dotenv_path) # carrega as variáveis de ambiente

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
print(SECRET_KEY,"\n",ALGORITHM,"\n",ACCESS_TOKEN_EXPIRE_MINUTES,"\n")

# Função para criar o token JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta # datetime.datetime.now(datetime.UTC)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar o token JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Token inválido ou expirado")

# Rota de criação de usuário
@usuario_router.post("/usuario/criar", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Model_Aluno).filter_by(matricula=usuario.matricula).first():
        raise HTTPException(status_code=400, detail="Matrícula já cadastrada")
    
    # Gera o hash da senha
    hashed_senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt())
    
    # Decodifica o hash para uma string antes de armazenar
    hashed_senha_str = hashed_senha.decode('utf-8')
 
    # Cria o usuário
    novo_usuario = Model_Aluno(
        matricula=usuario.matricula,
        nome=usuario.nome,
        email=usuario.email,
        senha=hashed_senha_str  # Armazena o hash como string
    )
   # print("senha antes de salvar no banco:", novo_usuario.senha)

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario



# Rota de login (gera o token)
@usuario_router.post("/usuario/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Model_Aluno).filter_by(matricula=login_request.matricula).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Verifica a senha digitada com o hash salvo no banco
    if not bcrypt.checkpw(login_request.senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        print("Senha digitada:", login_request.senha.encode('utf-8'))
        print("Hash salvo:", usuario.senha.encode('utf-8'))
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Criação do token JWT
    #access_token = create_access_token(data={"sub": usuario.matricula})
    #return {"access_token": access_token, "token_type": "bearer"}
    access_token = create_access_token(data={"sub": usuario.matricula})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "matricula": usuario.matricula,
            "nome": usuario.nome,
            "email": usuario.email,
        }
    }



# Rota para atualizar o perfil do usuário
@usuario_router.put("/usuario/update/{matricula}", response_model=UsuarioResponse)
def atualizar_perfil(matricula: str, usuario: UsuarioUpdate, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    usuario_db = db.query(Model_Aluno).filter_by(matricula=matricula).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario.nome:
        usuario_db.nome = usuario.nome
    if usuario.email:
        usuario_db.email = usuario.email
    if usuario.senha:
        usuario_db.senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

#botão "sair" nao funciona.

# Rota para excluir a conta do usuário
@usuario_router.delete("/usuario/deletar/{matricula}")
def excluir_usuario(matricula: str, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    usuario = db.query(Model_Aluno).filter_by(matricula=matricula).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"detail": "Usuário excluído com sucesso"}

###################################### RECUPERAÇÃO DE SENHA #############################################

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Função para enviar o e-mail com a nova senha
def enviar_email(email_destino: str, nova_senha: str):
    #lembrar de colocar no .env
    remetente = os.getenv("remetente")
    senha_email = os.getenv("senha_email")
    smtp_server = os.getenv("smtp_server")
    smtp_port = os.getenv("smtp_port")
    # Cria a mensagem
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = email_destino
    mensagem["Subject"] = "Recuperação de Senha"
    corpo_email = f"Sua nova senha é: {nova_senha}. Por favor, altere-a após o login."
    mensagem.attach(MIMEText(corpo_email, "plain"))
    # Envia o e-mail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha_email)
            servidor.sendmail(remetente, email_destino, mensagem.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar o e-mail: {str(e)}")

@usuario_router.post("/usuario/recuperar")
def recuperar_senha(matricula: str, db: Session = Depends(get_db)):
    usuario = db.query(Model_Aluno).filter_by(matricula=matricula).first()
    print(matricula)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    nova_senha = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    hashed_nova_senha = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    usuario.senha = hashed_nova_senha
    db.commit()
    db.refresh(usuario)
    # Envia o e-mail com a nova senha
    enviar_email(usuario.email, nova_senha)
    return {"detail": "Senha redefinida com sucesso. Verifique seu e-mail para a nova senha."}

