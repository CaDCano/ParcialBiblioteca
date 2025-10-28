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