import sys
import os
from typing import Dict, List, Optional
import datetime
import hashlib

# Configuraciones de Path e importación del Modelo real
try:
    # Intenta importar el modelo real
    from models.personal_model import PersonalModel
except ImportError:
    # Mock si el modelo real no se encuentra (MANTENER MOCK SOLO POR SI ACASO, PERO EL CÓDIGO USA EL REAL)
    class MockPersonalModel:
        # --- MOCK ACTUALIZADO PARA COINCIDIR CON LOS CAMPOS COMPLETOS DEL MODELO ---
        def obtener_por_id(self, id):
            if id == 1:
                return {
                    "persona_id": 1, "documento_identidad": "V12345678", "primer_nombre": "Juan", 
                    "segundo_nombre": "Carlos", "primer_apellido": "Pérez", 
                    "segundo_apellido": "Rojas", "telefono": "04141234567",
                    "direccion": "Calle Falsa 123", "genero": "M", # En modelo se guarda M/F/O
                    "cargo": 1, "resolucion": "N/A", "nombre_usuario": "jperez", "activo": True
                }
            return None
            
        def obtener_por_cedula(self, cedula):
            if cedula == "V12345678":
                return self.obtener_por_id(1)
            return None
            
        def agregar_personal(self, datos): return 2
        
        # El modelo ahora acepta el diccionario de datos completo
        def actualizar_personal(self, data): return True 
        
        def eliminar_personal(self, id): return True
        def listar_generos(self): return ["Femenino", "Masculino", "Otro"]
        def listar_cargos(self): return [{"id": 1, "nombre": "Coordinador"}, {"id": 2, "nombre": "Secretario"}]
        
    PersonalModel = MockPersonalModel
    
    
