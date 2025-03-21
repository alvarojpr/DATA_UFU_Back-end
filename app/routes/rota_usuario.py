from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.models.tabela_usuario import Model_Aluno
from app.schemas.schema_usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
import bcrypt
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta

# Token de autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuario/login")

usuario_router = APIRouter()

SECRET_KEY = "mysecretkey"  # Altere isso para algo mais seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # O tempo que o token será válido

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
    
    hashed_senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 
    novo_usuario = Model_Aluno(
        matricula=usuario.matricula,
        nome=usuario.nome,
        email=usuario.email,
        senha=hashed_senha
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

# Rota de login (gera o token)
@usuario_router.post("/usuario/login")
def login(matricula: str, senha: str, db: Session = Depends(get_db)):
    usuario = db.query(Model_Aluno).filter_by(matricula=matricula).first()
    if not usuario or not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Criação do token JWT
    access_token = create_access_token(data={"sub": usuario.matricula})
    return {"access_token": access_token, "token_type": "bearer"}

# Rota para atualizar o perfil do usuário
@usuario_router.put("/usuario/{matricula}", response_model=UsuarioResponse)
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

# Rota para excluir a conta do usuário
@usuario_router.delete("/usuario/{matricula}")
def excluir_usuario(matricula: str, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    usuario = db.query(Model_Aluno).filter_by(matricula=matricula).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"detail": "Usuário excluído com sucesso"}
