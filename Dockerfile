FROM python:3.11-slim

WORKDIR /app

# Injeta a raiz do container no caminho de busca do Python
ENV PYTHONPATH=/app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia absolutamente todos os arquivos locais (incluindo main.py) para o container
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]