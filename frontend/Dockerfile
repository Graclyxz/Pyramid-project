# Usa una imagen base de Node.js con la versión 22.14.0
FROM node:22.14.0

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY package.json package-lock.json ./
RUN npm install

# Copia el resto de los archivos
COPY . .

# Construye la aplicación
RUN npm run build

# Usa una imagen base de Nginx para servir el frontend
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

# Expone el puerto del frontend
EXPOSE 80

# Comando para iniciar Nginx
CMD ["nginx", "-g", "daemon off;"]