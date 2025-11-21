import sys
import os
from typing import List, Optional, Dict

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from ..models.seguimiento_expedientes_models import SeguimientoModel

modelo_seguimiento = SeguimientoModel()

def registrar_seguimiento(expediente_id: int, comentario: str, fecha: Optional[str] = None) -> int:
    return modelo_seguimiento.registrar_seguimiento(expediente_id, comentario, fecha)

def listar_seguimientos(expediente_id: Optional[int] = None, desde: Optional[str] = None, hasta: Optional[str] = None) -> List[Dict]:
    return modelo_seguimiento.obtener_seguimientos(expediente_id=expediente_id, desde=desde, hasta=hasta)