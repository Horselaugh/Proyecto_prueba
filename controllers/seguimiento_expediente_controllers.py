# File: seguimiento_expediente_controllers.py
import sys
import os
from typing import List, Optional, Dict, Any
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__))) 

try:
    from models.seguimiento_expedientes_models import SeguimientoModel
except ImportError as e:
    # Se ajusta la descripción de error de ArticuloModelo a SeguimientoModel
    raise ImportError(f"No se pudo importar SeguimientoModel: {e}")
    
    
class SeguimientoExpedienteControlador:
    """Controlador para gestionar el seguimiento y registro de expedientes."""

    def __init__(self):
        self.vista = None
        # Ambos deben usar la misma instancia de SeguimientoModel que usa el Singleton
        self.model = SeguimientoModel()
        self.exp_model = self.model # Usar la misma instancia
        self.expediente_map: Dict[str, int] = {} # Mapeo de cadena de ComboBox a ID
        
    def set_view(self, view_instance):
        """Establece la instancia de la vista."""
        self.vista = view_instance
        
    def load_initial_data(self):
        """Carga inicial de datos (lista de expedientes) al mostrar la vista."""
        if not self.vista: return
        
        try:
            expedientes = self.exp_model.listar_expedientes()
            options = []
            for exp in expedientes:
                # El modelo retorna 'titulo' y 'estado' (aunque sean mockeados)
                key = f"{exp['id']} - {exp['titulo']} ({exp['estado']})" 
                self.expediente_map[key] = exp['id']
                options.append(key)
                
            self.vista._cargar_opciones_expedientes(options)
            self.vista.display_message("Datos iniciales de expedientes cargados.", is_success=True)
            
            # Cargar el historial completo inicialmente
            self.handle_listar_seguimientos() 
            

        except Exception as e:
            # El error aquí ahora debería ser menos probable si la conexión funciona
            self.vista.display_message(f"❌ Error al cargar datos iniciales: {str(e)}", is_success=False)

    def handle_registrar_seguimiento(self, expediente_str: str, comentario: str):
        """Registra un nuevo seguimiento en la base de datos."""
        if not self.vista: return
        
        expediente_id = self.get_expediente_id_from_str(expediente_str)
        
        if not expediente_id:
            self.vista.display_message("❌ Seleccione un Expediente válido.", is_success=False)
            return
            
        if not comentario or len(comentario.strip()) < 10:
            self.vista.display_message("❌ El comentario es obligatorio y debe tener al menos 10 caracteres.", is_success=False)
            return
            
        try:
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            
            # El modelo ahora retorna dict {"status": "success", "id": new_id} o {"status": "error", "message": error}
            resultado = self.model.registrar_seguimiento(expediente_id, comentario, fecha=fecha_actual)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ Seguimiento ID {resultado.get('id')} registrado para EXP {expediente_id}.", is_success=True)
                self.vista.limpiar_registro()
                # Volver a cargar el historial para refrescar la vista
                self.handle_listar_seguimientos(expediente_id=expediente_id) 
            else:
                self.vista.display_message(f"❌ Error al registrar: {resultado.get('message', 'Error desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al registrar seguimiento: {str(e)}", is_success=False)


    def handle_listar_seguimientos(self, expediente_id: Optional[int] = None, desde: Optional[str] = None, hasta: Optional[str] = None):
        """Lista y muestra los seguimientos en el historial."""
        if not self.vista: return
        
        try:
            seguimientos = self.model.obtener_seguimientos(expediente_id=expediente_id, desde=desde, hasta=hasta)
            
            if seguimientos:
                # El controlador formatea los datos para la vista (agrega la descripción)
                for s in seguimientos:
                    s['expediente_desc'] = next((k for k, v in self.expediente_map.items() if v == s['expediente_id']), f"ID {s['expediente_id']}")
                    
                self.vista._mostrar_historial(seguimientos)
            else:
                self.vista._mostrar_historial([], message="No hay registros de seguimiento para los filtros indicados.")
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al obtener el historial: {str(e)}", is_success=False)
            self.vista._mostrar_historial([], message=f"Error al obtener historial: {str(e)}")

    def get_expediente_id_from_str(self, expediente_str: str) -> Optional[int]:
        """Obtiene el ID del expediente a partir de la cadena seleccionada."""
        return self.expediente_map.get(expediente_str)