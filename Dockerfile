# Usamos una imagen base de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos necesarios
COPY requirements.txt requirements.txt
COPY bot_levelme.py bot_levelme.py

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para correr el bot
CMD ["python", "bot_levelme.py"]
