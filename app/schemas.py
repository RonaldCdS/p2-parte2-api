from pydantic import BaseModel, Field
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1)
    descricao: Optional[str] = None
    preco: float = Field(..., gt=0)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True