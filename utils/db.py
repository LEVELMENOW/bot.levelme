# utils/db.py

import sqlite3

# ======================
# Conexión inicial
# ======================

def conectar_db():
    try:
        conn = sqlite3.connect('levelme.db')
        print("✅ Base de datos conectada.")
        return conn
    except sqlite3.Error as e:
        print(f"⚠️ Error al conectar la base de datos: {e}")
        return None


# ======================
# Crear tablas iniciales
# ======================

def crear_tablas():
    conn = conectar_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id TEXT UNIQUE,
                nombre TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabla de ideas generadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                idea TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabla de actividad del bot
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS actividad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                accion TEXT,
                detalles TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        print("✅ Tablas creadas correctamente.")

    except sqlite3.Error as e:
        print(f"⚠️ Error al crear tablas: {e}")

    finally:
        conn.close()


# ======================
# Funciones de inserción
# ======================

def registrar_usuario(discord_id, nombre):
    conn = conectar_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO usuarios (discord_id, nombre) VALUES (?, ?)', (discord_id, nombre))
        conn.commit()
        print(f"✅ Usuario registrado: {nombre} ({discord_id})")
    except sqlite3.Error as e:
        print(f"⚠️ Error al registrar usuario: {e}")
    finally:
        conn.close()


def guardar_idea(discord_id, idea):
    conn = conectar_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # Obtener el id del usuario
        cursor.execute('SELECT id FROM usuarios WHERE discord_id = ?', (discord_id,))
        usuario = cursor.fetchone()

        if usuario:
            usuario_id = usuario[0]
            cursor.execute('INSERT INTO ideas (usuario_id, idea) VALUES (?, ?)', (usuario_id, idea))
            conn.commit()
            print(f"✅ Idea guardada en la base de datos para el usuario {discord_id}.")
        else:
            print(f"⚠️ Usuario {discord_id} no encontrado en la base de datos.")

    except sqlite3.Error as e:
        print(f"⚠️ Error al guardar la idea: {e}")
    finally:
        conn.close()


def registrar_actividad(accion, detalles=""):
    conn = conectar_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO actividad (accion, detalles) VALUES (?, ?)', (accion, detalles))
        conn.commit()
        print(f"📝 Actividad registrada: {accion}")
    except sqlite3.Error as e:
        print(f"⚠️ Error al registrar actividad: {e}")
    finally:
        conn.close()
