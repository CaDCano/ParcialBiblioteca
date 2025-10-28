from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .base_datos import Base

libro_autor = Table(
    "libro_autor",
    Base.metadata,
    Column("id_libro", Integer, ForeignKey("libros.id", ondelete="CASCADE"), primary_key=True),
    Column("id_autor", Integer, ForeignKey("autores.id", ondelete="CASCADE"), primary_key=True),
)

class AutorBD(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    pais = Column(String)
    anio_nacimiento = Column(Integer)

    libros = relationship("LibroBD", secondary=libro_autor, back_populates="autores")

class LibroBD(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    isbn = Column(String, nullable=False, unique=True, index=True)
    anio_publicacion = Column(Integer)
    copias_disponibles = Column(Integer, default=0)

    autores = relationship("AutorBD", secondary=libro_autor, back_populates="libros")
