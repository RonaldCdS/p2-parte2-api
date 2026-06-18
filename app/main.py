import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from app.models import Base
from app.schemas import ProdutoCreate, ProdutoResponse
from app.repository import ProdutoRepository

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db_dev:5432/ecom_dev")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API - Camadas Profissionais")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return ProdutoRepository.listar(db)

@app.get("/produtos/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = ProdutoRepository.buscar_por_id(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.post("/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return ProdutoRepository.criar(db, produto)

@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    sucesso = ProdutoRepository.deletar(db, produto_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
