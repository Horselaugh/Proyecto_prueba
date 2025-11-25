# controllers/denuncia_controller.py

from models.denuncia_model import DenunciaModel
from typing import Dict, List, Optional
import datetime

class DenunciaController:
    """
    Controlador para gestionar la creación, consulta y ciclo de vida (seguimiento, cierre) 
    de una Denuncia.
    """

    # Definiciones estáticas de catálogos (se podrían obtener de la DB en un sistema real)
    ROLES_NNA_VALIDOS = ['VICTIMA', 'AGRESOR', 'TESTIGO']

    def __init__(self):
        self.model = DenunciaModel()
        # self.vista = None # Se podría usar para callback de mensajes/actualización

    # def set_view(self, view):
    #     self.vista = view

    # ----------------------------------------------------------------------
    # Gestión de Creación de Denuncia Completa
    # ----------------------------------------------------------------------

    def registrar_nueva_denuncia(self, 
                                 datos_denuncia: Dict, 
                                 nna_involucrados: List[Dict], 
                                 denunciantes: List[Dict], 
                                 denunciados_ids: List[int]) -> tuple[bool, str]:
        """
        Coordina la creación de la denuncia principal y sus sub-registros.

        :param datos_denuncia: {'consejero_id', 'fecha_hechos', 'descripcion'}
        :param nna_involucrados: Lista de NNA y sus roles.
        :param denunciantes: Lista de personas que denuncian.
        :param denunciados_ids: Lista de IDs de persona de los denunciados.
        :return: (éxito, mensaje)
        """
        
        # --- 1. Validaciones Preliminares ---
        if not (datos_denuncia.get('consejero_id') and datos_denuncia.get('fecha_hechos') and datos_denuncia.get('descripcion')):
            return False, "Datos de la denuncia principal incompletos (Consejero, Fecha Hechos, Descripción)."
            
        if not nna_involucrados:
            return False, "Debe haber al menos un NNA involucrado en la denuncia."
            
        if not denunciantes and not denunciados_ids:
            return False, "La denuncia debe tener al menos un denunciante o un denunciado registrado."
            
        # --- 2. Validación de Involucrados (Estructura y Catálogo) ---
        for nna in nna_involucrados:
            if nna.get('rol') not in self.ROLES_NNA_VALIDOS:
                return False, f"Rol de NNA '{nna.get('rol')}' no es válido. Debe ser: {', '.join(self.ROLES_NNA_VALIDOS)}"
            try:
                # Asegurar que los IDs sean enteros válidos
                nna['nna_id'] = int(nna['nna_id'])
            except ValueError:
                return False, "El ID de uno de los NNA involucrados no es un número entero válido."
        
        # --- 3. Llamada al Modelo (Transacción) ---
        
        denuncia_id, mensaje = self.model.crear_denuncia_completa(
            datos_denuncia, 
            nna_involucrados, 
            denunciantes, 
            denunciados_ids
        )
        
        if denuncia_id:
            return True, f"Denuncia ID {denuncia_id} registrada con éxito. {mensaje}"
        else:
            return False, f"Fallo en el registro de la denuncia: {mensaje}"

    # ----------------------------------------------------------------------
    # Gestión de Ciclo de Vida (Seguimiento y Cierre)
    # ----------------------------------------------------------------------

    def agregar_registro_seguimiento(self, denuncia_id: int, consejero_id: int, observaciones: str) -> tuple[bool, str]:
        """
        Registra una nueva observación de seguimiento para una denuncia.
        """
        try:
            denuncia_id = int(denuncia_id)
            consejero_id = int(consejero_id)
        except ValueError:
            return False, "IDs de Denuncia y Consejero deben ser números válidos."
            
        if not observaciones or len(observaciones) < 10:
            return False, "Las observaciones de seguimiento son obligatorias y deben ser descriptivas."

        return self.model.agregar_seguimiento(denuncia_id, consejero_id, observaciones)

    def cerrar_expediente_denuncia(self, denuncia_id: int, consejero_id: int, acta_cierre: str) -> tuple[bool, str]:
        """
        Marca una denuncia como cerrada y registra el acta final.
        """
        try:
            denuncia_id = int(denuncia_id)
            consejero_id = int(consejero_id)
        except ValueError:
            return False, "IDs de Denuncia y Consejero deben ser números válidos."
            
        if not acta_cierre or len(acta_cierre) < 20:
            return False, "El acta de cierre es obligatoria y debe ser descriptiva."

        return self.model.cerrar_denuncia(denuncia_id, consejero_id, acta_cierre)

    # ----------------------------------------------------------------------
    # Consultas
    # ----------------------------------------------------------------------

    def obtener_detalles_denuncia(self, denuncia_id: int) -> Optional[Dict]:
        """
        Obtiene los datos principales de una denuncia por su ID.
        """
        try:
            denuncia_id = int(denuncia_id)
            return self.model.obtener_denuncia_por_id(denuncia_id)
        except ValueError:
            return None