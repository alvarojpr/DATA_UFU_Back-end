from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.schema_usuario import UsuarioCreate, UsuarioUpdate
from app.services.service_usuario import get_usuario, create_usuario, update_usuario, delete_usuario

usuario_router = APIRouter()

@usuario_router.post("/usuario")
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if get_usuario(db, usuario.matricula):
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return create_usuario(db, usuario)

@usuario_router.get("/usuario/{matricula}")
def consultar_usuario(matricula: str, db: Session = Depends(get_db)):
    usuario = get_usuario(db, matricula)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@usuario_router.put("/usuario/{matricula}")
def atualizar_perfil(matricula: str, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario_atualizado = update_usuario(db, matricula, usuario)
    if not usuario_atualizado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario_atualizado

@usuario_router.delete("/usuario/{matricula}")
def excluir_usuario(matricula: str, db: Session = Depends(get_db)):
    usuario_excluido = delete_usuario(db, matricula)
    if not usuario_excluido:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario_excluido
