# Imagen base oficial de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos todos los archivos del proyecto al contenedor
COPY . /app

# Instalamos las dependencias del proyecto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Creamos carpeta para logs por si acaso no existe
RUN mkdir -p logs outputs config utils bot

# Exponemos el puerto por si lo necesita
EXPOSE 8080

# Comando para ejecutar el bot
CMD ["python", "bot/levelme.py"]
