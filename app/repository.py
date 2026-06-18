from sqlalchemy.orm import Session
from app.models import ProdutoModel
from app.schemas import ProdutoCreate

class ProdutoRepository:
    @staticmethod
    def listar(db: Session):
        return db.query(ProdutoModel).all()

    @staticmethod
    def buscar_por_id(db: Session, produto_id: int):
        return db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()

    @staticmethod
    def criar(db: Session, produto: ProdutoCreate):
        db_produto = ProdutoModel(**produto.model_dump())
        db.add(db_produto)
        db.commit()
        db.refresh(db_produto)
        return db_produto

    @staticmethod
    def deletar(db: Session, produto_id: int):
        db_produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
        if db_produto:
            db.delete(db_produto)
            db.commit()
            return True
        return False