# levelme.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.helpers import generar_respuesta_ia, guardar_idea, generar_diseno_canva
from utils.db import crear_tablas, registrar_usuario, guardar_idea as guardar_idea_db, registrar_actividad

# ====================
# Cargar variables de entorno
# ====================

load_dotenv(dotenv_path='config/.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# ====================
# Inicialización del bot
# ====================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ====================
# Crear tablas en la base de datos al iniciar
# ====================

crear_tablas()

# ====================
# Eventos del bot
# ====================

@bot.event
async def on_ready():
    print(f"✅ LevelME está online como {bot.user}")
    registrar_actividad("Bot iniciado", f"Usuario: {bot.user}")

@bot.event
async def on_message(message):
    # Evitamos que el bot se responda a sí mismo
    if message.author == bot.user:
        return

    # Registrar usuario en la base de datos
    discord_id = str(message.author.id)
    nombre_usuario = str(message.author)

    registrar_usuario(discord_id, nombre_usuario)
    registrar_actividad("Mensaje recibido", f"De: {nombre_usuario} - Contenido: {message.content}")

    # Procesar el mensaje como conversación natural
    try:
        respuesta = generar_respuesta_ia(message.content)
        await message.channel.send(respuesta)

        # Guardar la idea local y en base de datos
        guardar_idea(respuesta)
        guardar_idea_db(discord_id, respuesta)

        # Extra opcional: Canva mockup para ideas
        if "diseño" in message.content.lower():
            diseno = generar_diseno_canva(message.content)
            await message.channel.send(diseno)

        registrar_actividad("Respuesta enviada", respuesta)

    except Exception as e:
        error_msg = f"⚠️ Error procesando el mensaje: {e}"
        await message.channel.send(error_msg)
        registrar_actividad("Error", error_msg)

    # Permitimos que comandos sigan funcionando si decides usar comandos adicionales
    await bot.process_commands(message)

# ====================
# Iniciar el bot
# ====================

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
