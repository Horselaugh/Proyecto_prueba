import sys
import os
from models.denuncia_model import DenunciaModel
from typing import Dict, List, Optional
import datetime

# La importación 'sys.path.append' debe estar antes de cualquier importación local si es necesaria
sys.path.append(os.path.join(os.path.dirname(__file__))) 

class DenunciaController:
    """
    Controlador para gestionar la creación, consulta y ciclo de vida (seguimiento, cierre) 
    de una Denuncia.
    """

    # Definiciones estáticas de catálogos (se podrían obtener de la DB en un sistema real)
    ROLES_NNA_VALIDOS = ['VICTIMA', 'AGRESOR', 'TESTIGO']

    def __init__(self):
        self.model = DenunciaModel()
        
# --- MÉTODO CORREGIDO (actualizar_tabla) ---
    def actualizar_tabla(self, datos_busqueda: Dict = None, *args) -> List[Dict]:
        """
        Recupera el listado de denuncias aplicando filtros de búsqueda y estado.
        
        El argumento `*args` captura cualquier argumento posicional extra que pueda 
        ser enviado por los eventos (bind, command) de la vista (ej. el objeto Event o el valor del OptionMenu).
        
        :param datos_busqueda: Diccionario con los parámetros de la vista 
                                (ej: {'texto': 'texto_busqueda', 'estado': 'Pendiente'}). Es opcional.
        :return: Lista de diccionarios con los datos de las denuncias para la tabla.
        """
        # Si la llamada viene de un bind o command que no pasa datos, inicializamos un diccionario vacío
        if datos_busqueda is None or isinstance(datos_busqueda, str):
            # Si se recibe una cadena (valor del OptionMenu) o None, se asume que no hay filtros
            datos_busqueda = {}
            
        # 1. Obtener los parámetros de búsqueda de la vista
        # Ahora, si datos_busqueda es {}, las búsquedas serán vacías, lo que mostrará todo.
        texto_busqueda = datos_busqueda.get('texto', '').strip()
        filtro_estado = datos_busqueda.get('estado', 'Todos')
        
        # 2. Llamar al método del modelo para obtener los datos
        try:
            # Nota: Debes asegurarte que DenunciaModel tenga el método obtener_listado_denuncias_filtrado
            # Si texto_busqueda o filtro_estado son vacíos o 'Todos', el modelo debe manejarlo
            listado_denuncias = self.model.obtener_listado_denuncias_filtrado(
                texto_busqueda=texto_busqueda, 
                estado=filtro_estado
            )
            return listado_denuncias
        except Exception as e:
            # En un entorno real, se debería loggear el error
            print(f"Error al obtener listado de denuncias: {e}")
            return [] # Devuelve una lista vacía si hay un error
            
# --- MÉTODO FALTANTE AÑADIDO (generar_reporte_denuncias) ---
    def generar_reporte_denuncias(self, *args):
        """
        Lógica para generar y exportar el reporte actual (e.g., a PDF o Excel).
        
        El argumento `*args` se añade para permitir que este método sea usado como 
        callback de un botón si es necesario.
        """
        # Aquí iría la lógica para obtener todos los datos (o los filtrados actualmente)
        # y usar una librería como ReportLab o pandas/openpyxl para crear el archivo.
        print("Generando reporte de denuncias...")
        # Lógica de creación de archivo...
        
        # Simulación de éxito
        return True, "Reporte generado con éxito."

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