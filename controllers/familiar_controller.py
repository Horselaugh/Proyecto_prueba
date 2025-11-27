import sys
import os
from typing import Dict
from models.familiar_model import FamiliarModel

sys.path.append(os.path.join(os.path.dirname(__file__)))

class FamiliarControlador:
    """Controlador para gestionar las operaciones de Familiares"""

    def __init__(self):
        # Inicializa con el modelo real (FamiliarModel)
        self.model = FamiliarModel()
        self.vista = None

    def set_view(self, view_instance):
        """Establece la instancia de la vista para que el controlador pueda interactuar con ella."""
        self.vista = view_instance

    def load_initial_data(self):
        """Carga inicial de datos al mostrar la vista (parentescos)."""
        if not self.vista:
            return
        
        try:
            # Llama al método obtener_parentescos del modelo real (asumiendo que se añadió)
            parentescos = self.model.obtener_parentescos()
            self.vista._cargar_parentescos(parentescos)
            self.vista.display_message(
                "Listo para gestionar Familiares. 🏠",
                is_success=True
            )
            
        except Exception as e:
            # Muestra el error si obtener_parentescos no está implementado o falla
            error_msg = f"❌ Error al cargar datos iniciales: {str(e)}"
            self.vista.display_message(error_msg, is_success=False)

    # --- MÉTODOS DE MANEJO DE EVENTOS (Handle Methods) ---

    def _validar_datos(self, data: Dict) -> bool:
        """Valida la presencia de datos críticos (nombre, apellido, parentesco_id)."""
        
        obligatory_fields = [
            data.get('primer_nombre'),
            data.get('primer_apellido'),
            data.get('parentesco_id')
        ]
        
        # Se asume que la vista proporciona 'parentesco_id'
        if not all(obligatory_fields):
            self.vista.display_message(
                "❌ Nombre, apellido y parentesco son campos obligatorios.",
                is_success=False
            )
            return False
        return True

    def handle_crear_familiar(self, data: Dict):
        """Maneja la creación de un familiar y actualiza la vista."""
        if not self.vista:
            return
        if not self._validar_datos(data):
            return
        
        try:
            # El modelo ahora requiere 'parentesco_id'
            resultado = self.model.crear_familiar(**data)
            
            if resultado.get("status") == "success":
                success_msg = (
                    f"✅ Familiar '{data['primer_nombre']} {data['primer_apellido']}' creado."
                )
                self.vista.display_message(success_msg, is_success=True)
                self.vista.limpiar_entradas()
            else:
                # El modelo real usa 'error' en caso de fallo
                error_msg = resultado.get('error', 'Desconocido')
                self.vista.display_message(f"❌ Error al crear familiar: {error_msg}", is_success=False)
                
        except Exception as e:
            error_msg = f"❌ Error interno al crear familiar: {str(e)}"
            self.vista.display_message(error_msg, is_success=False)

    def handle_cargar_familiar_por_id(self, familiar_id: int):
        """Maneja la búsqueda de un familiar por ID y carga sus datos en la vista."""
        if not self.vista:
            return

        try:
            # La función buscar_familiar del modelo devuelve {'data': [...]} o {'error': ...}
            resultado = self.model.buscar_familiar(id=familiar_id) 
            
            # Extraer el diccionario de datos del familiar
            if resultado.get("status") == "success" and resultado.get("data"):
                # Extraemos el primer (y único) registro del familiar
                familiar_data = resultado['data'][0]
                
                self.vista.display_message(
                    f"✅ Familiar ID {familiar_id} cargado.", 
                    is_success=True
                )
                self.vista._establecer_datos_formulario(familiar_data) # Se envía el diccionario de datos
            else:
                error_msg = resultado.get('error', f"No se encontró familiar con ID: {familiar_id}")
                self.vista.display_message(f"❌ {error_msg}", is_success=False)
                self.vista.limpiar_entradas(clean_search=False)
                
        except Exception as e:
            error_msg = f"❌ Error al cargar familiar: {str(e)}"
            self.vista.display_message(error_msg, is_success=False)


    def handle_actualizar_familiar(self, data: Dict):
        """Maneja la actualización de un familiar y actualiza la vista."""
        familiar_id = data.get('id')
        if not self.vista or not familiar_id: 
            self.vista.display_message(
                "❌ ID del familiar es obligatorio para modificar.",
                is_success=False
            )
            return
        
        # Clonar data y eliminar 'id' antes de pasarlo a actualizar_familiar
        # Se asegura que 'parentesco_id' esté incluido para la actualización
        update_data = {k: v for k, v in data.items() if k not in ('id',)}
        
        try:
            resultado = self.model.actualizar_familiar(familiar_id, **update_data)
            
            if resultado.get("status") == "success":
                self.vista.display_message(
                    f"✅ Familiar ID {familiar_id} actualizado.", 
                    is_success=True
                )
                self.vista.limpiar_entradas()
            else:
                error_msg = resultado.get('error', 'Desconocido')
                self.vista.display_message(f"❌ Error al actualizar familiar: {error_msg}", is_success=False)
                
        except Exception as e:
            error_msg = f"❌ Error interno al actualizar familiar: {str(e)}"
            self.vista.display_message(error_msg, is_success=False)

    def handle_eliminar_familiar(self, familiar_id: int):
        """Maneja la eliminación de un familiar y actualiza la vista."""
        if not self.vista or not familiar_id:
            self.vista.display_message(
                "❌ ID del familiar es obligatorio para eliminar.", 
                is_success=False
            )
            return

        try:
            resultado = self.model.eliminar_familiar(familiar_id)
            
            if resultado.get("status") == "success":
                self.vista.display_message(
                    f"✅ Familiar ID {familiar_id} eliminado correctamente", 
                    is_success=True
                )
                self.vista.limpiar_entradas()
            else:
                error_msg = resultado.get('error', 'Desconocido')
                self.vista.display_message(f"❌ Error al eliminar familiar: {error_msg}", is_success=False)
                
        except Exception as e:
            error_msg = f"❌ Error interno al eliminar familiar: {str(e)}"
            self.vista.display_message(error_msg, is_success=False)