import sqlite3

# FUNCIONES DE CONEXIÓN A LA BASE DE DATOS
def coneccion_db():
    conectar = sqlite3.connect('Proyecto_ultima.db')
    return conectar

def cerrar_coneccion_db(conectar):
    conectar.close()