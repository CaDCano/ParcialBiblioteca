from fastapi import FastAPI
from base_datos import Base, motor
from modelos import *
from routers import autores_router, libros_router

Base.metadata.create_all(bind=motor)

app = FastAPI(title="Catálogo Biblioteca")

app.include_router(autores_router)
app.include_router(libros_router)
