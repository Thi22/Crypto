# Etapa base
FROM python:3.11-slim AS base

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt  

# Exponer el puerto 8000
EXPOSE 8000 

# Comando por defecto
CMD ["python", "app.py"]
