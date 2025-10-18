# familiar_controller.py
import sys
import os

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from models.familiar_model import FamiliarModel

modelo_familiar = FamiliarModel()

def crear(primer_nombre, primer_apellido, parentesco_id, direccion, telefono, 
          segundo_nombre=None, segundo_apellido=None, tutor=False):
    return modelo_familiar.crear_familiar(
        primer_nombre=primer_nombre,
        primer_apellido=primer_apellido,
        parentesco_id=parentesco_id,
        direccion=direccion,
        telefono=telefono,
        segundo_nombre=segundo_nombre,
        segundo_apellido=segundo_apellido,
        tutor=tutor
    )

def leer(id=None, primer_nombre=None, primer_apellido=None):
    return modelo_familiar.buscar_familiar(
        id=id,
        primer_nombre=primer_nombre,
        primer_apellido=primer_apellido
    )

def actualizar(id, **kwargs):
    return modelo_familiar.actualizar_familiar(id, **kwargs)

def eliminar(id):
    return modelo_familiar.eliminar_familiar(id)