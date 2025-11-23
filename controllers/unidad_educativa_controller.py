import sys
import os
from typing import List, Dict, Any, Optional

# ----------------------------------------------------------------------
# MOCKS (TEMPORAL) - Simulando el Modelo
# ----------------------------------------------------------------------
class MockUnidadEducativaModel:
    """Simulación del modelo de base de datos para Unidades Educativas."""
    
    def crear_unidad_educativa(self, **kwargs) -> Dict[str, Any]:
        # Simula éxito con un ID
        return {"status": "success", "id": 1, "message": f"UE {kwargs['nombre']} creada correctamente."}
        
    def buscar_unidad_educativa(self, id: Optional[int] = None, nombre: Optional[str] = None, tipo: Optional[str] = None) -> Dict[str, Any]:
        """Simula la consulta con filtros."""
        mock_data = [
            {"id": 1, "nombre": "E.B.N. Simon Bolivar", "director": "Ana Perez", "tipo": "Pública", "telefono": "04121234567", "direccion": "Calle A, Sector 1"},
            {"id": 2, "nombre": "U.E. Colegio San Jose", "director": "Luis Garcia", "tipo": "Privada", "telefono": "02129876543", "direccion": "Av. B, Urb. Central"},
        ]
        
        data_filtered = mock_data
        if id:
            data_filtered = [d for d in mock_data if d['id'] == id]
        elif nombre:
            data_filtered = [d for d in mock_data if nombre.lower() in d['nombre'].lower()]
        elif tipo:
            data_filtered = [d for d in mock_data if d['tipo'].lower() == tipo.lower()]
            
        return {"status": "success", "data": data_filtered, "message": f"Encontradas {len(data_filtered)} UE."}
        
    def actualizar_unidad_educativa(self, id: int, **kwargs) -> Dict[str, Any]:
        return {"status": "success", "message": f"UE ID {id} actualizada correctamente."}
        
    def eliminar_unidad_educativa(self, id: int) -> Dict[str, Any]:
        return {"status": "success", "message": f"UE ID {id} eliminada lógicamente."}
    
# Se asume que el modelo real existe si no hay excepción
try:
    from models.unidad_educativa_model import UnidadEducativaModel
except ImportError:
    UnidadEducativaModel = MockUnidadEducativaModel


class UnidadEducativaControlador:
    """Controlador para gestionar las operaciones de Unidades Educativas (UE)."""
    
    def __init__(self):
        self.vista = None
        self.model = UnidadEducativaModel()
        
    def set_view(self, view_instance):
        """Establece la instancia de la vista."""
        self.vista = view_instance

    def load_initial_data(self):
        """Carga inicial de datos (lista completa) al mostrar la vista."""
        if not self.vista: return
        try:
            resultado = self.model.buscar_unidad_educativa()
            if resultado['status'] == 'success':
                self.vista.display_list(resultado['data'])
                self.vista.display_message(f"✅ Cargadas {len(resultado['data'])} Unidades Educativas.", True)
            else:
                self.vista.display_message(f"❌ Error al cargar UE: {resultado.get('message', 'Desconocido')}", False)
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al cargar datos: {str(e)}", False)

    def handle_crear_ue(self, data: Dict[str, Any]):
        """Crea una nueva Unidad Educativa."""
        if not self.vista: return
        
        # Validaciones básicas
        if not data.get('nombre') or not data.get('director') or not data.get('telefono'):
            self.vista.display_message("❌ Nombre, director y teléfono son obligatorios.", False)
            return
            
        try:
            resultado = self.model.crear_unidad_educativa(**data)
            if resultado['status'] == 'success':
                self.vista.display_message(f"✅ {resultado['message']}", True)
                self.vista.limpiar_formulario()
                self.load_initial_data() # Refrescar lista
            else:
                self.vista.display_message(f"❌ Error al crear UE: {resultado.get('message', 'Desconocido')}", False)
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al crear UE: {str(e)}", False)

    def handle_buscar_ue(self, busqueda_id: Optional[int] = None, busqueda_nombre: Optional[str] = None):
        """Busca y muestra resultados en la vista."""
        if not self.vista: return

        try:
            resultado = self.model.buscar_unidad_educativa(id=busqueda_id, nombre=busqueda_nombre)
            
            if resultado['status'] == 'success':
                self.vista.display_list(resultado['data'])
                if resultado['data']:
                    self.vista.display_message(f"✅ Encontradas {len(resultado['data'])} Unidades Educativas.", True)
                else:
                    self.vista.display_message("⚠️ No se encontraron Unidades Educativas.", False)
            else:
                self.vista.display_message(f"❌ Error al buscar UE: {resultado.get('message', 'Desconocido')}", False)
                self.vista.display_list([])
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al buscar UE: {str(e)}", False)
            self.vista.display_list([])

    def handle_cargar_ue_para_edicion(self, id_ue: int):
        """Obtiene una UE y pasa sus datos a la vista para edición."""
        if not self.vista: return
        
        try:
            resultado = self.model.buscar_unidad_educativa(id=id_ue)
            
            if resultado['status'] == 'success' and resultado['data']:
                data = resultado['data'][0]
                self.vista._establecer_datos_formulario(data, id_ue)
                self.vista.display_message(f"✅ UE ID {id_ue} cargada para edición.", True)
            else:
                self.vista.display_message(f"❌ No se encontró la UE con ID {id_ue}.", False)
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar UE para edición: {str(e)}", False)

    def handle_actualizar_ue(self, id_ue: int, data: Dict[str, Any]):
        """Actualiza una Unidad Educativa existente."""
        if not self.vista: return
            
        try:
            # El modelo solo necesita los campos a actualizar
            data_to_update = {k: v for k, v in data.items() if v}
            resultado = self.model.actualizar_unidad_educativa(id=id_ue, **data_to_update)
            
            if resultado['status'] == 'success':
                self.vista.display_message(f"✅ {resultado['message']}", True)
                self.vista.limpiar_formulario()
                self.load_initial_data() # Refrescar lista
            else:
                self.vista.display_message(f"❌ Error al actualizar UE: {resultado.get('message', 'Desconocido')}", False)
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al actualizar UE: {str(e)}", False)

    def handle_eliminar_ue(self, id_ue: int):
        """Elimina una Unidad Educativa."""
        if not self.vista: return

        try:
            resultado = self.model.eliminar_unidad_educativa(id_ue)
            
            if resultado['status'] == 'success':
                self.vista.display_message(f"🗑️ {resultado['message']}", True)
                self.vista.limpiar_formulario()
                self.load_initial_data() # Refrescar lista
            else:
                self.vista.display_message(f"❌ Error al eliminar UE: {resultado.get('message', 'Desconocido')}", False)
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al eliminar UE: {str(e)}", False)