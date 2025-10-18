import sys
import os
# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.nna_model import NNAModel

class NNAController:
    """Controlador para gestionar las operaciones de NNA (Niños, Niñas y Adolescentes)"""

    def __init__(self):
        self.model = NNAModel()

    def crear(self, primer_nombre, primer_apellido, fecha_nacimiento, genero, 
              direccion, telefono, segundo_nombre=None, segundo_apellido=None):
        """Crea un nuevo NNA"""
        datos = {
            "primer_nombre": primer_nombre,
            "segundo_nombre": segundo_nombre,
            "primer_apellido": primer_apellido,
            "segundo_apellido": segundo_apellido,
            "fecha_nacimiento": fecha_nacimiento,
            "genero": genero,
            "direccion": direccion,
            "telefono": telefono,
            "documento_identidad": None  # Puede ser None para NNA
        }
        
        return self.model.crear_nna(datos)

    def leer(self, id=None, primer_nombre=None, primer_apellido=None):
        """Lee NNA por ID o por nombre y apellido"""
        if id:
            resultado = self.model.obtener_por_id(id)
            if resultado:
                return {"data": [resultado], "status": "success"}
            else:
                return {"error": "No se encontraron registros", "status": "error"}
        elif primer_nombre and primer_apellido:
            resultados = self.model.obtener_por_nombre(primer_nombre, primer_apellido)
            if resultados:
                return {"data": resultados, "status": "success"}
            else:
                return {"error": "No se encontraron registros", "status": "error"}
        else:
            return {"error": "Se necesita ID o nombre y apellido", "status": "error"}

    def listar_todos(self):
        """Lista todos los NNA activos"""
        try:
            resultados = self.model.listar_todos()
            return {"data": resultados, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}

    def actualizar(self, id, **kwargs):
        """Actualiza un NNA existente"""
        return self.model.actualizar_nna(id, kwargs)

    def eliminar(self, id):
        """Elimina lógicamente un NNA"""
        return self.model.eliminar_nna(id)