class PersonalControlador:
    """Controlador para gestionar las operaciones de Personal"""

    def __init__(self):
        self.model = PersonalModel()
        self.vista = None
        
        # Mapeos internos para conversión (Nombre de Cargo <-> ID, Nombre de Género <-> Código)
        self.cargo_map: Dict[str, int] = {}
        # 💡 CORRECCIÓN/ADICIÓN: Mapeo inverso de cargos (útil para cargar datos)
        self.cargo_reverse_map: Dict[int, str] = {} 
        
        # Mapeo de género: La base de datos solo acepta M/F/O.
        self.genero_map: Dict[str, str] = {"Femenino": "F", "Masculino": "M", "Otro": "O"}
        self.genero_reverse_map: Dict[str, str] = {v: k for k, v in self.genero_map.items()}

    def set_view(self, view_instance):
        """Establece la instancia de la vista."""
        self.vista = view_instance

    def load_initial_data(self):
        """Carga inicial de datos al mostrar la vista (cargos y géneros)."""
        if not self.vista: return
        
        try:
            # Cargar y mapear Cargos
            cargos_list = self.model.listar_cargos()
            self.cargo_map = {c['nombre']: c['id'] for c in cargos_list}
            # 💡 CORRECCIÓN: Inicializar el mapeo inverso aquí
            self.cargo_reverse_map = {c['id']: c['nombre'] for c in cargos_list}
            self.vista._cargar_cargos([c['nombre'] for c in cargos_list])
            
            # Cargar Géneros directamente del mapeo del controlador
            generos_list = list(self.genero_map.keys()) # Obtiene ['Femenino', 'Masculino', 'Otro']
            self.vista._cargar_generos(generos_list)
            
            self.vista.display_message("Listo para gestionar Personal. 🛠️", is_success=True)
            
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar datos iniciales: {str(e)}", is_success=False)

    # --- MÉTODOS DE MANEJO DE EVENTOS (Handle Methods) ---

    def _validar_datos(self, data: Dict, is_update: bool = False) -> bool:
        """Valida la presencia de datos críticos."""
        obligatorios = ['cedula', 'primer_nombre', 'primer_apellido', 'telefono', 'nombre_usuario']
        
        # La contraseña es obligatoria solo en la creación
        if not is_update and not data.get('password'):
            self.vista.display_message("❌ La contraseña es obligatoria para el registro.", is_success=False)
            return False
            
        # 💡 CORRECCIÓN: Usar 'documento_identidad' como clave si fuera necesario, pero la vista envía 'cedula'. Mantenemos 'cedula' por consistencia con la vista.
        if not all(data.get(k) for k in obligatorios):
            self.vista.display_message("❌ Cédula, Nombre, Apellido, Teléfono y Usuario son obligatorios.", is_success=False)
            return False
            
        if not data.get('cargo') or data.get('cargo') not in self.cargo_map:
            self.vista.display_message("❌ Debe seleccionar un Cargo válido.", is_success=False)
            return False
            
        return True

    def _hashear_password(self, password: str) -> str:
        """Función dummy para hashear la contraseña antes de enviarla al modelo."""
        # Nota: La codificación hash.sha256() es correcta para simular un hash simple.
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def handle_crear_personal(self, data: Dict):
        """Maneja la creación y actualiza la vista."""
        if not self.vista or not self._validar_datos(data): return
        
        try:
            # Mapear datos a formato de modelo
            data['cargo'] = self.cargo_map[data['cargo']]
            data['genero'] = self.genero_map.get(data['genero'], "O") # Mapear nombre de género a código (M/F/O)
            
            # Corrección: Hashear la contraseña antes de enviarla al Modelo
            data['password'] = self._hashear_password(data['password']) 
            
            # 💡 Corrección: El modelo espera 'cedula' pero la BD usa 'documento_identidad'.
            # Mantenemos 'cedula' aquí ya que la vista lo usa y el modelo lo maneja.
            # No se necesita una corrección aquí ya que el modelo lo extrae de `datos["cedula"]`.
            
            persona_id = self.model.agregar_personal(data)
            
            if persona_id:
                self.vista.display_message(f"✅ Personal '{data['primer_nombre']} {data['primer_apellido']}' registrado (ID: {persona_id}).", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ Error al registrar personal. La Cédula o Usuario pueden ya existir.", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al crear personal: {str(e)}", is_success=False)

    def handle_cargar_personal(self, id_or_cedula: str):
        """Busca personal por ID o Cédula y carga sus datos en la vista."""
        if not self.vista: return
        
        try:
            resultado = None
            if id_or_cedula.isdigit():
                resultado = self.model.obtener_por_id(int(id_or_cedula)) 
            else:
                # Llamar a la función obtener_por_cedula en el modelo
                resultado = self.model.obtener_por_cedula(id_or_cedula)
            
            if resultado:
                # Conversión de datos para la vista:
                
                # 1. Obtener nombre del cargo
                # 💡 CORRECCIÓN: Usar el mapeo inverso (self.cargo_reverse_map)
                cargo_nombre = self.cargo_reverse_map.get(resultado['cargo'], "Desconocido")
                resultado['cargo_nombre'] = cargo_nombre # Nueva clave que la vista espera
                
                # 2. Obtener nombre completo del género
                resultado['genero'] = self.genero_reverse_map.get(resultado['genero'], resultado['genero'])
                
                # Asignar la clave 'id' para que la vista lo use
                resultado['id'] = resultado['persona_id'] 
                
                # La vista espera 'documento_identidad' para la variable 'cedula_var'
                
                self.vista.display_message(f"✅ Personal '{resultado['primer_nombre']} {resultado['primer_apellido']}' cargado.", is_success=True)
                self.vista._establecer_datos_formulario(resultado)
            else:
                self.vista.display_message(f"❌ No se encontró Personal con ID/Cédula: {id_or_cedula}", is_success=False)
                self.vista.limpiar_entradas(clean_search=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar personal: {str(e)}", is_success=False)


    def handle_actualizar_personal(self, data: Dict):
        """Maneja la actualización y actualiza la vista."""
        personal_id = data.get('id')
        
        # Manejar el hash de la contraseña si se modificó
        password_raw = data.get('password')
        if password_raw == "********":
            data.pop('password', None) # No enviar la contraseña al modelo
        elif password_raw:
            data['password'] = self._hashear_password(password_raw)
            
        if not self.vista or not personal_id or not self._validar_datos(data, is_update=True): return
        
        try:
            # Mapear datos a formato de modelo antes de actualizar
            data['cargo'] = self.cargo_map[data['cargo']]
            data['genero'] = self.genero_map.get(data['genero'], "O") # Mapear nombre de género a código (M/F/O)
            
            # El modelo espera 'persona_id'
            data['persona_id'] = personal_id 
            
            # Corrección: Pasar el diccionario de datos completo al modelo
            resultado = self.model.actualizar_personal(data) 
            
            if resultado: 
                self.vista.display_message(f"✅ Personal ID {personal_id} actualizado.", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ Error al actualizar personal. Verifique si el registro existe.", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al actualizar personal: {str(e)}", is_success=False)

    def handle_eliminar_personal(self, personal_id: int):
        """Maneja la eliminación y actualiza la vista."""
        if not self.vista or not personal_id:
            self.vista.display_message("❌ ID del Personal es obligatorio para eliminar.", is_success=False)
            return

        try:
            resultado = self.model.eliminar_personal(personal_id)
            
            if resultado:
                self.vista.display_message(f"✅ Personal ID {personal_id} eliminado correctamente", is_success=True)
                self.vista.limpiar_entradas()
            else:
                self.vista.display_message(f"❌ Error al eliminar personal.", is_success=False)
                
        except Exception as e:
            self.vista.display_message(f"❌ Error interno al eliminar personal: {str(e)}", is_success=False)