import sys
import os
from typing import Dict, Optional

sys.path.append(os.path.join(os.path.dirname(__file__))) 

try:
    from models.articulo_model import ArticuloModelo
except ImportError as e:
    raise ImportError(f"No se pudo importar ArticuloModelo: {e}")
    
    
class ArticuloControlador:
    """Controlador para gestionar las operaciones de Artículos LOPNNA"""

    def __init__(self):
        self.model = ArticuloModelo()
        self.vista = None

    def set_view(self, view_instance):
        """Establece la instancia de la vista para que el controlador pueda interactuar con ella."""
        self.vista = view_instance

    def load_initial_data(self):
        """Carga inicial de datos al mostrar la vista (solo un mensaje de estado en este caso)."""
        if self.vista:
            self.vista.display_message("Listo para gestionar Artículos LOPNNA. Use el campo de búsqueda para empezar. 🔎", is_success=True)

    # --- MÉTODOS DE MANEJO DE EVENTOS (Handle Methods) ---

    def handle_crear_articulo(self, codigo: str, articulo: str, descripcion: str):
        """Maneja la creación y actualiza la vista."""
        if not self.vista: return
        
        if not codigo or not articulo or not descripcion:
            self.vista.display_message("❌ Código, artículo y descripción son obligatorios", is_success=False)
            return

        try:
            articulo_id = self.model.insertar_articulo(codigo, articulo, descripcion)
            
            if articulo_id:
                self.vista.display_message(f"✅ Artículo '{codigo}' creado correctamente.", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ No se pudo crear el artículo. El código '{codigo}' ya existe.", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al crear artículo: {str(e)}", is_success=False)

    def handle_buscar_articulo(self, termino_busqueda: str):
        """Maneja la búsqueda y actualiza la vista con el resultado."""
        if not self.vista: return
        
        if not termino_busqueda:
            self.vista.display_message("❌ Término de búsqueda es obligatorio.", is_success=False)
            self.vista.limpiar_entradas()
            return
            
        try:
            resultado = self.model.buscar_articulo(termino_busqueda)
            
            if resultado:
                articulo_data = {
                    "id": resultado["id"],
                    "codigo": resultado["codigo"],
                    "articulo": resultado["articulo"],
                    "descripcion": resultado["descripcion"]
                }
                
                self.vista.display_message(f"✅ Artículo encontrado: {resultado['codigo']}", is_success=True)
                self.vista._establecer_datos_formulario(articulo_data)
            else:
                self.vista.display_message(f"❌ No se encontró ningún artículo con: '{termino_busqueda}'", is_success=False)
                self.vista.limpiar_entradas()
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al buscar artículo: {str(e)}", is_success=False)

    def handle_modificar_articulo(self, articulo_id: int, codigo: str, articulo: str, descripcion: str):
        """Maneja la actualización y actualiza la vista."""
        if not self.vista: return

        if not articulo_id or not codigo or not articulo or not descripcion:
            self.vista.display_message("❌ Todos los campos y el ID del artículo son obligatorios para modificar.", is_success=False)
            return
        
        try:
            exito = self.model.modificar_articulo(articulo_id, codigo, articulo, descripcion)
            
            if exito:
                self.vista.display_message(f"✅ Artículo '{codigo}' actualizado correctamente", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ No se pudo actualizar el artículo. El código '{codigo}' ya existe o el ID no es válido.", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al actualizar artículo: {str(e)}", is_success=False)

    def handle_eliminar_articulo(self, articulo_id: int):
        """Maneja la eliminación y actualiza la vista."""
        if not self.vista: return
        
        if not articulo_id:
            self.vista.display_message("❌ ID del artículo es obligatorio para eliminar.", is_success=False)
            return

        try:
            exito = self.model.eliminar_articulo(articulo_id)
            
            if exito:
                self.vista.display_message(f"✅ Artículo ID {articulo_id} eliminado correctamente", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ No se pudo eliminar el artículo ID {articulo_id}. Verifique que exista.", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al eliminar artículo: {str(e)}", is_success=False)