from models.personal_model import PersonalModel
from sqlite3 import Error

class PersonalController():

    def __init__(self):
        self.model = PersonalModel()

    def registroPersonal(self, datos):
        if not all(key in datos for key in ["cedula", "primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido", "telefono", "nombre_usuario", "password"]):
            return {"estado": False, "error": "Datos incompletos"}

        try:
            persona_id= self.model.agregar_personal(
                cedula=datos["cedula"],
                primer_nombre=datos["primer_nombre"],
                segundo_nombre=datos["segundo_nombre"],
                primer_apellido=datos["primer_apellido"],
                segundo_apellido=datos["segundo_apellido"],
                telefono=datos["telefono"],
                nombre_usuario=datos["nombre_usuario"],
                password=datos["password"]
            )       

        except Error as e:
            return {"status": False, "error": "No se pudo registrar"}