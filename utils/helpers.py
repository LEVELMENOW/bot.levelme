# utils/helpers.py

import os
import requests
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

# Variables de entorno
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CANVA_CLIENT_ID = os.getenv('CLIENT_ID')
CANVA_CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# ======================
# Función: Generar respuesta IA (OpenAI)
# ======================

def generar_respuesta_ia(prompt):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        respuesta = response.json()['choices'][0]['message']['content'].strip()
        return respuesta

    except Exception as e:
        print(f"⚠️ Error en OpenAI: {e}")
        return "⚠️ Hubo un error generando la respuesta de IA."


# ======================
# Función: Obtener token de Canva
# ======================

def obtener_token_canva():
    try:
        token_url = "https://oauth.canva.com/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': CANVA_CLIENT_ID,
            'client_secret': CANVA_CLIENT_SECRET,
            'scope': 'https://api.canva.com/auth/user.read https://api.canva.com/auth/designs.read'
        }

        response = requests.post(token_url, data=data)
        response.raise_for_status()
        token_info = response.json()
        access_token = token_info.get('access_token')
        print(f"✅ Token Canva obtenido correctamente: {access_token}")
        return access_token

    except Exception as e:
        print(f"❌ Error al obtener token Canva: {e}")
        return None


# ======================
# Función: Generar diseño en Canva (placeholder)
# ======================

def generar_diseno_canva(idea):
    # ⚠️ Importante: Canva API aún necesita autenticación completa.
    # Aquí dejamos la estructura para cuando conectemos la cuenta.

    token = obtener_token_canva()
    if not token:
        return "❌ No se pudo obtener el token de Canva."

    # Aquí iría el endpoint real de Canva para crear diseños (cuando terminemos la API)
    # Esto es un mockup de ejemplo:
    print(f"🎨 Generando diseño en Canva para: {idea}")
    return f"🖼️ Diseño generado para: {idea} (funcionalidad Canva lista para conectar 🚀)"


# ======================
# Función: Guardar idea generada en outputs
# ======================

def guardar_idea(idea):
    try:
        with open('logs/activity.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"{idea}\n")

        with open('outputs/ideas_generadas.txt', 'a', encoding='utf-8') as output_file:
            output_file.write(f"{idea}\n")

        print("✅ Idea guardada correctamente.")

    except Exception as e:
        print(f"⚠️ Error al guardar la idea: {e}")
