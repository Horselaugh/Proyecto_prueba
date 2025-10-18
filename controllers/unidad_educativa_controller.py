# unidad_educativa_controller.py
import sys
import os

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from models.unidad_educativa_model import UnidadEducativaModel

# Instancia del modelo
modelo_unidad_educativa = UnidadEducativaModel()

def crear(nombre, director, tipo, telefono, direccion):
    """
    Controlador para crear una nueva unidad educativa
    """
    return modelo_unidad_educativa.crear_unidad_educativa(
        nombre=nombre,
        director=director,
        tipo=tipo,
        telefono=telefono,
        direccion=direccion
    )

def leer(id=None, nombre=None, tipo=None):
    """
    Controlador para buscar unidades educativas
    """
    return modelo_unidad_educativa.buscar_unidad_educativa(
        id=id,
        nombre=nombre,
        tipo=tipo
    )

def actualizar(id, nombre=None, director=None, tipo=None, telefono=None, direccion=None):
    """
    Controlador para actualizar una unidad educativa
    """
    return modelo_unidad_educativa.actualizar_unidad_educativa(
        id=id,
        nombre=nombre,
        director=director,
        tipo=tipo,
        telefono=telefono,
        direccion=direccion
    )

def eliminar(id):
    """
    Controlador para eliminar una unidad educativa
    """
    return modelo_unidad_educativa.eliminar_unidad_educativa(id)

def listar_todas():
    """
    Controlador para listar todas las unidades educativas
    """
    return modelo_unidad_educativa.listar_todas_unidades_educativas()