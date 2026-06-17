# Importa Flask para crear la aplicación web
from flask import Flask, render_template, request, redirect
# Importa el conector que permite comunicarse con MySQL
import mysql.connector

# Crea la aplicación Flask
app = Flask(__name__)

# Crea la conexión con la base de datos
# mysql_principal es el nombre del servicio en docker-compose
def obtener_conexion():
    return mysql.connector.connect(
        host="mysql_secundario",
        user="root",
        password="root",
        database="replica"
    )

# Ruta principal
# Se ejecuta cuando ingresamos al navegador
@app.route("/")
def index():
    conexion = obtener_conexion()
    # Crea un cursor para ejecutar consultas SQL
    # dictionary=True permite obtener resultados como diccionarios
    cursor = conexion.cursor(dictionary=True)

    # Consulta todas las películas almacenadas
    cursor.execute(
        "SELECT * FROM peliculas"
    )

    # Guarda todos los registros encontrados
    peliculas = cursor.fetchall()

    conexion.close()

    # Envía las películas al archivo HTML
    return render_template(
        "index.html",
        peliculas=peliculas
    )

# Ruta para crear una película
# Solo acepta peticiones POST desde el formulario
@app.route("/agregar", methods=["POST"])
def agregar():
    conexion = obtener_conexion()
    # Obtiene los datos enviados desde el formulario
    nombre = request.form["nombre"]

    genero = request.form["genero"]
    # Crea cursor para ejecutar SQL
    cursor = conexion.cursor()
    # Inserta una nueva película
    cursor.execute(

        """
        INSERT INTO peliculas(nombre,genero)
        VALUES(%s,%s)
        """,

        (
            nombre,
            genero
        )

    )

    # Guarda definitivamente los cambios
    conexion.commit()
    conexion.close()

    # Regresa a la página principal
    return redirect("/")


# Ruta para buscar película por ID
@app.route("/buscar")
def buscar():
    conexion = obtener_conexion()

    # Obtiene el ID enviado desde el formulario
    id = request.args["id"]

    # Crea cursor
    cursor = conexion.cursor(dictionary=True)

    # Busca la película indicada
    cursor.execute(

        "SELECT * FROM peliculas WHERE id=%s",

        (id,)

    )

    # Guarda el resultado
    pelicula = cursor.fetchone()

    conexion.close()

    # Muestra solamente la película encontrada
    return render_template(

        "index.html",

        peliculas=[pelicula]

    )

# Ruta para eliminar una película
@app.route("/eliminar")
def eliminar():
    conexion = obtener_conexion()

    # Obtiene el ID enviado por URL
    id = request.args["id"]

    cursor = conexion.cursor()

    # Elimina el registro
    cursor.execute(

        "DELETE FROM peliculas WHERE id=%s",

        (id,)

    )

    # Guarda cambios
    conexion.commit()
    conexion.close()

    return redirect("/")

# Ruta para actualizar una película
# Recibe datos del formulario
@app.route("/actualizar", methods=["POST"])
def actualizar():
    conexion = obtener_conexion()

    # Obtiene datos enviados
    id = request.form["id"]

    nombre = request.form["nombre"]

    genero = request.form["genero"]

    cursor = conexion.cursor()

    # Actualiza la película seleccionada
    cursor.execute(

        """
        UPDATE peliculas
        SET nombre=%s,genero=%s
        WHERE id=%s
        """,

        (
            nombre,
            genero,
            id
        )

    )

    # Guarda cambios
    conexion.commit()
    conexion.close()


    return redirect("/")

# Inicia el servidor Flask
# 0.0.0.0 permite recibir conexiones desde otros contenedores
app.run(

    host="0.0.0.0",

    port=8100

)