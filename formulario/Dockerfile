# Usa Python como imagen base
FROM python:latest


# Carpeta de trabajo dentro del contenedor
WORKDIR /app


# Copia el proyecto dentro del contenedor
COPY . .



# Instala Flask
RUN pip install flask



# Instala conexión MySQL
RUN pip install mysql-connector-python



# Expone el puerto donde trabaja Flask
EXPOSE 8100



# Ejecuta automáticamente la aplicación
CMD ["python","app2.py"]