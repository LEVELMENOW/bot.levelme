# bot/levelme.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.helpers import generar_respuesta_ia, generar_diseno_canva
from utils.db import get_db, registrar_usuario, guardar_idea, registrar_actividad

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
# Eventos del bot
# ====================

@bot.event
async def on_ready():
    print(f"✅ LevelME está online como {bot.user}")
    with next(get_db()) as db:
        registrar_actividad(db, "Bot iniciado", f"Usuario: {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    discord_id = str(message.author.id)
    nombre_usuario = str(message.author)

    with next(get_db()) as db:
        # Registro de usuario y actividad
        registrar_usuario(db, discord_id, nombre_usuario)
        registrar_actividad(db, "Mensaje recibido", f"De: {nombre_usuario} - Contenido: {message.content}")

        try:
            # Generar respuesta IA
            respuesta = generar_respuesta_ia(message.content)
            await message.channel.send(respuesta)

            # Guardar idea en base de datos
            guardar_idea(db, discord_id, respuesta)

            # Opcional: Canva mockup para ideas
            if "diseño" in message.content.lower():
                diseno = generar_diseno_canva(message.content)
                await message.channel.send(diseno)

            registrar_actividad(db, "Respuesta enviada", respuesta)

        except Exception as e:
            error_msg = f"⚠️ Error procesando el mensaje: {e}"
            await message.channel.send(error_msg)
            registrar_actividad(db, "Error", error_msg)

    await bot.process_commands(message)


# ====================
# Iniciar el bot
# ====================

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

