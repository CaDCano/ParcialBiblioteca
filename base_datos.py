from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL_BASE_DATOS = "sqlite:///./biblioteca.db"

motor = create_engine(URL_BASE_DATOS, connect_args={"check_same_thread": False})
SesionLocal = sessionmaker(bind=motor, autoflush=False, autocommit=False)
Base = declarative_base()


def obtener_sesion_bd():
    bd = SesionLocal()
    try:
        yield bd
    finally:
        bd.close()
