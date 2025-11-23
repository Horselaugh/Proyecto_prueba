import sys
import os
from typing import Dict, List, Optional
import datetime

# Configuraciones de Path e importación del Modelo real o Mock
try:
    from models.nna_model import NNAModel
except ImportError:
    # Mock si el modelo real no se encuentra
    class MockNNAModel:
        def obtener_por_id(self, id):
            if id == 1:
                return {
                    "id": 1, "primer_nombre": "Carlos", "segundo_nombre": "Manuel", 
                    "primer_apellido": "López", "segundo_apellido": "Díaz",
                    "fecha_nacimiento": "2015-05-20", "genero": "Masculino",
                    "direccion": "Av. Principal, Casa 5", "telefono": "555-4321", 
                    "documento_identidad": "V12345678" 
                }
            return None
        def crear_nna(self, datos): return {"status": "success", "message": "NNA creado.", "id": 2}
        def actualizar_nna(self, id, **kwargs): return {"status": "success", "message": f"NNA ID {id} actualizado."}
        def eliminar_nna(self, id): return {"status": "success", "message": f"NNA ID {id} eliminado."}
        def listar_generos(self): return ["Femenino", "Masculino", "Otro"]
        
    NNAModel = MockNNAModel
    
    
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
            generos = self.model.listar_generos()
            self.vista._cargar_generos(generos)
            self.vista.display_message("Listo para gestionar NNA. Ingrese el ID para buscar. 🔎", is_success=True)
            
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar datos iniciales: {str(e)}", is_success=False)

    # --- MÉTODOS DE MANEJO DE EVENTOS (Handle Methods) ---

    def _validar_datos(self, data: Dict) -> bool:
        """Valida la presencia de datos críticos y el formato de fecha."""
        if not all([data.get('primer_nombre'), data.get('primer_apellido'), data.get('fecha_nacimiento')]):
            self.vista.display_message("❌ Nombre, apellido y fecha de nacimiento son obligatorios.", is_success=False)
            return False
        
        try:
            datetime.date.fromisoformat(data.get('fecha_nacimiento'))
        except (ValueError, TypeError):
            self.vista.display_message("❌ Formato de Fecha de Nacimiento inválido. Use YYYY-MM-DD.", is_success=False)
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
                self.vista.display_message(f"❌ Error al crear NNA: {resultado.get('message', 'Desconocido')}", is_success=False)
                
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
            # Clonar data y eliminar 'id' para pasarlo como kwargs
            update_data = {k: v for k, v in data.items() if k != 'id'}
            resultado = self.model.actualizar_nna(nna_id, **update_data)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ NNA ID {nna_id} actualizado.", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ Error al actualizar NNA: {resultado.get('message', 'Desconocido')}", is_success=False)
                
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