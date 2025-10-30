📚 Sistema de Biblioteca con FastAPI 📚

Descripcion:
    
    - La biblioteca necesita un sistema para gestionar su catalogo de libros y los autores
    - El sistema debe permitir:
        ✅ Registrar autores (nombre, pais de origen, anio de naciemiento)
        ✅ Registrar libros (titulo, ISBN, anio de publicacion, numero de copias disponibles)
        ✅ Un libro puede tener multiples autores (coautores)
        ✅ Consultar libros por autor
        ✅ Consultar autores de un libro


Endpionts requeridos (minimo):
    - De los requeriminetos se desprende la descripcion de las acciones que debe tener el sistema

    -- DEL AUTOR --

        ✅ Crear nuevo autor
        ✅ Listar todos autores (con filtro por pais)
        ✅ Obtener autor y sus libros
        ✅ Actualizar autor
        ✅ Eliminar Autor (¿Que pasa con sus libros?)

    -- DEL LIBRO --

        ✅ Crear libro con autor(es)
        ✅ Listar libros (con filtro por anio)
        ✅ Obtener libro y autores
        ✅ Actualizar libro
        ✅ Eliminar libro

    Incluye:

        ✅ CRUD completo para autores y libros
        ✅ Relación muchos-a-muchos (libros ↔ autores)

📏 Reglas de negocio:

    📋 ISBN unico : No pueden existir dos libros con mismo ISBN
    📋 No eliminar libro con copias disponibles
    📋 Cascada: Si elimina un autor, ¿Que pasa con sus libros? (opción ?forzar=true)


🏗️ Estructura del proyecto:

    ParcialBiblioteca/
    │── main.py
    │── base_datos.py
    │── modelos.py
    │── esquemas.py
    │── requirements.txt
    │── routers/
    │   ├── __init__.py
    │   ├── autores.py
    │   └── libros.py
    └── README.md

⚙️ Instalación y ejecución

    1️⃣ Clonar repositorio
        git clone <https://github.com/CaDCano/ParcialBiblioteca>
        cd ParcialBiblioteca

    2️⃣ Crear entorno virtual
        python -m venv .venv

    3️⃣ Activar entorno virtual

        source .venv/Scripts/activate

    4️⃣ Instalar dependencias
        pip install -r requirements.txt

    5️⃣ Ejecutar servidor
        uvicorn main:app --reload

🧪 Uso de la API
    🌐 Documentacion interactiva

Tipo	URL
Swagger UI	http://127.0.0.1:8000/docs

✨ Endpoints principales ✨
| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/autores/` | Listar autores |
| POST | `/autores/` | Crear autor |
| GET | `/autores/{id}` | Obtener autor y sus libros |
| PUT | `/autores/{id}` | Actualizar autor |
| DELETE | `/autores/{id}?forzar=true` | Eliminar autor (con cascada opcional)|
| GET | `/libros/` | Listar libros |
| POST | `/libros/` | Crear libro |
| GET | `/libros/{id}` | Obtener libro y autores |
| PUT | `/libros/{id}` | Actualizar libro |
| DELETE | `/libros/{id}` | Eliminar libro (solo si copias = 0)|

📥 Datos de prueba
    ✅ Autores


        {
        "nombre": "Gabriel García Márquez",
        "pais": "Colombia",
        "anio_nacimiento": 1927
        }

        {
        "nombre": "Mario Vargas Llosa",
        "pais": "Perú",
        "anio_nacimiento": 1936
        }

        {
        "nombre": "Isabel Allende",
        "pais": "Chile",
        "anio_nacimiento": 1942
        }


    ✅ Libros


        {
        "titulo": "Cien Años de Soledad",
        "isbn": "9788437604947",
        "anio_publicacion": 1967,
        "copias_disponibles": 10,
        "id_autores": [1]
        }

        {
        "titulo": "La Ciudad y Los Perros",
        "isbn": "9788420431406",
        "anio_publicacion": 1963,
        "copias_disponibles": 7,
        "id_autores": [2]
        }

        {
        "titulo": "La Casa de los Espíritus",
        "isbn": "9788401337536",
        "anio_publicacion": 1982,
        "copias_disponibles": 5,
        "id_autores": [3]
        }

        {
        "titulo": "Cuentos del Realismo Mágico",
        "isbn": "9780000001234",
        "anio_publicacion": 1985,
        "copias_disponibles": 4,
        "id_autores": [1, 3]
        }




📦Requerimientos📦

    
    Contenido de requirements.txt:
        fastapi
        uvicorn
        SQLAlchemy
        pydantic
        pydantic-settings
        typing-extensions
