# controllers/relacion_controller.py

from models.relacion_model import RelacionNNAFamiliarModel
from models.nna_model import NNAModel 
from models.familiar_model import FamiliarModel 

class RelacionNNAFamiliarController:
    """
    Controlador para gestionar la creación y consulta de vínculos entre NNA y familiares.
    """

    def __init__(self):
        self.model = RelacionNNAFamiliarModel()
        self.nna_model = NNAModel() 
        self.familiar_model = FamiliarModel() 

    def obtener_parentescos_disponibles(self):
        """
        Retorna la lista de parentescos disponibles para el menú/combobox.
        """
        try:
            parentescos = self.model.obtener_parentescos()
            return parentescos
        except Exception as e:
            print(f"[ERROR_CTRL] No se pudieron cargar los parentescos: {e}")
            return []

    def crear_nueva_relacion(self, nna_id, familiar_id, parentesco_id, convive_str):
        """
        Valida los datos y llama al modelo para crear una nueva relación.
        
        :param nna_id: ID del NNA.
        :param familiar_id: ID del Familiar.
        :param parentesco_id: ID del Parentesco (catálogo).
        :param convive_str: 'Sí' o 'No'.
        :return: (bool, mensaje)
        """
        # --- 1. Validación y Conversión ---
        try:
            nna_id = int(nna_id)
            familiar_id = int(familiar_id)
            parentesco_id = int(parentesco_id)
        except ValueError:
            return False, "Los IDs de NNA, Familiar y Parentesco deben ser números enteros."
        
        if nna_id <= 0 or familiar_id <= 0 or parentesco_id <= 0:
            return False, "IDs no válidos."
        
        # Conversión del string a valor booleano (0 o 1 para SQLite)
        convive_bool = 1 if convive_str.upper() == 'SÍ' else 0
        
        # --- 2. Lógica del Negocio (ejemplo: no relacionarse a sí mismo) ---
        if nna_id == familiar_id:
            return False, "Un NNA no puede ser su propio familiar."
            
        # --- 3. Llamada al Modelo ---
        exito, mensaje = self.model.crear_relacion(nna_id, familiar_id, parentesco_id, convive_bool)
        return exito, mensaje

    def listar_relaciones_de_nna(self, nna_id):
        """
        Obtiene la lista de relaciones para un NNA específico.
        """
        try:
            nna_id = int(nna_id)
            relaciones = self.model.obtener_relaciones_por_nna(nna_id)
            return relaciones
        except ValueError:
            return []
        except Exception as e:
            print(f"[ERROR_CTRL] Error al listar relaciones para NNA {nna_id}: {e}")
            return []