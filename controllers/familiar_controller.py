import sys
import os
from typing import Dict, List, Optional

# Configuraciones de Path e importación del Modelo real o Mock
try:
    # Intenta importar el modelo real
    from models.familiar_model import FamiliarModel
    from sqlite3 import Row
except ImportError:
    # Si el modelo real no existe, usamos un mock para la simulación
    class MockFamiliarModel:
        def obtener_parentescos(self):
            return [{"id": 1, "nombre": "Padre"}, {"id": 2, "nombre": "Madre"}, {"id": 3, "nombre": "Abuelo"}]

        def buscar_familiar(self, id=None, **kwargs):
            if id == 1:
                return {"id": 1, "primer_nombre": "Juan", "primer_apellido": "Pérez", 
                        "parentesco_id": 1, "parentesco_desc": "Padre", 
                        "direccion": "Calle Falsa 123", "telefono": "555-1234", 
                        "segundo_nombre": None, "segundo_apellido": "Sánchez", "tutor": True}
            return None

        def crear_familiar(self, **kwargs): return {"status": "success", "message": "Familiar creado (Mock)", "id": 5}
        def actualizar_familiar(self, id, **kwargs): return {"status": "success", "message": f"Familiar ID {id} actualizado (Mock)", "id": id}
        def eliminar_familiar(self, id): return {"status": "success", "message": f"Familiar ID {id} eliminado (Mock)"}
        
    FamiliarModel = MockFamiliarModel
    
    
class FamiliarControlador:
    """Controlador para gestionar las operaciones de Familiares"""

    def __init__(self):
        self.model = FamiliarModel()
        self.vista = None

    def set_view(self, view_instance):
        """Establece la instancia de la vista para que el controlador pueda interactuar con ella."""
        self.vista = view_instance

    def load_initial_data(self):
        """Carga inicial de datos al mostrar la vista (parentescos)."""
        if not self.vista: return
        
        try:
            parentescos = self.model.obtener_parentescos()
            self.vista._cargar_parentescos(parentescos)
            self.vista.display_message("Listo para gestionar Familiares. 🏠", is_success=True)
            
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar datos iniciales: {str(e)}", is_success=False)

    # --- MÉTODOS DE MANEJO DE EVENTOS (Handle Methods) ---

    def _validar_datos(self, data: Dict) -> bool:
        """Valida la presencia de datos críticos."""
        if not all([data.get('primer_nombre'), data.get('primer_apellido'), data.get('parentesco_id')]):
            self.vista.display_message("❌ Nombre, apellido y parentesco son campos obligatorios.", is_success=False)
            return False
        return True

    def handle_crear_familiar(self, data: Dict):
        """Maneja la creación y actualiza la vista."""
        if not self.vista or not self._validar_datos(data): return
        
        try:
            resultado = self.model.crear_familiar(**data)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ Familiar '{data['primer_nombre']} {data['primer_apellido']}' creado.", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ Error al crear familiar: {resultado.get('message', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al crear familiar: {str(e)}", is_success=False)

    def handle_cargar_familiar_por_id(self, familiar_id: int):
        """Busca un familiar por ID y carga sus datos en la vista."""
        if not self.vista: return

        try:
            # Asumimos que buscar_familiar en el modelo puede buscar por ID
            resultado = self.model.buscar_familiar(id=familiar_id) 
            
            if resultado:
                self.vista.display_message(f"✅ Familiar ID {familiar_id} cargado.", is_success=True)
                self.vista._establecer_datos_formulario(resultado)
            else:
                self.vista.display_message(f"❌ No se encontró familiar con ID: {familiar_id}", is_success=False)
                self.vista.limpiar_entradas(clean_search=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar familiar: {str(e)}", is_success=False)


    def handle_actualizar_familiar(self, data: Dict):
        """Maneja la actualización y actualiza la vista."""
        familiar_id = data.get('id')
        if not self.vista or not familiar_id or not self._validar_datos(data): return
        
        try:
            # Clonar data y eliminar 'id' para pasarlo como kwargs
            update_data = {k: v for k, v in data.items() if k != 'id'}
            resultado = self.model.actualizar_familiar(familiar_id, **update_data)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ Familiar ID {familiar_id} actualizado.", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ Error al actualizar familiar: {resultado.get('message', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al actualizar familiar: {str(e)}", is_success=False)

    def handle_eliminar_familiar(self, familiar_id: int):
        """Maneja la eliminación y actualiza la vista."""
        if not self.vista or not familiar_id:
            self.vista.display_message("❌ ID del familiar es obligatorio para eliminar.", is_success=False)
            return

        try:
            resultado = self.model.eliminar_familiar(familiar_id)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ Familiar ID {familiar_id} eliminado correctamente", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ Error al eliminar familiar: {resultado.get('message', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al eliminar familiar: {str(e)}", is_success=False)