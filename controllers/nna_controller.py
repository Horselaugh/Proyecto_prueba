import sys
import os
from typing import Dict, List, Optional
import datetime
from models.nna_model import NNAModel
    
class NNAControlador:
    """Controlador para gestionar las operaciones de NNA"""

    def __init__(self):
        self.model = NNAModel()
        self.vista = None

    def set_view(self, view_instance):
        """Establece la instancia de la vista para que el controlador pueda interactuar con ella."""
        self.vista = view_instance

    def load_initial_data(self):
        """Carga inicial de datos al mostrar la vista (géneros)."""
        if not self.vista: return
        
        try:
            # CORRECCIÓN: Llamar al nuevo método listar_generos()
            generos = self.model.listar_generos()
            self.vista._cargar_generos(generos)
            self.vista.display_message("Listo para gestionar NNA. Ingrese el ID para buscar. 🔎", is_success=True)
            
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar datos iniciales: {str(e)}", is_success=False)

    # --- MÉTODOS DE MANEJO DE EVENTOS (Handle Methods) ---

    def _validar_datos(self, data: Dict) -> bool:
        """
        CORRECCIÓN: Valida SOLO la presencia de datos críticos (Obligatorios). 
        El formato de fecha, género y teléfono se delega al Modelo.
        """
        if not all([data.get('primer_nombre'), data.get('primer_apellido'), data.get('fecha_nacimiento')]):
            self.vista.display_message("❌ Nombre, apellido y fecha de nacimiento son obligatorios.", is_success=False)
            return False
            
        return True

    def handle_crear_nna(self, data: Dict):
        """Maneja la creación y actualiza la vista."""
        if not self.vista or not self._validar_datos(data): return
        
        try:
            resultado = self.model.crear_nna(data)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ NNA '{data['primer_nombre']} {data['primer_apellido']}' creado.", is_success=True)
                self.vista.limpiar_entradas()
            else:
                # El modelo maneja el mensaje de error de formato/BD
                self.vista.display_message(f"❌ Error al crear NNA: {resultado.get('error', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al crear NNA: {str(e)}", is_success=False)

    def handle_cargar_nna_por_id(self, nna_id: int):
        """Busca un NNA por ID y carga sus datos en la vista."""
        if not self.vista: return
            
        try:
            resultado = self.model.obtener_por_id(nna_id) 
            
            if resultado:
                self.vista.display_message(f"✅ NNA '{resultado['primer_nombre']} {resultado['primer_apellido']}' cargado.", is_success=True)
                self.vista._establecer_datos_formulario(resultado)
            else:
                self.vista.display_message(f"❌ No se encontró NNA con ID: {nna_id}", is_success=False)
                self.vista.limpiar_entradas(clean_search=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar NNA: {str(e)}", is_success=False)


    def handle_actualizar_nna(self, data: Dict):
        """Maneja la actualización y actualiza la vista."""
        nna_id = data.get('id')
        if not self.vista or not nna_id or not self._validar_datos(data): return
        
        try:
            # CORRECCIÓN: Clonar data y eliminar 'id'. Se pasa el diccionario limpio al modelo.
            update_data = {k: v for k, v in data.items() if k != 'id'}
            
            # CORRECCIÓN: Llamar al modelo pasando el diccionario 'update_data' directamente como el segundo argumento
            resultado = self.model.actualizar_nna(nna_id, update_data)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ NNA ID {nna_id} actualizado.", is_success=True)
                self.vista.limpiar_entradas()
            else:
                # El modelo maneja el mensaje de error de formato/BD
                self.vista.display_message(f"❌ Error al actualizar NNA: {resultado.get('error', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al actualizar NNA: {str(e)}", is_success=False)

    def handle_eliminar_nna(self, nna_id: int):
        """Maneja la eliminación y actualiza la vista."""
        if not self.vista or not nna_id:
            self.vista.display_message("❌ ID del NNA es obligatorio para eliminar.", is_success=False)
            return

        try:
            resultado = self.model.eliminar_nna(nna_id)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ NNA ID {nna_id} eliminado correctamente", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ Error al eliminar NNA: {resultado.get('message', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al eliminar NNA: {str(e)}", is_success=False)