from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from base_datos import obtener_sesion_bd
from modelos import LibroBD, AutorBD
from esquemas import LibroCrear, LibroActualizar, LibroLeer, LibroConAutores, AutorLeer

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post("", response_model=LibroConAutores, status_code=status.HTTP_201_CREATED)
def crear_libro(datos: LibroCrear, bd: Session = Depends(obtener_sesion_bd)):
    """
    Crea un nuevo libro.

    Valida:
    - ISBN unico
    - Debe tener minimo un autor
    - Copias >= 0

    Error:
    - 400 si ISBN ya existe
    - 404 si un autor no existe
    """
    
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
    """
    Lista todos los libros.
    
    Parametros:
    - anio (int, opcional): Filtrar por año de publicacion
    """
    
    consulta = bd.query(LibroBD)
    if anio:
        consulta = consulta.filter(LibroBD.anio_publicacion == anio)
    return consulta.all()


@router.get("/{id_libro}", response_model=LibroConAutores)
def obtener_libro(id_libro: int, bd: Session = Depends(obtener_sesion_bd)):
    """
    Consulta informacion de un libro.

    Incluye:
    - Autores asociados

    Error:
    - 404 si libro no existe
    """
    
    libro = bd.query(LibroBD).filter(LibroBD.id == id_libro).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return LibroConAutores(
        **libro.__dict__,
        autores=[AutorLeer.from_orm(a) for a in libro.autores]
    )
    
    

@router.put("/{id_libro}", response_model=LibroConAutores)
def actualizar_libro(id_libro: int, datos: LibroActualizar, bd: Session = Depends(obtener_sesion_bd)):
    
    """
    Actualiza datos de un libro.

    Valida:
    - ISBN unico
    - Autores validos

    Error:
    - 404 si libro no existe
    - 400 si ISBN ya existe
    """
    
    libro = bd.query(LibroBD).filter(LibroBD.id == id_libro).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    datos_dict = datos.dict(exclude_unset=True)

    if "isbn" in datos_dict and datos_dict["isbn"] != libro.isbn:
        if bd.query(LibroBD).filter(LibroBD.isbn == datos_dict["isbn"]).first():
            raise HTTPException(status_code=400, detail="El ISBN ya existe")

    if "id_autores" in datos_dict:
        autores = bd.query(AutorBD).filter(AutorBD.id.in_(datos_dict["id_autores"])).all()
        if len(autores) != len(set(datos_dict["id_autores"])):
            raise HTTPException(status_code=400, detail="Algún autor no existe")
        libro.autores = autores

    for campo, valor in datos_dict.items():
        if campo not in ("id_autores",):
            setattr(libro, campo, valor)

    bd.commit()
    bd.refresh(libro)
    return LibroConAutores(
        **libro.__dict__,
        autores=[AutorLeer.from_orm(a) for a in libro.autores]
    )


@router.delete("/{id_libro}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(id_libro: int, bd: Session = Depends(obtener_sesion_bd)):
    
    """
    Elimina un libro.

    Condición:
    - Solo si copias_disponibles = 0

    Error:
    - 400 si aun tiene copias
    - 404 si libro no existe
    """
    
    libro = bd.query(LibroBD).filter(LibroBD.id == id_libro).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if libro.copias_disponibles > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar un libro con copias disponibles")
    bd.delete(libro)
    bd.commit()
    return None