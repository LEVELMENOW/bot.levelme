# db.py profesional para PostgreSQL Railway

from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import os

# ============================
# Configuración de conexión
# ============================
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:pWOwHDZorUEHfKOEyOuAwGmXmYOfkxQJ@turntable.proxy.rlwy.net:40781/railway")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================
# Modelos de base de datos
# ============================

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    fecha_registro = Column(TIMESTAMP(timezone=True), server_default=func.now())

    ideas = relationship("Idea", back_populates="usuario")
    tokens = relationship("CanvaToken", back_populates="usuario")


class Idea(Base):
    __tablename__ = 'ideas'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    idea = Column(Text, nullable=False)
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="ideas")


class Actividad(Base):
    __tablename__ = 'actividad'

    id = Column(Integer, primary_key=True, index=True)
    accion = Column(String, nullable=False)
    detalles = Column(Text)
    fecha = Column(TIMESTAMP(timezone=True), server_default=func.now())


class CanvaToken(Base):
    __tablename__ = 'canva_tokens'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    expires_at = Column(TIMESTAMP(timezone=True))

    usuario = relationship("Usuario", back_populates="tokens")


# ============================
# Funciones auxiliares
# ============================

def init_db():
    Base.metadata.create_all(bind=engine)
    print("\u2705 Base de datos inicializada correctamente en Railway.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================
# Funciones operativas
# ============================

def registrar_usuario(db, discord_id, nombre):
    from sqlalchemy.exc import IntegrityError
    nuevo_usuario = Usuario(discord_id=discord_id, nombre=nombre)
    try:
        db.add(nuevo_usuario)
        db.commit()
        print(f"\u2705 Usuario registrado: {nombre} ({discord_id})")
    except IntegrityError:
        db.rollback()
        print(f"⚠️ Usuario ya existente: {discord_id}")


def guardar_idea(db, discord_id, idea_text):
    usuario = db.query(Usuario).filter(Usuario.discord_id == discord_id).first()
    if usuario:
        nueva_idea = Idea(usuario_id=usuario.id, idea=idea_text)
        db.add(nueva_idea)
        db.commit()
        print(f"\u2705 Idea guardada para el usuario {discord_id}.")
    else:
        print(f"⚠️ Usuario {discord_id} no encontrado.")


def registrar_actividad(db, accion, detalles=""):
    nueva_actividad = Actividad(accion=accion, detalles=detalles)
    db.add(nueva_actividad)
    db.commit()
    print(f"📝 Actividad registrada: {accion}")


# Ejecuta la creación de tablas si se llama directamente
if __name__ == "__main__":
    init_db()
