from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..base_datos import obtener_sesion_bd
from ..modelos import AutorBD, LibroBD
from ..esquemas import AutorCrear, AutorActualizar, AutorLeer, AutorConLibros, LibroLeer

router = APIRouter(prefix="/autores", tags=["Autores"])

