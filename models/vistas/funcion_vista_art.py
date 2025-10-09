from models.articulos_model import ArticuloModelo
# from views.articulos_view import ArticuloVista # Asumo que ArticuloVista está definida
import tkinter as tk # Solo para referencia de tipo si usas Tkinter

# Define una clase stub simple para el ejemplo si no tienes ArticuloVista definida aquí
class ArticuloVista:
    def __init__(self):
        self.buscar_var = tk.StringVar()
    def establecer_eventos(self, **kwargs): pass
    def mostrar_mensaje(self, mensaje, color): print(f"[{color}] {mensaje}")
    def obtener_valores(self): 
        # Esta es una simulación de lo que la vista debería retornar
        return {
            "termino_busqueda": self.buscar_var.get(),
            "titulo_nombre": "",
            "capitulo_nombre": "",
            "numero_articulo": "",
            "descripcion": "",
            "texto": ""
        }
    def establecer_valores(self, **kwargs): pass
    def limpiar_entradas(self): pass
    def mostrar_literales(self, literales): pass # Nuevo método en la vista

# ----------------------------------------------------------------------

class ArticuloControlador:
    """
    Controlador que maneja la interacción entre el Modelo y la Vista.
    Contiene la lógica de la aplicación.
    """
    def __init__(self, modelo: ArticuloModelo, vista: ArticuloVista):
        self.modelo = modelo
        self.vista = vista
        
        self.articulo_original_num = None 
        
        self.vista.establecer_eventos(
            agregar_articulo=self.agregar_articulo,
            buscar_articulo=self.leer_articulo,
            modificar_articulo=self.modificar_articulo,
            eliminar_articulo=self.eliminar_articulo,
            # Nuevo evento para obtener literales
            obtener_literales=self.obtener_literales_del_articulo 
        )
        self.vista.mostrar_mensaje("¡Gestor de Artículos LOPNNA listo! (SQLite) Los datos persisten en 'lopnna.db'.")

    def _validar_campos_requeridos(self, data: dict) -> bool:
        """Verifica que los campos estén llenos."""
        if not data["numero_articulo"]:
            self.vista.mostrar_mensaje("Error: El número de artículo es obligatorio.", color="#FF5733")
            return False
        if not data["titulo_nombre"]:
            self.vista.mostrar_mensaje("Error: El campo Título es obligatorio.", color="#FF5733")
            return False
        if not data["capitulo_nombre"]:
            self.vista.mostrar_mensaje("Error: El campo Capítulo es obligatorio.", color="#FF5733")
            return False
        if not data["texto"]:
            self.vista.mostrar_mensaje("Error: El texto del artículo no puede estar vacío.", color="#FF5733")
            return False
        return True
# Fin de validar_campos_requeridos

    def agregar_articulo(self):
        """Lógica para crear un nuevo artículo, manejando la jerarquía Título/Capítulo."""
        data = self.vista.obtener_valores()
        
        if not self._validar_campos_requeridos(data):
            return
            
        self.articulo_original_num = None 

        # Insertar o buscar Título y obtener ID
        titulo_id = self.modelo.insertar_titulo(data["titulo_nombre"])
        if not titulo_id:
            self.vista.mostrar_mensaje("Error: No se pudo crear/obtener el ID del Título.", color="#FF5733")
            return

        # Insertar o buscar Capítulo y obtener ID
        capitulo_id = self.modelo.insertar_capitulo(titulo_id, data["capitulo_nombre"])
        if not capitulo_id:
            self.vista.mostrar_mensaje("Error: No se pudo crear/obtener el ID del Capítulo.", color="#FF5733")
            return
            
        # Insertar Artículo
        articulo_id = self.modelo.insertar_articulo(
            capitulo_id, 
            data["numero_articulo"], 
            data["descripcion"], 
            data["texto"]
        )

        if articulo_id:
            self.vista.mostrar_mensaje(f"Artículo N° {data['numero_articulo']} creado y guardado en SQLite.", color="#3CB371")
            self.vista.limpiar_entradas()
        else:
            self.vista.mostrar_mensaje(f"Error: El Artículo N° {data['numero_articulo']} ya existe en ese Capítulo.", color="#FF5733")
