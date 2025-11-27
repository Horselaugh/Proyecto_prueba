import sys
import os
from typing import List, Dict, Any, Optional

# ----------------------------------------------------------------------
# Importación del Modelo Real
# ----------------------------------------------------------------------

# Añadir el directorio superior y el directorio actual al path para las importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
# Si 'models' no estuviera en el mismo nivel, se necesitaría un ajuste de path.
# Para este ejemplo, asumimos que todos los archivos están en el mismo directorio
# o que la estructura permite la importación directa.
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    # Intenta importar el modelo real.
    from models.unidad_educativa_model import UnidadEducativaModel
except ImportError:
    # Esto solo debería ocurrir en un entorno de ejecución específico.
    print("Error: No se pudo importar UnidadEducativaModel. Asegúrese de que 'unidad_educativa_model.py' y 'database_connector.py' estén disponibles.")
    # Si la importación falla, se podría usar un mock, pero el objetivo es usar el real.
    sys.exit(1) # Detener si no se puede inicializar el modelo.

# ----------------------------------------------------------------------
# Controlador
# ----------------------------------------------------------------------

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
            # Usar el método de listado completo del modelo
            resultado = self.model.listar_todas_unidades_educativas()
            
            if resultado['status'] == 'success':
                data = resultado.get('data', [])
                self.vista.display_list(data)
                self.vista.display_message(f"✅ Cargadas {len(data)} Unidades Educativas.", True)
            else:
                self.vista.display_list([])
                self.vista.display_message(f"❌ Error al cargar UE: {resultado.get('error', 'Desconocido')}", False)
        except Exception as e:
            self.vista.display_list([])
            self.vista.display_message(f"❌ Error interno al cargar datos: {str(e)}", False)

    def handle_crear_ue(self, data: Dict[str, Any]):
        """Crea una nueva Unidad Educativa."""
        if not self.vista: return
        
        # El modelo ya hace las validaciones obligatorias, solo llama.
        try:
            # El modelo necesita todos los campos definidos, usar .get() para seguridad
            nombre = data.get('nombre', '')
            director = data.get('director', '')
            tipo = data.get('tipo', '')
            telefono = data.get('telefono', '')
            direccion = data.get('direccion', '')

            resultado = self.model.crear_unidad_educativa(
                nombre=nombre, director=director, tipo=tipo, telefono=telefono, direccion=direccion)
                
            if resultado['status'] == 'success':
                self.vista.display_message(f"✅ {resultado['message']}", True)
                self.vista.limpiar_formulario()
                self.load_initial_data() # Refrescar lista
            else:
                self.vista.display_message(f"❌ Error al crear UE: {resultado.get('error', 'Desconocido')}", False)
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al crear UE: {str(e)}", False)

    def handle_buscar_ue(self, busqueda_id: Optional[int] = None, busqueda_nombre: Optional[str] = None):
        """Busca y muestra resultados en la vista."""
        if not self.vista: return

        try:
            resultado = None
            if busqueda_id is not None:
                # Búsqueda por ID
                resultado = self.model.buscar_unidad_educativa(id=busqueda_id)
            elif busqueda_nombre:
                # Búsqueda por Nombre (parcial)
                resultado = self.model.buscar_unidad_educativa(nombre=busqueda_nombre)
            else:
                # Si se llama sin parámetros, cargar todos (lo cual es redundante, pero por si acaso)
                self.load_initial_data()
                return

            if resultado is None:
                return

            if resultado['status'] == 'success':
                data = resultado.get('data', [])
                self.vista.display_list(data)
                if data:
                    self.vista.display_message(f"✅ Encontradas {len(data)} Unidades Educativas.", True)
                else:
                    self.vista.display_message("⚠️ No se encontraron Unidades Educativas con ese criterio.", False)
            else:
                self.vista.display_message(f"❌ Error al buscar UE: {resultado.get('error', 'Desconocido')}", False)
                self.vista.display_list([])
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al buscar UE: {str(e)}", False)
            self.vista.display_list([])

    def handle_cargar_ue_para_edicion(self, id_ue: int):
        """Obtiene una UE y pasa sus datos a la vista para edición."""
        if not self.vista: return
        
        try:
            resultado = self.model.buscar_unidad_educativa(id=id_ue)
            
            if resultado['status'] == 'success' and resultado.get('data'):
                # Los datos vienen como tipo 'PUBLICA' o 'PRIVADA' en mayúsculas desde el modelo/BD
                data = resultado['data'][0]
                # Asegurar que el 'tipo' sea Capitalizado para el ComboBox de la vista (ej: Pública)
                data['tipo'] = data.get('tipo', 'PÚBLICA').capitalize() 
                
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
            # El modelo maneja la validación de qué campos actualizar (solo si tienen valor)
            resultado = self.model.actualizar_unidad_educativa(id=id_ue, **data)
            
            if resultado['status'] == 'success':
                self.vista.display_message(f"✅ {resultado['message']}", True)
                self.vista.limpiar_formulario()
                self.load_initial_data() # Refrescar lista
            else:
                self.vista.display_message(f"❌ Error al actualizar UE: {resultado.get('error', 'Desconocido')}", False)
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al actualizar UE: {str(e)}", False)

    def handle_eliminar_ue(self, id_ue: int):
        """Elimina una Unidad Educativa."""
        if not self.vista: return

        try:
            # El modelo realiza la eliminación física (DELETE)
            resultado = self.model.eliminar_unidad_educativa(id_ue)
            
            if resultado['status'] == 'success':
                self.vista.display_message(f"🗑️ {resultado['message']}", True)
                self.vista.limpiar_formulario()
                self.load_initial_data() # Refrescar lista
            else:
                self.vista.display_message(f"❌ Error al eliminar UE: {resultado.get('error', 'Desconocido')}", False)
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al eliminar UE: {str(e)}", False)