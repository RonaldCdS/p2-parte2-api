import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. IMPORTAÇÕES DA NOVA ESTRUTURA (Com o prefixo app)
from app.main import app, get_db
from app.models import Base, ProdutoModel

# 2. CONFIGURAÇÃO DO BANCO DE DADOS DE TESTE (CONEXÃO INTERNA DOCKER)
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password@db_test:5432/ecom_test"
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. FIXTURE DE ISOLAMENTO DO BANCO (EXECUTA A CADA FUNÇÃO DE TESTE)
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """
    Garante o isolamento limpando e recriando todas as tabelas
    antes de cada cenário de teste rodar.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# 4. FIXTURE DA SESSÃO DO BANCO DE DADOS
@pytest.fixture(scope="function")
def db_session():
    """
    Fornece uma sessão ativa do banco de dados de teste
    para validações diretas dentro dos asserts.
    """
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# 5. FIXTURE DO CLIENTE HTTP (INJEÇÃO DE DEPENDÊNCIA)
@pytest.fixture(scope="function")
def client():
    """
    Configura o TestClient do FastAPI substituindo a sessão local
    pela sessão isolada do banco de testes.
    """
    def _get_db_override():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = _get_db_override
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()

# 6. FIXTURE DE SUPORTE: PRODUTO EXISTENTE (Ajustado para app.models)
@pytest.fixture(scope="function")
def produto_existente():
    """
    Cria um produto diretamente no banco antes do teste rodar
    para cenários de busca por ID e deleção.
    """
    session = TestingSessionLocal()
    novo_produto = ProdutoModel(
        nome="Produto Teste",
        descricao="Descricao do teste",
        preco=99.90
    )
    session.add(novo_produto)
    session.commit()
    session.refresh(novo_produto)
    
    produto_dict = {
        "id": novo_produto.id,
        "nome": novo_produto.nome,
        "descricao": novo_produto.descricao,
        "preco": novo_produto.preco
    }
    session.close()
    return produto_dict