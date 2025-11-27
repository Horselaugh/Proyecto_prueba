import sys
import os
from typing import Dict, Any, Optional, TYPE_CHECKING
from tkinter import messagebox # Se puede usar para confirmaciones/mensajes de error graves


# sys.path.append(os.path.join(os.path.dirname(__file__))) 

# Se importa el modelo real (asumiendo que está disponible)
try:
    from models.configuracion_model import ConfiguracionModel
except ImportError:
    # Fallback o manejo de error si el modelo no está en el path
    print("Error: No se pudo importar ConfiguracionModel.")
    sys.exit(1)

# Se usa TYPE_CHECKING para evitar dependencias circulares en tiempo de ejecución
if TYPE_CHECKING:
    # Importar el tipo de la vista solo para anotaciones de tipo
    from views.configuracion_view import ConfiguracionViewFrame

class ConfiguracionControlador:
    """
    Controlador para el módulo de configuración.
    Actúa como intermediario entre la Vista (ConfiguracionViewFrame) y el Modelo (ConfiguracionModel).
    Contiene la lógica de negocio y validación.
    """

    def __init__(self):
        # El controlador crea una instancia del modelo.
        self.modelo = ConfiguracionModel()
        self.vista: Optional['ConfiguracionViewFrame'] = None

    def set_view(self, view_instance: 'ConfiguracionViewFrame'):
        """Inyecta la instancia de la Vista en el Controlador."""
        self.vista = view_instance

    def get_rol_id_from_str(self, rol_str: str) -> Optional[int]:
        """
        Extrae el ID numérico del rol desde la cadena de la Vista (e.g., '1 - Admin').
        Esta lógica debe residir en el Controlador o Modelo, no en la Vista.
        """
        if not rol_str or ' - ' not in rol_str:
            return None
        try:
            # El ID es el primer elemento antes del ' - '
            return int(rol_str.split(' - ')[0])
        except ValueError:
            return None

    def get_rol_id_from_nombre(self, rol_nombre: str) -> Optional[int]:
        """Busca el ID de un rol basado en su nombre."""
        roles = self.modelo.obtener_todos_los_roles()
        for rol in roles:
            if rol['nombre'] == rol_nombre:
                return rol['id']
        return None


    def load_initial_data(self):
        """Carga los datos iniciales (roles y usuarios) en la vista."""
        if self.vista:
            try:
                roles = self.modelo.obtener_todos_los_roles()
                # Convertir los objetos Row a diccionarios para la vista si es necesario
                roles_dict = [dict(r) for r in roles]
                
                usuarios = self.modelo.obtener_todos_los_usuarios()
                # Convertir los objetos Row a diccionarios para la vista si es necesario
                usuarios_dict = [dict(u) for u in usuarios]
                
                # Delegar la presentación de datos a la Vista
                self.vista._cargar_roles(roles_dict)
                self.vista._cargar_usuarios(usuarios_dict)
                self.vista.display_message("✅ Datos de Configuración cargados.", is_success=True)
            except Exception as e:
                self.vista.display_message(f"❌ Error al cargar datos iniciales: {e}", is_success=False)
                print(f"Error: {e}")

    # ======================================================================
    # HANDLERS DE ROLES
    # ======================================================================

    def _validar_rol_data(self, data: Dict[str, str]) -> bool:
        """Validación de negocio del lado del Controlador."""
        if not data.get('nombre') or not data.get('descripcion'):
            if self.vista:
                self.vista.display_message("❌ Error: Nombre y descripción del rol son obligatorios.", is_success=False)
            return False
        return True

    def handle_crear_rol(self, data: Dict[str, str]):
        """Maneja la solicitud de creación de un rol."""
        if not self._validar_rol_data(data): return
        
        # Lógica de negocio/Modelo
        rol_id = self.modelo.insertar_rol(data['nombre'], data['descripcion'])
        
        if self.vista:
            if rol_id is not None:
                self.vista.display_message(f"✅ Rol '{data['nombre']}' creado con ID: {rol_id}.", is_success=True)
                self.vista._limpiar_campos_rol(clear_selection=True)
                self.load_initial_data()
            else:
                self.vista.display_message(f"❌ Error: El rol '{data['nombre']}' ya existe o hubo un error en DB.", is_success=False)

    def handle_guardar_rol(self, data: Dict[str, Any]):
        """Maneja la solicitud de modificación de un rol."""
        if not self._validar_rol_data(data) or data.get('id') is None: 
            if self.vista: self.vista.display_message("❌ Error: ID de rol inválido o datos incompletos.", is_success=False)
            return

        rol_id = data['id']
        
        if self.modelo.modificar_rol(rol_id, data['nombre'], data['descripcion']):
            if self.vista:
                self.vista.display_message(f"✅ Rol '{data['nombre']}' guardado.", is_success=True)
                self.vista._limpiar_campos_rol(clear_selection=True)
                self.load_initial_data()
        else:
            if self.vista:
                self.vista.display_message(f"❌ Error: No se pudo guardar el rol (posiblemente nombre duplicado).", is_success=False)

    def handle_eliminar_rol(self, rol_id: int, nombre_rol: str):
        """Maneja la solicitud de eliminación de un rol."""
        if not rol_id:
            if self.vista: self.vista.display_message("❌ Error: ID de rol inválido para eliminar.", is_success=False)
            return
            
        # Lógica: Evitar eliminación de roles con usuarios asociados (Lógica de negocio simple)
        # Nota: En este mock, el modelo no tiene la lógica para verificar esto, solo la DB
        
        if self.modelo.eliminar_rol(rol_id):
            if self.vista:
                self.vista.display_message(f"🗑️ Rol '{nombre_rol}' eliminado.", is_success=True)
                self.vista._limpiar_campos_rol(clear_selection=True)
                self.load_initial_data()
        else:
            if self.vista:
                self.vista.display_message(f"❌ Error al eliminar el rol '{nombre_rol}'.", is_success=False)

    # ======================================================================
    # HANDLERS DE USUARIOS
    # ======================================================================

    def _validar_usuario_data(self, data: Dict[str, Any]) -> bool:
        """Validación de negocio del lado del Controlador para usuarios."""
        if not data.get('primer_nombre') or not data.get('documento') or not data.get('apellido') or not data.get('rol_id'):
            if self.vista:
                self.vista.display_message("❌ Error: Nombre, Apellido, Documento y Rol son obligatorios.", is_success=False)
            return False
        return True

    def _prepare_usuario_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepara los datos del formulario de la vista para el modelo."""
        # Se obtiene el ID de rol a partir de la cadena de la vista
        rol_id = self.get_rol_id_from_str(data['rol_str']) 
        
        # Construcción del diccionario de datos que el modelo espera
        return {
            'persona_id': data.get('id'), # None en creación
            'rol_id': rol_id,
            # El modelo solo necesita los 4 nombres, documento y dirección para la tabla 'persona'.
            'primer_nombre': data['primer_nombre'],
            'segundo_nombre': data.get('segundo_nombre', ''), # La vista solo tiene 1 apellido y 1 nombre
            'primer_apellido': data['apellido'],
            'segundo_apellido': data.get('segundo_apellido', ''),
            'documento_identidad': data['documento'],
            'direccion': data.get('direccion', 'Dirección no especificada'),
            'nombre_usuario_anterior': data.get('nombre_usuario_anterior', '')
            # Los demás campos (genero, telefono, resolucion, contraseña) los maneja el modelo con valores por defecto
        }

    def handle_crear_usuario(self, data: Dict[str, Any]):
        """Maneja la solicitud de creación de un usuario."""
        datos_para_modelo = self._prepare_usuario_data({'rol_str': data['rol_str'], **data})

        if not self._validar_usuario_data(datos_para_modelo): return

        try:
            persona_id = self.modelo.insertar_usuario(datos_para_modelo)
            if self.vista:
                self.vista.display_message(f"✅ Usuario '{datos_para_modelo['primer_nombre']}' creado con ID: {persona_id}.", is_success=True)
                self.vista._limpiar_campos_usuario(clear_selection=True)
                self.load_initial_data()
        except ValueError as e:
            # Manejo de errores de unicidad del modelo
            if self.vista:
                self.vista.display_message(f"❌ Error de unicidad: {e}.", is_success=False)
        except Exception as e:
            if self.vista:
                self.vista.display_message(f"❌ Error al crear usuario: {e}.", is_success=False)
            print(f"Error: {e}")

    def handle_guardar_usuario(self, data: Dict[str, Any]):
        """Maneja la solicitud de modificación de un usuario."""
        if data.get('id') is None:
            if self.vista: self.vista.display_message("❌ Error: ID de usuario inválido.", is_success=False)
            return
            
        datos_para_modelo = self._prepare_usuario_data({'rol_str': data['rol_str'], **data})

        if not self._validar_usuario_data(datos_para_modelo): return
        
        try:
            if self.modelo.modificar_usuario(datos_para_modelo):
                if self.vista:
                    self.vista.display_message(f"✅ Usuario '{datos_para_modelo['primer_nombre']}' guardado.", is_success=True)
                    self.vista._limpiar_campos_usuario(clear_selection=True)
                    self.load_initial_data()
            else:
                if self.vista:
                    self.vista.display_message(f"❌ Error: No se pudo guardar el usuario.", is_success=False)
        except ValueError as e:
            # Manejo de errores de unicidad del modelo
            if self.vista:
                self.vista.display_message(f"❌ Error de unicidad: {e}.", is_success=False)
        except Exception as e:
            if self.vista:
                self.vista.display_message(f"❌ Error al modificar usuario: {e}.", is_success=False)
            print(f"Error: {e}")

    def handle_eliminar_usuario(self, persona_id: int, nombre_usuario: str):
        """Maneja la solicitud de eliminación de un usuario."""
        if not persona_id:
            if self.vista: self.vista.display_message("❌ Error: ID de usuario inválido para eliminar.", is_success=False)
            return
            
        # Lógica: El modelo se encarga de eliminar la persona, y las claves foráneas
        # con ON DELETE CASCADE se encargarán de eliminar las entradas en 'personal' y 'persona_rol'.
        
        if self.modelo.eliminar_usuario(persona_id):
            if self.vista:
                self.vista.display_message(f"🗑️ Usuario '{nombre_usuario}' eliminado.", is_success=True)
                self.vista._limpiar_campos_usuario(clear_selection=True)
                self.load_initial_data()
        else:
            if self.vista:
                self.vista.display_message(f"❌ Error al eliminar el usuario '{nombre_usuario}'.", is_success=False)