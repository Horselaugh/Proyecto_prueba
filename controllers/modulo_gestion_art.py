import sqlite3
from sqlite3 import Row
from typing import List, Optional
from models.database import Database

class ArticuloModelo:
    """
    Modelos que manaja la estructura jerárquica de la LOPNNA (Título, Capítulo, Artículo, Literal)
    """
    def __init__(self):
        self.db = Database()
    
    def insertar_titulo(self, nombre: str) -> Optional[int]:
        """Inserta un título y retorna su ID (o el existente si ya existe)"""
        query_insert = "INSERT INTO titulo (nombre) VALUES(?)"
        query_select = "SELECT id FROM titulo WHERE nombre = ?"
        try:
            with self.db.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                
                # Intenta insertar
                try:
                    cursor.execute(query_insert, (nombre,))
                    conexion.commit()
                    return cursor.lastrowid
                
                except sqlite3.IntegrityError:
                    # Si falla por existir (UNIQUE), busca el ID existente
                    cursor.execute(query_select, (nombre,))
                    resultado = cursor.fetchone()
                    if resultado:
                        # print(f"Título '{nombre}' ya existe. Retornando ID: {resultado[0]}") # Debug
                        return resultado[0]
                    print(f"ERROR LÓGICO: IntegrityError para Título '{nombre}' pero SELECT falló.") 
                    return None
                        
        except sqlite3.Error as e:
            print(f"Error al insertar Título: {str(e)}")
            return None
# Fin de insertar_titulo
        
    def insertar_capitulo(self, titulo_id: int, nombre: str) -> Optional[int]:
        """
        Inserta un capítulo y retorna su ID (o el existente si ya existe).
        Args: 
            titulo_id: ID del título al que pertenece.
            nombre: Nombre del capítulo.
        """
        
        query_insert = "INSERT INTO capitulo (titulo_id, nombre) VALUES (?, ?)"
        query_select = "SELECT id FROM capitulo WHERE titulo_id = ? AND nombre = ?"
        try:
            with self.db.obtener_conexion() as conexion:
                cursor = conexion.cursor()                
                # Intenta insertar
                try:
                    cursor.execute(query_insert, (titulo_id, nombre,))
                    conexion.commit()
                    return cursor.lastrowid
                except sqlite3.IntegrityError:
                    # Si falla por existir (UNIQUE), busca el ID existente
                    cursor.execute(query_select, (titulo_id, nombre,))
                    resultado = cursor.fetchone()
                    if resultado:
                        return resultado[0] # Retorna el ID
                    else:
                        print(f"ERROR LÓGICO: IntegrityError para Capítulo '{nombre}' pero SELECT falló.")
                        return None
        except sqlite3.Error as e:
            print(f"Error al insertar Capítulo: {str(e)}")
            return None
# Fin de insertar_capitulo
    
    def insertar_articulo(self, capitulo_id: int, numero_articulo: str, descripcion: str, texto: str) -> Optional[int]:
        """Inserta un artículo y retorna un ID, requiere el capitulo_id"""
        query = "INSERT INTO articulo (capitulo_id, numero_articulo, descripcion, texto) VALUES (?, ?, ?, ?)"
        try:
            with self.db.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(query, (capitulo_id, numero_articulo, descripcion, texto))
                conexion.commit()
                return cursor.lastrowid                
        except sqlite3.IntegrityError as e:
             # Si ya existe, no se hace nada o se podría buscar y retornar su ID,
            print(f"Advertencia: Artículo {numero_articulo} ya existe en ese capítulo. {str(e)}")
            return None
        except sqlite3.Error as e:
            print(f"Error al insertar artículo {numero_articulo}: {str(e)}")
            return None
# Fin de insertar_articulo
            
    def insertar_literal(self, articulo_id: int, literal_codigo: str, texto: str) -> bool:
        """Inserta un literal para un artículo"""
        query = "INSERT INTO literal (articulo_id, literal_codigo, texto) VALUES (?, ?, ?)"
        try:
            with self.db.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(query, (articulo_id, literal_codigo, texto))
                conexion.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Advertencia: Literal {literal_codigo} del Art. {articulo_id} ya existe. {str(e)}")
            return False
        except sqlite3.Error as e:
            print(f"Error al insertar literal {literal_codigo} del Art. {articulo_id}: {str(e)}")
            return False
