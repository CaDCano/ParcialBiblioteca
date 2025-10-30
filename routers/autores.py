from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from base_datos import obtener_sesion_bd
from modelos import AutorBD, LibroBD
from esquemas import AutorCrear, AutorActualizar, AutorLeer, AutorConLibros, LibroLeer

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

@router.delete("/{id_autor}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_autor(
    id_autor: int,
    bd: Session = Depends(obtener_sesion_bd),
    forzar: bool = Query(False, description="Forzar eliminación del autor y libros huérfanos"),
):
    autor = bd.query(AutorBD).filter(AutorBD.id == id_autor).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    libros_huerfanos = []
    for libro in autor.libros:
        if len(libro.autores) == 1 and libro.copias_disponibles > 0:
            libros_huerfanos.append(libro)

    if libros_huerfanos and not forzar:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "No se puede eliminar el autor: algunos libros quedarían sin autores y tienen copias disponibles.",
                "libros_bloqueados": [
                    {"id": l.id, "titulo": l.titulo, "copias_disponibles": l.copias_disponibles}
                    for l in libros_huerfanos
                ],
            },
        )

    # Borrar relaciones y libros huérfanos
    for libro in list(autor.libros):
        libro.autores.remove(autor)
        if len(libro.autores) == 0:
            if forzar or libro.copias_disponibles == 0:
                bd.delete(libro)

    bd.delete(autor)
    bd.commit()
    return None
