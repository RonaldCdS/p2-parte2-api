import pytest

# 1. Listar produtos quando o banco está vazio
def test_listar_produtos_banco_vazio(client):
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []

# 2. Criar produto e verificar persistência no banco
def test_criar_produto_verificar_persistencia(client):
    payload = {"nome": "Teclado", "preco": 150.0, "estoque": 10, "ativo": True}
    response = client.post("/produtos", json=payload)
    assert response.status_code == 201
    dados = response.json()
    assert dados["id"] is not None
    assert dados["nome"] == "Teclado"

# 3. Criar produto e verificar que aparece na listagem
def test_criar_produto_verificar_na_listagem(client):
    payload = {"nome": "Mouse", "preco": 80.0, "estoque": 5, "ativo": True}
    client.post("/produtos", json=payload)
    
    response = client.get("/produtos")
    lista = response.json()
    assert len(lista) == 1
    assert lista[0]["nome"] == "Mouse"

# 4. Buscar produto por id — caso de sucesso
def test_buscar_produto_por_id_sucesso(client, produto_existente):
    id_produto = produto_existente["id"]
    response = client.get(f"/produtos/{id_produto}")
    assert response.status_code == 200
    assert response.json()["nome"] == produto_existente["nome"]

# 5. Buscar produto com id inexistente — deve retornar 404
def test_buscar_produto_id_inexistente(client):
    response = client.get("/produtos/9999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]

# 6. Deletar produto — deve retornar 204
def test_deletar_produto_sucesso(client, produto_existente):
    id_produto = produto_existente["id"]
    response = client.delete(f"/produtos/{id_produto}")
    assert response.status_code == 204
    assert response.text == ""

# 7. Deletar produto e confirmar remoção com GET subsequente
def test_deletar_produto_e_confirmar_com_get(client, produto_existente):
    id_produto = produto_existente["id"]
    
    # Deleta
    del_response = client.delete(f"/produtos/{id_produto}")
    assert del_response.status_code == 204
    
    # Confirma sumiço
    get_response = client.get(f"/produtos/{id_produto}")
    assert get_response.status_code == 404

# 8. Deletar produto inexistente — deve retornar 404
def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/9999")
    assert response.status_code == 404

# 9. Teste parametrizado com @pytest.mark.parametrize cobrindo payloads inválidos (status 422)
@pytest.mark.parametrize(
    "payload_invalido",
    [
        {"nome": "", "preco": 10.0},          # Nome vazio
        {"nome": "Produto X", "preco": 0.0},  # Preço zero
        {"nome": "Produto Y", "preco": -5.0}, # Preço negativo
        {"preco": 20.0},                      # Falta nome
    ],
)
def test_payloads_invalidos(client, payload_invalido):
    response = client.post("/produtos", json=payload_invalido)
    assert response.status_code == 422

# 10. Teste que valide que o banco está isolado entre execuções
def test_validar_isolamento_banco(client):
    # Como a fixture limpa o banco antes de cada teste rodar,
    # este teste garante que a listagem começa estritamente zerada,
    # independente se os testes anteriores inseriram dados.
    response = client.get("/produtos")
    assert response.status_code == 200
    assert len(response.json()) == 0