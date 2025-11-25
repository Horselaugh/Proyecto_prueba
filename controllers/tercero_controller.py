# controllers/tercero_controller.py

from models.tercero_model import TerceroModel

class TerceroController:
    """
    Controlador para gestionar la creación y consulta de Terceros.
    """

    RELACIONES_VALIDAS = ['VECINO', 'DOCENTE', 'ENTIDAD_JURIDICA', 'OTRO']
    GENEROS_VALIDOS = ['M', 'F']
    
    def __init__(self):
        self.model = TerceroModel()

    def obtener_lista_relaciones(self):
        """
        Retorna la lista de tipos de relación NNA que se puede usar en la vista.
        """
        return self.RELACIONES_VALIDAS

    def registrar_tercero(self, datos_formulario):
        """
        Valida los datos y llama al modelo para registrar un nuevo tercero.
        
        :param datos_formulario: Diccionario con todos los datos de persona y la relación_nna.
        :return: (bool, mensaje)
        """
        
        # --- 1. Validación de Datos Obligatorios ---
        campos_obligatorios = ['documento_identidad', 'primer_nombre', 'primer_apellido', 'genero', 'direccion', 'telefono', 'relacion_nna']
        for campo in campos_obligatorios:
            if not datos_formulario.get(campo):
                return False, f"El campo '{campo}' es obligatorio."

        # --- 2. Validación de Catálogos ---
        if datos_formulario['genero'].upper() not in self.GENEROS_VALIDOS:
            return False, "El género debe ser 'M' (Masculino) o 'F' (Femenino)."
            
        relacion = datos_formulario['relacion_nna'].upper()
        if relacion not in self.RELACIONES_VALIDAS:
            return False, f"Tipo de relación no válida. Debe ser una de: {', '.join(self.RELACIONES_VALIDAS)}"
            
        # --- 3. Preparación de Datos ---
        datos_persona = {
            'documento_identidad': datos_formulario['documento_identidad'],
            'primer_nombre': datos_formulario['primer_nombre'],
            'segundo_nombre': datos_formulario.get('segundo_nombre', ''),
            'primer_apellido': datos_formulario['primer_apellido'],
            'segundo_apellido': datos_formulario.get('segundo_apellido', ''),
            'genero': datos_formulario['genero'].upper(),
            'direccion': datos_formulario['direccion'],
            'telefono': datos_formulario['telefono']
        }
        
        # --- 4. Llamada al Modelo ---
        persona_id, mensaje = self.model.crear_tercero(datos_persona, relacion)
        
        if persona_id:
            return True, f"Tercero registrado con ID: {persona_id}. {mensaje}"
        else:
            return False, mensaje


    def listar_terceros(self):
        """
        Obtiene la lista completa de terceros registrados.
        """
        try:
            terceros = self.model.obtener_terceros()
            return terceros
        except Exception as e:
            print(f"[ERROR_CTRL] Error al listar terceros: {e}")
            return []