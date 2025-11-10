# Usar imagem base leve do Python
FROM python:3.11-slim

# Definir diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo de dependências primeiro (para cache mais eficiente)
COPY requirements.txt .

# Instalar dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o restante do código
COPY . .

# Expor a porta usada pelo FastAPI
EXPOSE 8000

# Comando para iniciar o servidor FastAPI com Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

