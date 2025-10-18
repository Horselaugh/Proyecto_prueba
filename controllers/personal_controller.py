from models.personal_model import PersonalModel
from sqlite3 import Error

class PersonalController:
    """Controlador para gestionar las operaciones de Personal"""

    def __init__(self):
        self.model = PersonalModel()

    def agregar_personal(self, cedula, primer_nombre, segundo_nombre, primer_apellido, 
                        segundo_apellido, telefono, nombre_usuario, password):
        """Agrega nuevo personal a la base de datos"""
        try:
            datos = {
                "cedula": cedula,
                "primer_nombre": primer_nombre,
                "segundo_nombre": segundo_nombre,
                "primer_apellido": primer_apellido,
                "segundo_apellido": segundo_apellido,
                "telefono": telefono,
                "direccion": "Por definir",
                "genero": "M",
                "cargo": 1,
                "resolucion": None,
                "nombre_usuario": nombre_usuario,
                "password": password
            }
            
            persona_id = self.model.agregar_personal(datos)
            return persona_id
            
        except Error as e:
            print(f"Error al agregar nuevo personal: {e}")
            return None

    def obtener_personal(self, persona_id):
        """Obtiene un personal por su ID"""
        try:
            return self.model.obtener_por_id(persona_id)
        except Error as e:
            print(f"Error al obtener personal: {e}")
            return None

    def listar_personal(self):
        """Lista todo el personal activo"""
        try:
            return self.model.listar_todo()
        except Error as e:
            print(f"Error al listar personal: {e}")
            return []

    def actualizar_personal(self, datos):
        """Actualiza los datos de un personal"""
        try:
            return self.model.actualizar_personal(datos)
        except Error as e:
            print(f"Error al actualizar personal: {e}")
            return False

    def eliminar_personal(self, persona_id):
        """Elimina lógicamente un personal"""
        try:
            return self.model.eliminar_personal(persona_id)
        except Error as e:
            print(f"Error al eliminar personal: {e}")
            return False

    def obtener_por_usuario(self, nombre_usuario):
        """Obtiene un personal por nombre de usuario"""
        try:
            return self.model.obtener_por_usuario(nombre_usuario)
        except Error as e:
            print(f"Error al obtener personal por usuario: {e}")
            return None