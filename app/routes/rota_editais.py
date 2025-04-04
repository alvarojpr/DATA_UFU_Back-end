from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.obter_editais import obter_editais_com_cache

router_editais = APIRouter()

@router_editais.get("/editais")
def listar_editais(db: Session = Depends(get_db)):
    return obter_editais_com_cache(db)

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from database import get_db
# from app.models.tabela_editais import Model_Edital
# from app.schemas.schema_edital import EditalCreate, EditalUpdate, EditalResponse
# from app.services.service_editais import get_edital, create_edital, update_edital, delete_edital

#  editais_router = APIRouter()  # Instanciando como uma rota do FastAPI


# @editais_router.get("/editais", response_model=list[EditalResponse])
# def listar_editais(db: Session = Depends(get_db)):
#     return db.query(Model_Edital).all()
    
# @app.get("/editais")
# async def retorna_webscraping(
#     db: Session = Depends(get_db),
#     org: Optional[str] = None,
#     tipo: Optional[str] = None
# ):
#     query = db.query(model.Model_Editais)

#     if org:
#         org_lista = org.split(",")
#         query = query.filter(model.Model_Editais.orgaoresponsavel.in(org_lista))

#     if tipo:
#         tipo_lista = tipo.split(",")
#         query = query.filter(model.ModelEditais.tipo.in(tipo_lista))

#     editais = query.all()

#     if not editais:
#         return {"Mensagem": "Nenhum edital encontrado com os filtros fornecidos"}

#     return editais