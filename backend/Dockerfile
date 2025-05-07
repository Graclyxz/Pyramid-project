# Usa una imagen base de Python con la versión 3.13.2
FROM python:3.13-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala git, herramientas de compilación y dependencias de PostgreSQL
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libpq-dev \
    && apt-get clean

# Copia los archivos necesarios
COPY . .

# Instala las dependencias
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
RUN pip install -e ".[testing]"

# Inicializa y actualiza la base de datos
RUN alembic -c development.ini downgrade base
RUN alembic -c development.ini upgrade head
RUN initialize_backend_db development.ini

# Expone el puerto del backend
EXPOSE 6543

# Comando para iniciar el servidor
CMD ["pserve", "development.ini"]