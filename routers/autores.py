from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..base_datos import obtener_sesion_bd
from ..modelos import AutorBD, LibroBD
from ..esquemas import AutorCrear, AutorActualizar, AutorLeer, AutorConLibros, LibroLeer

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.post("", response_model=AutorLeer, status_code=status.HTTP_201_CREATED)
def crear_autor(datos: AutorCrear, bd: Session = Depends(obtener_sesion_bd)):
    autor = AutorBD(**datos.dict())
    bd.add(autor)
    bd.commit()
    bd.refresh(autor)
    return autor


@router.get("", response_model=List[AutorLeer])
def listar_autores(pais: Optional[str] = Query(None), bd: Session = Depends(obtener_sesion_bd)):
    consulta = bd.query(AutorBD)
    if pais:
        consulta = consulta.filter(AutorBD.pais == pais)
    return consulta.all()


@router.get("/{id_autor}", response_model=AutorConLibros)
def obtener_autor(id_autor: int, bd: Session = Depends(obtener_sesion_bd)):
    autor = bd.query(AutorBD).filter(AutorBD.id == id_autor).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    resultado = AutorConLibros.from_orm(autor)
    resultado.libros = [LibroLeer.from_orm(l) for l in autor.libros]
    return resultado


@router.put("/{id_autor}", response_model=AutorLeer)
def actualizar_autor(id_autor: int, datos: AutorActualizar, bd: Session = Depends(obtener_sesion_bd)):
    autor = bd.query(AutorBD).filter(AutorBD.id == id_autor).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(autor, campo, valor)

    bd.commit()
    bd.refresh(autor)
    return autor
