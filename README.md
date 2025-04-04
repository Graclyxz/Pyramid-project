# Pyramid-project
Aplicacion web con varias tecnologias python: Backend>Pyramid, SQLalchymist y PostgreSQL; Frontend> React

# Modelos
1. Modelo Entidad-Relación (ER) para la base de datos.

   - Usuario
     - id (int)
     - nombre (str)
     - email (unique)
     - password [hash] (str)
     - direccion (str)
     - telefono (str)
     - es_admin (bo)
   - Producto
     - id (int)
     - nombre (str)
     - marca (str)
     - desc (str)
     - precio (fload)
     - cant_dis (int)
     - categoria (str)
     - imagen (str)
   - Carrito
     - id
     - usuario_id
     - producto_id
     - cantidad 


2. Componentes para la arquitectura del proyecto.
   - App
     - Autentificacion
       - login
       - Cliente
         - editar perfil
         - selccionar productos
     - Productos (admin)
       - Manejo de productos
         - crear
         - ver
         - editar
         - eliminar
     - Carrito
       - Añadir al carrito
       - Quitar productos del carrito
   - DataBase
     - Usuario
     - Producto
     - Carrito


# Estructura del Proyecto
1. Backend (Pyramid): Gestiona la lógica del servidor, la base de datos y la autenticación.
2. Frontend (React): Proporciona una interfaz de usuario interactiva para interactuar con el backend.

## Caracteristicas

### 1. Pyramid (Backend)
- Lenguaje: Python.
- Framework: Pyramid.
- Base de datos: PostgreSQL.
- ORM: SQLAlchemy.
- Autenticación: JSON Web Tokens (JWT) para la autenticación de usuarios.

### 2. React (Frontend)
- Lenguaje: JavaScript.
- Framework: React.
- Estilos: CSS

## Iniciar Backend
- initialize_backend_db development.ini
- pserve development.ini

## Instalación del Backend
Pasos de instalacion del proyecto

### 1. Entorno Virtual
- python -m venv env
- env\Scripts\activate

### 2. Dependencias Iniciales
- pip install pyramid cookiecutter psycopg2 

### 3. CookieCutter
- cookiecutter gh:Pylons/pyramid-cookiecutter-starter
  - opciones: 
    - project_name (Pyramid Scaffold): backend
    - repo_name (backend): backend
    - template_language: jinja2
    - sql backend: sqlalchemy

### 4. Iniciar Backend por primera vez

- cd Pyramid-backend
- pip install --upgrade pip setuptools
- pip install -e ".[testing]"
- alembic -c development.ini revision --autogenerate -m "init"
- alembic -c development.ini upgrade head
- initialize_backend_db development.ini
- pytest
- pserve development.ini

## Iniciar Frontend
- npm i
- npm start

## Instalación del Frontend
- npx create-react-app frontend
- cd frontend
- npm i axios react-router-dom
- npm start
