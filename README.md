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
