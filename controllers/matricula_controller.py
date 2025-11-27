import sys
import os
from typing import Dict, List, Optional
import datetime
# La importación debe ser relativa al entorno de ejecución (ej. models.matricula_model)
from models.matricula_model import MatriculaModel

class MatriculaControlador:
    """Controlador para gestionar las operaciones de Matrículas"""

    def __init__(self):
        self.model = MatriculaModel()
        self.vista = None

    def set_view(self, view_instance):
        """Establece la instancia de la vista para que el controlador pueda interactuar con ella."""
        self.vista = view_instance

    def load_initial_data(self):
        """Carga inicial de datos al mostrar la vista (NNA, Unidades y Grados)."""
        if not self.vista: return
        
        try:
            # Obtener datos del modelo
            nna_list = self.model.obtener_nna()
            unidad_list = self.model.obtener_unidades_educativas()
            grados_list = self.model.listar_grados()
            
            # Pasar datos a la vista
            self.vista._cargar_comboboxes(nna_list, unidad_list, grados_list)
            self.vista.display_message("Seleccione un NNA y una Unidad Educativa. 🎓", is_success=True)
            
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar datos iniciales: {str(e)}", is_success=False)

    # --- MÉTODOS DE MANEJO DE EVENTOS (Handle Methods) ---

    def _validar_datos_comunes(self, data: Dict) -> bool:
        """Valida la presencia de datos críticos."""
        # Se verifica que los IDs y el grado no sean None, lo que indica que no se seleccionó
        if not all([data.get('nna_id'), data.get('unidad_id'), data.get('grado')]):
            self.vista.display_message("❌ NNA, Unidad Educativa y Grado son obligatorios.", is_success=False)
            return False
        
        # Validar formato de fecha (simple)
        try:
            datetime.date.fromisoformat(data.get('fecha_matricula'))
        except (ValueError, TypeError):
            self.vista.display_message("❌ Formato de Fecha de Matrícula inválido. Use YYYY-MM-DD.", is_success=False)
            return False

        return True

    def handle_crear_matricula(self, data: Dict):
        """Maneja la creación y actualiza la vista."""
        if not self.vista or not self._validar_datos_comunes(data): return
        
        try:
            resultado = self.model.crear_matricula(**data)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ Matrícula creada exitosamente.", is_success=True)
                # Mantener la selección de NNA/Unidad, solo limpiar campos de matrícula
                self.vista.limpiar_entradas(clean_nna_unidad=False)
            else:
                # El modelo usa la clave 'error' para el mensaje
                self.vista.display_message(f"❌ Error al crear matrícula: {resultado.get('error', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al crear matrícula: {str(e)}", is_success=False)

    def handle_buscar_matricula(self, nna_id: int, unidad_id: int):
        """Busca una matrícula específica y carga sus datos en la vista."""
        if not self.vista or not nna_id or not unidad_id: 
            self.vista.limpiar_entradas(clean_nna_unidad=False) 
            return
            
        try:
            resultado = self.model.buscar_matricula(nna_id=nna_id, unidad_id=unidad_id) 
            
            if resultado.get("status") == "success" and resultado.get("data"):
                data_list = resultado["data"]
                data = data_list[0] # Asumimos que solo debería haber una matrícula activa NNA-Unidad
                self.vista.display_message(f"✅ Matrícula encontrada. Grado: {data['grado']}", is_success=True)
                self.vista._establecer_datos_formulario(data)
            else:
                # Si el estado es error o no hay data (no se encontró), limpia campos
                self.vista.display_message("ℹ️ No hay matrícula existente para esta combinación. Puede crear una nueva.", is_success=True)
                self.vista.limpiar_entradas(clean_nna_unidad=False) # Limpia campos de matrícula, mantiene selección
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al buscar matrícula: {str(e)}", is_success=False)


    def handle_actualizar_matricula(self, data: Dict):
        """Maneja la actualización y actualiza la vista."""
        nna_id = data.get('nna_id')
        unidad_id = data.get('unidad_id')
        
        if not self.vista or not nna_id or not unidad_id or not self._validar_datos_comunes(data): return
        
        try:
            # Clonar data y eliminar IDs para pasarlo como kwargs al modelo
            update_data = {k: v for k, v in data.items() if k not in ['nna_id', 'unidad_id']}
            resultado = self.model.actualizar_matricula(nna_id, unidad_id, **update_data)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ Matrícula actualizada correctamente.", is_success=True)
                # Volver a buscar para recargar los datos actualizados y el estado de los botones
                self.handle_buscar_matricula(nna_id, unidad_id) 
            else:
                self.vista.display_message(f"❌ Error al actualizar matrícula: {resultado.get('error', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al actualizar matrícula: {str(e)}", is_success=False)

    def handle_eliminar_matricula(self, nna_id: int, unidad_id: int):
        """Maneja la eliminación y actualiza la vista."""
        if not self.vista or not nna_id or not unidad_id:
            self.vista.display_message("❌ ID de NNA y Unidad son obligatorios para eliminar.", is_success=False)
            return

        try:
            resultado = self.model.eliminar_matricula(nna_id, unidad_id)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ Matrícula eliminada correctamente", is_success=True)
                # Limpiar la selección de la matrícula (pero mantener NNA/Unidad)
                self.vista.limpiar_entradas(clean_nna_unidad=False) 
            else:
                self.vista.display_message(f"❌ Error al eliminar matrícula: {resultado.get('error', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al eliminar matrícula: {str(e)}", is_success=False)