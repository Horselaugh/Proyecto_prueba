# Importación de librerías
import sqlite3
from sqlite3 import Error

# Se define la clase para acceder a la base de datos
class Database():
    
	def __init__(self, db_archivo = "database.db"):
		self.db_archivo = db_archivo

	# Se define la función de crear la conexión a la base de datos
	def crearConexion(self):
		try:
			self.conexion = sqlite3.connect(self.db_archivo)
			print(f"Conexión exitosa a la base de datos: {self.db_archivo}")
			return self.conexion
		
		except Error as e:
			print(f"Error: {e}. Al tratar de conectar a la base de datos")
			return None
	
	# Se define la función que cierra la conexión con la base de datos
	def cerrarConexion(conexion):
		if conexion:
			conexion.close()
			print(f"La conexión con la base de datos ha finalizado")
