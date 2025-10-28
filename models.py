from pydantic import BaseModel
from typing import List, Optional

class AutorBase(BaseModel):
    nombre: str
    pais: str
    anio_nacimiento: int

class AutorCreate(AutorBase):
    pass

class AutorOut(AutorBase):
    id: int
    class Config:
        orm_mode = True

class LibroBase(BaseModel):
    titulo: str
    genero: str
    anio_publicacion: int
    autor_id: int
    
class LibroCreate(LibroBase):
    pass

class LibroOut(LibroBase): 
    id: int
    autor: AutorOut
    class Config:
        orm_mode = True