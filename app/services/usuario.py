from sqlalchemy.orm import Session
from models.usuario import Model_Aluno
from schemas.usuario import UsuarioCreate, UsuarioUpdate
import bcrypt

def get_usuario(db: Session, matricula: str):
    return db.query(Model_Aluno).filter(Model_Aluno.matricula == matricula).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
    hashed_senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_usuario = Model_Aluno(
        matricula=usuario.matricula,
        senha=hashed_senha,
        nome=usuario.nome,
        email=usuario.email
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, matricula: str, usuario: UsuarioUpdate):
    db_usuario = get_usuario(db, matricula)
    if not db_usuario:
        return None
    if usuario.nome:
        db_usuario.nome = usuario.nome
    if usuario.email:
        db_usuario.email = usuario.email
    if usuario.senha:
        db_usuario.senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, matricula: str):
    db_usuario = get_usuario(db, matricula)
    if not db_usuario:
        return None
    db.delete(db_usuario)
    db.commit()
    return db_usuario
