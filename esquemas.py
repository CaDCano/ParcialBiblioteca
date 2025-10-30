from typing import List, Optional
from pydantic import BaseModel, constr, conint, Field


# --- Esquemas de Autor ---
class AutorCrear(BaseModel):
    nombre: constr(min_length=1)
    pais: Optional[str] = None
    anio_nacimiento: Optional[int] = None


class AutorActualizar(BaseModel):
    nombre: Optional[constr(min_length=1)] = None
    pais: Optional[str] = None
    anio_nacimiento: Optional[int] = None


class AutorLeer(BaseModel):
    id: int
    nombre: str
    pais: Optional[str]
    anio_nacimiento: Optional[int]

    class Config:
        from_attributes = True


# --- Esquemas de Libro ---
class LibroCrear(BaseModel):
    titulo: constr(min_length=1)
    isbn: constr(min_length=1)
    anio_publicacion: Optional[int] = None
    copias_disponibles: conint(ge=0) = 0
    id_autores: List[int] = Field(..., min_items=1)


class LibroActualizar(BaseModel):
    titulo: Optional[constr(min_length=1)] = None
    isbn: Optional[constr(min_length=1)] = None
    anio_publicacion: Optional[int] = None
    copias_disponibles: Optional[conint(ge=0)] = None
    id_autores: Optional[List[int]] = None


class LibroLeer(BaseModel):
    id: int
    titulo: str
    isbn: str
    anio_publicacion: Optional[int]
    copias_disponibles: int

    class Config:
        from_attributes = True



# --- Esquemas anidados ---
class LibroConAutores(LibroLeer):
    autores: List[AutorLeer]

class AutorConLibros(AutorLeer):
    libros: List[LibroLeer]
