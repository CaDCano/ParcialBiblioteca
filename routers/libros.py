from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..base_datos import obtener_sesion_bd
from ..modelos import LibroBD, AutorBD
from ..esquemas import LibroCrear, LibroActualizar, LibroLeer, LibroConAutores, AutorLeer

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post("", response_model=LibroConAutores, status_code=status.HTTP_201_CREATED)
def crear_libro(datos: LibroCrear, bd: Session = Depends(obtener_sesion_bd)):
    if bd.query(LibroBD).filter(LibroBD.isbn == datos.isbn).first():
        raise HTTPException(status_code=400, detail="El ISBN ya existe")

    autores = bd.query(AutorBD).filter(AutorBD.id.in_(datos.id_autores)).all()
    if len(autores) != len(set(datos.id_autores)):
        raise HTTPException(status_code=400, detail="Algunos autores no existen")

    libro = LibroBD(
        titulo=datos.titulo,
        isbn=datos.isbn,
        anio_publicacion=datos.anio_publicacion,
        copias_disponibles=datos.copias_disponibles,
        autores=autores,
    )
    bd.add(libro)
    bd.commit()
    bd.refresh(libro)
    return LibroConAutores(
        **libro.__dict__,
        autores=[AutorLeer.from_orm(a) for a in autores]
    )


@router.get("", response_model=List[LibroLeer])
def listar_libros(anio: Optional[int] = Query(None), bd: Session = Depends(obtener_sesion_bd)):
    consulta = bd.query(LibroBD)
    if anio:
        consulta = consulta.filter(LibroBD.anio_publicacion == anio)
    return consulta.all()


@router.get("/{id_libro}", response_model=LibroConAutores)
def obtener_libro(id_libro: int, bd: Session = Depends(obtener_sesion_bd)):
    libro = bd.query(LibroBD).filter(LibroBD.id == id_libro).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return LibroConAutores(
        **libro.__dict__,
        autores=[AutorLeer.from_orm(a) for a in libro.autores]
    )
    
    
@router.put("/{id_libro}",)