# Fin de insertar_literal

    # --- Métodos de Lectura (Se mantienen) ---

    def obtener_todos_los_articulos(self) -> List[Row]:
        """
        Retorna todos los artículos para llenar la lista en la vista
        """
        query = """
            SELECT 
                t.nombre AS titulo_nombre, 
                c.nombre AS capitulo_nombre, 
                a.numero_articulo, 
                a.descripcion
            FROM titulo t
            INNER JOIN capitulo c ON t.id = c.titulo_id
            INNER JOIN articulo a ON c.id = a.capitulo_id
            ORDER BY t.nombre, c.nombre, a.numero_articulo
        """
        try:
            with self.db.obtener_conexion() as conexion:
                conexion.row_factory = sqlite3.Row
                cursor = conexion.cursor()
                cursor.execute(query)
                return cursor.fetchall()
                
        except sqlite3.Error as e:
            print(f"Ha ocurrido un error mientras se trataba de obtener todos los artículos: {str(e)}")
            return []
    # Fin de obtener_todos_los_articulos
    
    def buscar_articulo(self, termino_busqueda: str) -> sqlite3.Row | None:
        """Busca y retorna un Artículo por su descripción o por su nombre de artículo"""
        query = """
            SELECT 
                t.nombre AS titulo_nombre, 
                c.nombre AS capitulo_nombre,
                a.numero_articulo,
                a.descripcion,
                a.texto
            FROM articulo a
            INNER JOIN capitulo c ON c.id = a.capitulo_id
            INNER JOIN titulo t ON t.id = c.titulo_id 
            WHERE a.descripcion LIKE ? OR a.numero_articulo LIKE ?
            ORDER BY c.nombre, a.numero_articulo, a.descripcion, a.texto
            LIMIT 1
        """
        
        termino_like = f"%{termino_busqueda}%" 
        parametros = (termino_like, termino_busqueda.strip())
        
        try:
            with self.db.obtener_conexion() as conexion:
                conexion.row_factory = sqlite3.Row
                cursor = conexion.cursor()
                cursor.execute(query, parametros)
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Ha ocurrido un error mientras se trataba de obtener el articulo con el término {termino_busqueda}: {str(e)}")
            return None
    # Fin de buscar_articulo
    
    def obtener_literales_por_articulo(self, numero_articulo: str) -> List[Row]:
        """
        Busca y retorna todos los literales de un artículo dado su número.
        """
        query = """
            SELECT
                l.literal_codigo,
                l.texto
            FROM literal l
            INNER JOIN articulo a ON a.id = l.articulo_id
            WHERE a.numero_articulo = ?
            ORDER BY l.literal_codigo
        """
        
        try:
            with self.db.obtener_conexion() as conexion:
                conexion.row_factory = sqlite3.Row
                cursor = conexion.cursor()
                cursor.execute(query, (numero_articulo,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener literales para el artículo {numero_articulo}: {str(e)}")
            return []
# Fin de obtener_literales_por_articulo
    
    def modificar_articulo(self, articulo_original: str, capitulo_id: int, nuevo_numero: str, nueva_descripcion: str, nuevo_texto: str) -> bool:
        """
        Busca a un artículo por su numero_articulo original y modifica los datos.
        """
        query = """
            UPDATE articulo
            SET 
                capitulo_id = ?,
                numero_articulo = ?,
                descripcion = ?,
                texto = ?
            WHERE numero_articulo = ?
        """
        
        try:
            with self.db.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                parametros = (capitulo_id, nuevo_numero, nueva_descripcion, nuevo_texto, articulo_original)
                cursor.execute(query, parametros)
                conexion.commit()
                return cursor.rowcount > 0 
        except sqlite3.IntegrityError as e:
            # Si el nuevo_numero ya existe en el capitulo_id, lanzará este error
            print(f"Error de integridad: El artículo {nuevo_numero} ya existe en ese capítulo. {str(e)}")
            return False
        except sqlite3.Error as e:
            print(f"Ha ocurrido un error mientras se trataba actualizar el artículo {articulo_original}: {str(e)}")
            return False
# Fin de modificar_artículo

    def eliminar_articulo(self, numero_articulo: str) -> bool:
        """
        Elimina un artículo de la base de datos dado su número de artículo.
        
        NOTA: Debido a 'ON DELETE CASCADE' en la tabla 'literal',
              todos los literales asociados a este artículo serán eliminados automáticamente.
        """
        query = "DELETE FROM articulo WHERE numero_articulo = ?"
        
        try:
            with self.db.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(query, (numero_articulo,))
                conexion.commit()
                # Retorna True si se eliminó al menos una fila
                if cursor.rowcount > 0:
                    print(f"Artículo {numero_articulo} eliminado con éxito.")
                    return True
                else:
                    print(f"Advertencia: No se encontró el artículo {numero_articulo} para eliminar.")
                    return False
        except sqlite3.Error as e:
            print(f"Error al intentar eliminar el artículo {numero_articulo}: {str(e)}")
            return False
    # Fin de eliminar_articulo