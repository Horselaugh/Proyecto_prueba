import sys
import os
from typing import Dict, List, Optional
import datetime

# Configuraciones de Path e importación del Modelo real o Mock
try:
    from models.matricula_model import MatriculaModel
    # Asumir que el modelo tiene métodos para NNA, Unidades y Grados
except ImportError:
    # Si el modelo real no existe, usamos un mock para la simulación
    class MockMatriculaModel:
        def obtener_nna(self): return [{"id": 101, "nombre_completo": "Ana Torres"}]
        def obtener_unidades_educativas(self): return [{"id": 201, "nombre": "UE Simón Bolívar"}]
        def listar_grados(self): return ["1er Grado", "2do Grado"]
        def crear_matricula(self, **kwargs): 
            return {"status": "success", "message": "Matrícula creada (Mock)", "nna_id": kwargs['nna_id'], "unidad_id": kwargs['unidad_id']}
        def buscar_matricula(self, nna_id, unidad_id):
            if nna_id == 101 and unidad_id == 201:
                return [{
                    "nna_id": 101, "nna_nombre": "Ana Torres",
                    "unidad_id": 201, "unidad_nombre": "UE Simón Bolívar", 
                    "grado": "1er Grado", "fecha_matricula": "2024-09-15", 
                    "activa": True
                }]
            return []
        def actualizar_matricula(self, nna_id, unidad_id, **kwargs): return {"status": "success", "message": f"Matrícula {nna_id}-{unidad_id} actualizada (Mock)"}
        def eliminar_matricula(self, nna_id, unidad_id): return {"status": "success", "message": f"Matrícula {nna_id}-{unidad_id} eliminada (Mock)"}
        
    MatriculaModel = MockMatriculaModel
    
    
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
            nna_list = self.model.obtener_nna()
            unidad_list = self.model.obtener_unidades_educativas()
            grados_list = self.model.listar_grados()
            
            self.vista._cargar_comboboxes(nna_list, unidad_list, grados_list)
            self.vista.display_message("Seleccione un NNA y una Unidad Educativa. 🎓", is_success=True)
            
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar datos iniciales: {str(e)}", is_success=False)

    # --- MÉTODOS DE MANEJO DE EVENTOS (Handle Methods) ---

    def _validar_datos_comunes(self, data: Dict) -> bool:
        """Valida la presencia de datos críticos."""
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
                self.vista.display_message(f"❌ Error al crear matrícula: {resultado.get('message', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al crear matrícula: {str(e)}", is_success=False)

    def handle_buscar_matricula(self, nna_id: int, unidad_id: int):
        """Busca una matrícula específica y carga sus datos en la vista."""
        if not self.vista or not nna_id or not unidad_id: 
            self.vista.limpiar_entradas(clean_nna_unidad=False)
            return
            
        try:
            resultados = self.model.buscar_matricula(nna_id=nna_id, unidad_id=unidad_id) 
            
            if resultados:
                data = resultados[0] # Asumimos que solo debería haber una matrícula activa NNA-Unidad
                self.vista.display_message(f"✅ Matrícula encontrada. Grado: {data['grado']}", is_success=True)
                self.vista._establecer_datos_formulario(data)
            else:
                self.vista.display_message("ℹ️ No hay matrícula activa para esta combinación. Puede crear una.", is_success=True)
                self.vista.limpiar_entradas(clean_nna_unidad=False) # Limpia campos de matrícula, mantiene selección
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al buscar matrícula: {str(e)}", is_success=False)


    def handle_actualizar_matricula(self, data: Dict):
        """Maneja la actualización y actualiza la vista."""
        nna_id = data.get('nna_id')
        unidad_id = data.get('unidad_id')
        
        if not self.vista or not nna_id or not unidad_id or not self._validar_datos_comunes(data): return
        
        try:
            # Clonar data y eliminar IDs para pasarlo como kwargs
            update_data = {k: v for k, v in data.items() if k not in ['nna_id', 'unidad_id']}
            resultado = self.model.actualizar_matricula(nna_id, unidad_id, **update_data)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ Matrícula de NNA {nna_id} actualizada.", is_success=True)
                self.vista.limpiar_entradas(clean_nna_unidad=False) # Limpia campos de matrícula, mantiene selección
            else:
                self.vista.display_message(f"❌ Error al actualizar matrícula: {resultado.get('message', 'Desconocido')}", is_success=False)
                
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
                self.vista.limpiar_entradas(clean_nna_unidad=False) # Limpia campos de matrícula, mantiene selección
            else:
                self.vista.display_message(f"❌ Error al eliminar matrícula: {resultado.get('message', 'Desconocido')}", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al eliminar matrícula: {str(e)}", is_success=False)