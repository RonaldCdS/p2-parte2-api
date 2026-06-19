Markdown
# 🛒 E-Commerce API — Arquitetura em Camadas & Repository Pattern

Esta é uma API RESTful para gerenciamento de produtos de um e-commerce, desenvolvida com **FastAPI** e **SQLAlchemy**. O projeto foi estruturado seguindo rigorosamente as melhores práticas de engenharia de software do mercado, utilizando separação de conceitos (*Separation of Concerns*), validação estrita de dados e testes automatizados isolados via **Docker**.

---

## 🏗️ Arquitetura e Padrões de Projeto

O projeto foi migrado de um modelo monolítico de arquivo único para uma **Arquitetura em Camadas**, implementando o **Repository Pattern**. Isso isola a lógica de negócios da persistência de dados e garante uma aplicação testável, sustentável e altamente escalável.

### Estrutura de Diretórios
text
'''P2_part_1_back/
├── app/                  # Núcleo da aplicação
│   ├── main.py           # Maestro das rotas (FastAPI) e Injeção de Dependências
│   ├── models.py         # Camada de Dados: Mapeamento ORM (SQLAlchemy)
│   ├── schemas.py        # Camada de Validação: Contratos de Entrada/Saída (Pydantic)
│   └── repository.py     # Camada de Persistência: Padrão Repository (Queries SQL)
├── exemplo.py/           # Módulo dedicado aos Testes Automatizados
│   └── tests/
│       ├── __init__.py
│       └── test__produtos.py
├── conftest.py           # Configurações globais e Fixtures isoladas do Pytest
├── Dockerfile            # Blueprint de build do container Python
└── docker-compose.yml    # Orquestração do App de Testes e Bancos PostgreSQL
Detalhes das Camadas
Rotas (main.py): Atua estritamente como um controlador. Não executa queries SQL diretamente e delega toda a responsabilidade de banco para o repositório.

Modelos (models.py): Define exclusivamente o esquema físico do banco de dados relacional.

Schemas (schemas.py): Blindagem da API usando Pydantic. Valida tipos de dados, regras de negócio (como tamanho mínimo de string e preços estritamente positivos) e mascara a saída escondendo dados sensíveis.

Repositório (repository.py): Centraliza todas as operações CRUD. Facilita futuras manutenções ou substituições de tecnologias de banco de dados sem impactar as rotas da API.

🧪 Estratégia de Testes e Isolamento Estrito
A suíte de testes conta com 13 cenários automatizados cobrindo fluxos de sucesso, falhas de validação (regras do Pydantic) e rotas inexistentes.

Isolamento de Infraestrutura: Utilização de um banco de dados PostgreSQL exclusivo para testes (ecom_test), rodando em um container Docker separado do banco de desenvolvimento (ecom_dev).

Isolamento entre Execuções: Através de fixtures do Pytest no arquivo conftest.py, o banco de testes é completamente limpo e recriado do zero antes de cada função de teste ser executada (Base.metadata.drop_all e create_all). Isso impede o vazamento de estado e garante que nenhum teste dependa do resultado do outro.

🚀 Como Executar o Projeto e os Testes
Toda a infraestrutura está conteinerizada, eliminando a necessidade de instalar Python, PostgreSQL ou dependências localmente na máquina hospedeira.

Pré-requisitos
Docker e Docker Compose instalados.

Executando a Suíte de Testes
Para construir a imagem do ambiente de testes do zero e rodar os 13 cenários validados, execute os comandos abaixo no terminal da raiz do projeto:

PowerShell
# Build limpo ignorando o cache do Docker
docker compose build --no-cache app_tests

# Inicialização dos bancos e execução automatizada do Pytest
docker compose up app_tests
Ao finalizar, o container de testes aplicará os asserts e retornará o código de saída esperado (code 0), comprovando a estabilidade da API estruturada.
