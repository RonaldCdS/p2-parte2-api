# 🛒 E-Commerce API — Arquitetura em Camadas (FastAPI)

API RESTful para gerenciamento de produtos desenvolvida com **FastAPI**, **SQLAlchemy** (PostgreSQL) e **Pytest**. O projeto foi reestruturado do zero utilizando padrões de mercado para garantir alta manutenibilidade e testes isolados.

---

## 🏗️ Arquitetura do Projeto (Repository Pattern)

A aplicação utiliza uma **Arquitetura em Camadas** para separar responsabilidades e blindar as regras de negócio:

* **`app/main.py`**: Gerencia apenas as rotas (endpoints) e a injeção de dependências.
* **`app/models.py`**: Define a estrutura das tabelas do banco de dados (SQLAlchemy).
* **`app/schemas.py`**: Valida os dados de entrada e saída (Pydantic), impedindo preços negativos ou nomes vazios.
* **`app/repository.py`**: Centraliza todas as queries SQL (CRUD), isolando a lógica de banco das rotas.

### Estrutura de Arquivos
```text
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── repository.py
├── exemplo.py/tests/
│   ├── __init__.py
│   └── test__produtos.py   # 13 Cenários de testes automatizados
├── conftest.py             # Fixtures e configuração do banco de testes
├── Dockerfile
└── docker-compose.yml

🧪 Estratégia de Testes & Isolamento
A API possui 13 testes automatizados cobrindo fluxos de sucesso (CRUD), tratamento de erros (404) e payloads inválidos (422).

Banco Dedicado: Os testes rodam em um banco de dados PostgreSQL exclusivo (ecom_test), totalmente separado do ambiente de desenvolvimento.

Isolamento Total: Através do conftest.py, o banco de testes é limpo e recriado do zero antes de cada teste rodar, garantindo que um cenário nunca interfira no outro.

🚀 Como Rodar os Testes (Docker)
Toda a aplicação está conteinerizada. Para buildar e executar a suíte de testes com um único comando, rode no terminal:

Bash
# Build limpo e execução dos testes
docker compose build --no-cache app_tests && docker compose up app_tests
