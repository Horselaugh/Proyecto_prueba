import sys
import os
# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.articulo_model import ArticuloModelo
from sqlite3 import Row
from typing import List, Dict, Optional

class GestionArticulosControlador:
    """Controlador para gestionar las operaciones de Artículos LOPNNA"""

    def __init__(self):
        self.model = ArticuloModelo()

    def crear_articulo(self, codigo: str, articulo: str, descripcion: str) -> Dict:
        """Crea un nuevo artículo en la base de datos"""
        try:
            if not codigo or not articulo or not descripcion:
                return {
                    "status": "error", 
                    "message": "❌ Código, artículo y descripción son obligatorios"
                }
            
            articulo_id = self.model.insertar_articulo(codigo, articulo, descripcion)
            
            if articulo_id:
                return {
                    "status": "success",
                    "message": f"✅ Artículo '{codigo}' creado correctamente",
                    "id": articulo_id
                }
            else:
                return {
                    "status": "error",
                    "message": f"❌ No se pudo crear el artículo. El código '{codigo}' ya existe."
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error al crear artículo: {str(e)}"
            }

    def listar_articulos(self) -> Dict:
        """Obtiene todos los artículos de la base de datos"""
        try:
            articulos = self.model.obtener_todos_los_articulos()
            
            if articulos:
                # Convertir los objetos Row a diccionarios para mejor manejo
                articulos_list = []
                for articulo in articulos:
                    articulos_list.append({
                        "id": articulo["id"],
                        "codigo": articulo["codigo"],
                        "articulo": articulo["articulo"],
                        "descripcion": articulo["descripcion"]
                    })
                
                return {
                    "status": "success",
                    "data": articulos_list,
                    "message": f"✅ Se encontraron {len(articulos_list)} artículos"
                }
            else:
                return {
                    "status": "success",
                    "data": [],
                    "message": "ℹ️ No se encontraron artículos en la base de datos"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error al listar artículos: {str(e)}"
            }

    def buscar_articulo(self, termino_busqueda: str) -> Dict:
        """Busca un artículo por código, nombre o descripción"""
        try:
            if not termino_busqueda:
                return {
                    "status": "error",
                    "message": "❌ Término de búsqueda es obligatorio"
                }
            
            resultado = self.model.buscar_articulo(termino_busqueda)
            
            if resultado:
                articulo_data = {
                    "id": resultado["id"],
                    "codigo": resultado["codigo"],
                    "articulo": resultado["articulo"],
                    "descripcion": resultado["descripcion"]
                }
                
                return {
                    "status": "success",
                    "data": articulo_data,
                    "message": f"✅ Artículo encontrado: {resultado['codigo']}"
                }
            else:
                return {
                    "status": "error",
                    "message": f"❌ No se encontró ningún artículo con: '{termino_busqueda}'"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error al buscar artículo: {str(e)}"
            }

    def actualizar_articulo(self, articulo_id: int, codigo: str, articulo: str, descripcion: str) -> Dict:
        """Actualiza un artículo existente"""
        try:
            if not articulo_id:
                return {
                    "status": "error",
                    "message": "❌ ID del artículo es obligatorio"
                }
            
            if not codigo or not articulo or not descripcion:
                return {
                    "status": "error",
                    "message": "❌ Código, artículo y descripción son obligatorios"
                }
            
            exito = self.model.modificar_articulo(articulo_id, codigo, articulo, descripcion)
            
            if exito:
                return {
                    "status": "success",
                    "message": f"✅ Artículo '{codigo}' actualizado correctamente"
                }
            else:
                return {
                    "status": "error",
                    "message": f"❌ No se pudo actualizar el artículo. El código '{codigo}' ya existe o el ID no es válido."
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error al actualizar artículo: {str(e)}"
            }

    def eliminar_articulo(self, articulo_id: int) -> Dict:
        """Elimina un artículo de la base de datos"""
        try:
            if not articulo_id:
                return {
                    "status": "error",
                    "message": "❌ ID del artículo es obligatorio"
                }
            
            exito = self.model.eliminar_articulo(articulo_id)
            
            if exito:
                return {
                    "status": "success",
                    "message": f"✅ Artículo ID {articulo_id} eliminado correctamente"
                }
            else:
                return {
                    "status": "error",
                    "message": f"❌ No se pudo eliminar el artículo ID {articulo_id}. Verifique que exista."
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error al eliminar artículo: {str(e)}"
            }

    def obtener_articulo_por_id(self, articulo_id: int) -> Dict:
        """Obtiene un artículo específico por su ID"""
        try:
            # Como el modelo no tiene un método específico por ID, usamos buscar
            # con un término que solo coincida con IDs
            resultado = self.model.buscar_articulo(str(articulo_id))
            
            if resultado and resultado["id"] == articulo_id:
                articulo_data = {
                    "id": resultado["id"],
                    "codigo": resultado["codigo"],
                    "articulo": resultado["articulo"],
                    "descripcion": resultado["descripcion"]
                }
                
                return {
                    "status": "success",
                    "data": articulo_data,
                    "message": f"✅ Artículo encontrado: {resultado['codigo']}"
                }
            else:
                return {
                    "status": "error",
                    "message": f"❌ No se encontró ningún artículo con ID: {articulo_id}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Error al obtener artículo: {str(e)}"
            }