import requests
import os
from dotenv import load_dotenv
import requests

load_dotenv()  # Carga las variables del .env

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


# Endpoint para obtener el token de acceso
TOKEN_URL = "https://oauth.canva.com/token"

# Datos para la solicitud del token
data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'https://api.canva.com/auth/user.read https://api.canva.com/auth/designs.read'
}

def obtener_token():
    try:
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        token_info = response.json()
        access_token = token_info.get('access_token')
        print(f"\n✅ Token obtenido correctamente: {access_token}\n")
        return access_token
    except requests.RequestException as e:
        print(f"\n❌ Error al obtener el token: {e}\n")
        return None

if __name__ == "__main__":
    obtener_token()
