# relacion_model.py

from database_connector import database
from sqlite3 import Error

class RelacionNNAFamiliarModel:
    """
    Modelo para gestionar las relaciones (vínculos) entre NNA y Familiares.
    Utiliza la tabla relacion_nna, nna, familiar y parentesco.
    """

    def __init__(self):
        self.db = database

    def obtener_relaciones_por_nna(self, nna_id):
        """
        Recupera todas las relaciones de parentesco para un NNA específico.
        Retorna una lista de diccionarios o una lista vacía.
        """
        sql = """
            SELECT 
                r.nna_id, 
                r.familiar_id, 
                p_fam.primer_nombre || ' ' || p_fam.primer_apellido AS nombre_familiar,
                t.nombre AS parentesco,
                r.convive,
                p_nna.documento_identidad AS doc_nna,
                p_fam.documento_identidad AS doc_familiar
            FROM relacion_nna r
            JOIN parentesco t ON r.parentesco = t.id
            JOIN nna n ON r.nna_id = n.persona_id
            JOIN familiar f ON r.familiar_id = f.persona_id
            JOIN persona p_nna ON n.persona_id = p_nna.id
            JOIN persona p_fam ON f.persona_id = p_fam.id
            WHERE r.nna_id = ?;
        """
        conn = self.db.crearConexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (nna_id,))
            
            # Obtener nombres de columnas
            columnas = [desc[0] for desc in cursor.description]
            
            # Mapear resultados a lista de diccionarios
            relaciones = [dict(zip(columnas, row)) for row in cursor.fetchall()]
            return relaciones
        except Error as e:
            print(f"[ERROR_RELACION] Error al obtener relaciones: {e}")
            return []
        finally:
            self.db.cerrarConexion()


    def crear_relacion(self, nna_id, familiar_id, parentesco_id, convive):
        """
        Inserta una nueva relación NNA/Familiar.
        """
        sql = """
            INSERT INTO relacion_nna (nna_id, familiar_id, parentesco, convive)
            VALUES (?, ?, ?, ?);
        """
        conn = self.db.crearConexion()
        if conn is None:
            return False, "Error de conexión a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (nna_id, familiar_id, parentesco_id, convive))
            conn.commit()
            return True, "Relación creada exitosamente."
        except Error as e:
            # Una restricción PRIMARY KEY o FOREIGN KEY falló
            return False, f"Error al crear la relación: {e}"
        finally:
            self.db.cerrarConexion()


    # Métodos de utilidad
    def obtener_parentescos(self):
        """
        Recupera todos los tipos de parentesco (Catálogo).
        """
        sql = "SELECT id, nombre FROM parentesco;"
        conn = self.db.crearConexion()
        if conn is None:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()  # Retorna lista de tuplas (id, nombre)
        except Error as e:
            print(f"[ERROR_RELACION] Error al obtener parentescos: {e}")
            return []
        finally:
            self.db.cerrarConexion()