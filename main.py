from fastapi import FastAPI
from .base_datos import Base, motor
from .routers import autores, libros

# Crear las tablas
Base.metadata.create_all(bind=motor)

app = FastAPI(title="Catálogo de Libros y Autores")