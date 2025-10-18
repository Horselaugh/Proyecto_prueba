# matricula_controller.py
import sys
import os

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from models.matricula_model import MatriculaModel

# Instancia del modelo
modelo_matricula = MatriculaModel()

def crear(nna_id, unidad_id, grado, fecha_matricula=None, activa=True):
    """
    Controlador para crear una nueva matrícula educativa
    """
    return modelo_matricula.crear_matricula(
        nna_id=nna_id,
        unidad_id=unidad_id,
        grado=grado,
        fecha_matricula=fecha_matricula,
        activa=activa
    )

def leer(nna_id=None, unidad_id=None):
    """
    Controlador para buscar matrículas
    """
    return modelo_matricula.buscar_matricula(
        nna_id=nna_id,
        unidad_id=unidad_id
    )

def actualizar(nna_id, unidad_id, grado=None, fecha_matricula=None, activa=None):
    """
    Controlador para actualizar una matrícula
    """
    return modelo_matricula.actualizar_matricula(
        nna_id=nna_id,
        unidad_id=unidad_id,
        grado=grado,
        fecha_matricula=fecha_matricula,
        activa=activa
    )

def eliminar(nna_id, unidad_id):
    """
    Controlador para eliminar una matrícula
    """
    return modelo_matricula.eliminar_matricula(nna_id, unidad_id)

def listar_activas():
    """
    Controlador para listar todas las matrículas activas
    """
    return modelo_matricula.listar_matriculas_activas()

def obtener_por_nna(nna_id):
    """
    Controlador para obtener matrículas por NNA
    """
    return modelo_matricula.obtener_matricula_por_nna(nna_id)

def obtener_por_unidad(unidad_id):
    """
    Controlador para obtener matrículas por unidad educativa
    """
    return modelo_matricula.obtener_matriculas_por_unidad(unidad_id)