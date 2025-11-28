import sys
import os
from models.denuncia_model import DenunciaModel 
from typing import Dict, List, Optional

class DenunciaController:
    """
    Controlador para gestionar la creación, consulta y ciclo de vida (seguimiento, cierre) 
    de una Denuncia.
    """

    # Definiciones estáticas de catálogos (se podrían obtener de la DB en un sistema real)
    ROLES_NNA_VALIDOS = ['VICTIMA', 'AGRESOR', 'TESTIGO']

    def __init__(self):
        self.model = DenunciaModel()
        self.view = None 
        
    def set_view(self, view_instance):
        self.view = view_instance
        print(f"Vista asignada al controlador: {self.view.__class__.__name__}")
        
# ----------------------------------------------------------------------
# Métodos de Manejo de Eventos 
# ----------------------------------------------------------------------

    def load_initial_data(self):
        """Método solicitado por la vista para cargar los datos iniciales al mostrar el frame."""
        print("Cargando datos iniciales de denuncias...")
        listado = self.actualizar_tabla() 

    def handle_crear_denuncia(self, titulo, denunciante, estado, descripcion):
        """Maneja el evento de creación. Usa la firma simplificada de la vista (Simulación de creación)."""
        print(f"Intento de creación de denuncia: Título='{titulo}', Denunciante='{denunciante}', Estado='{estado}'")
        if hasattr(self.view, 'display_message'):
             self.view.display_message("⚠️ El formulario simplificado no contiene todos los campos (e.g., Consejero ID, Fecha Hechos, Denunciantes, NNA Involucrados). Se necesita un formulario extendido para registrar la denuncia completa.", is_success=False)

    def handle_buscar_denuncia(self, termino_busqueda: str):
        """Maneja el evento de búsqueda (por ID o texto)."""
        print(f"Buscando denuncias por término: '{termino_busqueda}'")
        
        try:
            denuncia_id = int(termino_busqueda)
            detalles = self.obtener_detalles_denuncia(denuncia_id)
            if detalles and hasattr(self.view, '_establecer_datos_formulario'):
                 # Simulación del campo 'denunciante' para la vista simplificada
                 detalles['denunciante'] = 'Denunciante de Ejemplo (Simulación)'
                 self.view._establecer_datos_formulario(detalles)
                 self.view.display_message(f"Denuncia ID {denuncia_id} cargada exitosamente.", is_success=True)
                 return
        except ValueError:
            # Búsqueda por texto (no ID)
            pass
            
        datos_busqueda = {'texto': termino_busqueda, 'estado': 'Todos'} 
        listado = self.actualizar_tabla(datos_busqueda)
        
        if hasattr(self.view, 'display_message'):
             self.view.display_message(f"Búsqueda finalizada. {len(listado)} resultados encontrados.", is_success=True)

    def handle_modificar_denuncia(self, denuncia_id: int, titulo: str, denunciante: str, estado: str, descripcion: str):
        """
        Maneja el evento de modificación. Actualiza la descripción y el estado.
        """
        print(f"Intento de modificación para Denuncia ID {denuncia_id}.")
        
        try:
            denuncia_id = int(denuncia_id)
        except ValueError:
            if hasattr(self.view, 'display_message'):
                self.view.display_message("❌ ID de Denuncia no válido.", is_success=False)
            return

        # Mapeo de estado de la vista a booleano para el modelo (True=Abierta/Pendiente, False=Cerrada/Resuelta)
        estado_bool = True if estado in ["Pendiente", "En Revisión"] else False

        success, msg = self.model.actualizar_datos_basicos_denuncia(denuncia_id, descripcion, estado_bool)
        
        if hasattr(self.view, 'display_message'):
             self.view.display_message(f"Denuncia ID {denuncia_id} modificada. {msg}", is_success=success)
             if success and hasattr(self.view, 'limpiar_entradas'):
                self.view.limpiar_entradas()

    def handle_eliminar_denuncia(self, denuncia_id):
        """
        [CORRECCIÓN CLAVE] Maneja el evento de eliminación llamando al modelo.
        """
        print(f"Intento de eliminación para Denuncia ID {denuncia_id}.")
        
        try:
            denuncia_id = int(denuncia_id)
        except ValueError:
            if hasattr(self.view, 'display_message'):
                self.view.display_message("❌ ID de Denuncia no válido.", is_success=False)
            return

        # Llama al método real del modelo
        success, msg = self.model.eliminar_denuncia(denuncia_id)
        
        if hasattr(self.view, 'display_message'):
             self.view.display_message(f"Denuncia ID {denuncia_id}: {msg}", is_success=success)
             if success and hasattr(self.view, 'limpiar_entradas'):
                self.view.limpiar_entradas() 

# ----------------------------------------------------------------------
# Métodos de Datos y Lógica Central (Se omiten para brevedad)
# ----------------------------------------------------------------------
        
    def actualizar_tabla(self, datos_busqueda: Dict = None, *args) -> List[Dict]:
        """Recupera el listado de denuncias aplicando filtros."""
        if datos_busqueda is None or isinstance(datos_busqueda, str):
            datos_busqueda = {}
            
        texto_busqueda = datos_busqueda.get('texto', '').strip()
        filtro_estado = datos_busqueda.get('estado', 'Todos')
        
        try:
            return self.model.obtener_listado_denuncias_filtrado(
                texto_busqueda=texto_busqueda, 
                estado=filtro_estado
            )
        except Exception as e:
            print(f"Error al obtener listado de denuncias: {e}")
            return []
            
    def obtener_detalles_denuncia(self, denuncia_id: int) -> Optional[Dict]:
        """Obtiene los datos principales de una denuncia por su ID."""
        try:
            denuncia_id = int(denuncia_id)
            return self.model.obtener_denuncia_por_id(denuncia_id)
        except ValueError:
            return None