# Fin de agregar_articulo

    def leer_articulo(self):
        """
        Lógica para buscar y mostrar un artículo.
        CORRECCIÓN: La vista necesita el 'titulo_nombre' que el modelo no estaba retornando.
        """
        termino = self.vista.obtener_valores()["termino_busqueda"]
        
        if not termino:
            self.vista.mostrar_mensaje("Advertencia: Ingrese un número de artículo o una palabra clave para buscar.", color="#FFBF00")
            self.articulo_original_num = None
            return

        articulo_encontrado = self.modelo.buscar_articulo(termino)
        
        if articulo_encontrado:
            self.articulo_original_num = articulo_encontrado["numero_articulo"] 
            
            # Se añade el campo 'titulo_nombre' a los valores a establecer.
            self.vista.establecer_valores(
                # El modelo DEBE ser actualizado para devolver titulo_nombre
                titulo_nombre=articulo_encontrado.get("titulo_nombre", "N/A"), 
                capitulo_nombre=articulo_encontrado["capitulo_nombre"],
                numero_articulo=articulo_encontrado["numero_articulo"],
                descripcion=articulo_encontrado["descripcion"],
                texto=articulo_encontrado["texto"]
            )
            self.vista.mostrar_mensaje(
                f"🔍 Artículo N° {articulo_encontrado['numero_articulo']} encontrado y cargado.", 
                color="#219EBC"
            )
        else:
            self.vista.limpiar_entradas()
            self.vista.buscar_var.set(termino)
            self.articulo_original_num = None
            self.vista.mostrar_mensaje(f"Artículo o término '{termino}' no encontrado.", color="#FF5733")
# Fin de leer_articulo

    def modificar_articulo(self):
        """Lógica para modificar un artículo existente, manejando la jerarquía Título/Capítulo."""
        data = self.vista.obtener_valores()
        
        if not self._validar_campos_requeridos(data):
            return
            
        if not self.articulo_original_num:
            self.vista.mostrar_mensaje("Advertencia: Busque y cargue un artículo antes de intentar modificar.", color="#FFBF00")
            return
            
        # Insertar o buscar Título y Capítulo para obtener el ID de Capítulo actualizado
        titulo_id = self.modelo.insertar_titulo(data["titulo_nombre"])
        capitulo_id = self.modelo.insertar_capitulo(titulo_id, data["capitulo_nombre"])

        if not titulo_id or not capitulo_id:
            self.vista.mostrar_mensaje("Error: No se pudo obtener la jerarquía para la modificación.", color="#FF5733")
            return
            
        # Modificar Artículo
        if self.modelo.modificar_articulo(
            self.articulo_original_num, # Número de artículo en la DB
            capitulo_id,
            data["numero_articulo"], # Nuevo número de artículo (puede ser el mismo)
            data["descripcion"],
            data["texto"]
        ):
            self.vista.mostrar_mensaje(f"Artículo N° {data['numero_articulo']} modificado con éxito.", color="#FFA500")
            self.vista.limpiar_entradas()
            # Si el número de artículo cambió, se actualiza la referencia
            self.articulo_original_num = data["numero_articulo"] 
        else:
            self.vista.mostrar_mensaje("Error: Falló la modificación. Revise el número de artículo o la consola.", color="#FF5733")
# Fin de modificar_articulo

    def eliminar_articulo(self):
        """Lógica para eliminar un artículo existente."""
        data = self.vista.obtener_valores()
        numero_articulo = data["numero_articulo"]
        
        if not numero_articulo:
            self.vista.mostrar_mensaje("Error: Debe ingresar el Número de Artículo a eliminar.", color="#FF5733")
            return
            
        # Intentar eliminar en el Modelo
        if self.modelo.eliminar_articulo(numero_articulo):
            self.vista.mostrar_mensaje(f"Artículo N° {numero_articulo} eliminado con éxito.", color="#B80000")
            self.vista.limpiar_entradas()
            # Limpia la referencia si el artículo eliminado era el cargado.
            if self.articulo_original_num == numero_articulo:
                self.articulo_original_num = None 
        else:
            self.vista.mostrar_mensaje(f"Error: El Artículo N° {numero_articulo} no fue encontrado.", color="#FF5733")
# Fin de eliminar Artículo
            
    def obtener_literales_del_articulo(self):
        """
        Busca los literales de un artículo cargado y se los pasa a la vista para su despliegue.
        """
        numero_articulo = self.vista.obtener_valores()["numero_articulo"]
        
        if not numero_articulo:
            self.vista.mostrar_mensaje("Advertencia: Primero busque y cargue un artículo para ver sus literales.", color="#FFBF00")
            return
            
        literales = self.modelo.obtener_literales_por_articulo(numero_articulo)
        
        if literales:
            self.vista.mostrar_literales(literales)
            self.vista.mostrar_mensaje(f"Se cargaron {len(literales)} literales para el Art. {numero_articulo}.", color="#008080")
        else:
            # Pasa una lista vacía para limpiar cualquier despliegue anterior
            self.vista.mostrar_literales([]) 
            self.vista.mostrar_mensaje(f"El Artículo {numero_articulo} no tiene literales asociados.", color="#008080")
# Fin de obtener_literales_del_articulo