# Dockerfile profesional para LevelME Bot

# Imagen base oficial de Python optimizada
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto al contenedor
COPY . /app

# Instalar dependencias del sistema para compilación
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Actualizar pip e instalar dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Crear carpetas necesarias por si no existen
RUN mkdir -p logs outputs config utils bot

# Variables de entorno (buenas prácticas)
ENV PYTHONUNBUFFERED=1

# Exponer puerto si decides poner API REST futuro (preparado)
EXPOSE 8080

# Comando para ejecutar el bot directamente
CMD ["python", "bot/levelme.py"]
