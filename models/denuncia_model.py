import sys
import os
from database_connector import Database # Importar la clase Database del Singleton
from sqlite3 import Error, IntegrityError
from typing import Dict, List, Optional

# Añadir el path para que las importaciones relativas funcionen
sys.path.append(os.path.join(os.path.dirname(__file__)))

# 🚨 CAMBIO CLAVE: Importar directamente la clase Database desde database_connector
# Se asume que database_connector.py está en la misma carpeta o accesible por path.
try:
    from database_connector import Database  # Usamos la clase Database (Singleton)
except ImportError:
    # Esto manejaría el caso si la estructura de carpetas es diferente (models/database_connector)
    # y la importación del nivel superior falla.
    print("Advertencia: No se pudo importar Database directamente. Intentando models.database_connector...")
    from models.database_connector import Database

class DenunciaModel:

    def __init__(self):
        # Se obtiene la única instancia del Singleton Database
        self.db = Database()

    def crear_denuncia_completa(self, datos_denuncia: Dict, nna_involucrados: List[Dict], denunciantes: List[Dict], denunciados: List[int]) -> tuple[Optional[int], str]:
        """
        Crea la denuncia principal y todos sus registros asociados en una sola transacción.

        :param datos_denuncia: Diccionario con campos de la tabla 'denuncia'.
        :param nna_involucrados: Lista de diccionarios [{'nna_id', 'rol', 'detalle_participacion'}]
        :param denunciantes: Lista de diccionarios [{'persona_id', 'declaracion', 'lesiones'}]
        :param denunciados: Lista de IDs de persona de los denunciados.
        :return: Tupla (denuncia_id o None, mensaje de estado)
        """
        conn = self.db.crearConexion()
        if conn is None:
            return None, "Error de conexión a la base de datos."
        
        try:
            cursor = conn.cursor()
            
            # --- 1. Insertar Denuncia Principal ---
            sql_denuncia = """
                INSERT INTO denuncia (consejero_id, fecha_hechos, descripcion, estado)
                VALUES (?, ?, ?, ?);
            """
            consejero_id = datos_denuncia.get('consejero_id')
            fecha_hechos = datos_denuncia.get('fecha_hechos')
            descripcion = datos_denuncia.get('descripcion')
            estado = datos_denuncia.get('estado', True) # Por defecto, activa (True)
            
            cursor.execute(sql_denuncia, (consejero_id, fecha_hechos, descripcion, estado))
            denuncia_id = cursor.lastrowid
            
            # --- 2. Insertar NNA Involucrados ---
            sql_nna = "INSERT INTO nna_involucrado (denuncia_id, nna_id, rol, detalle_participacion) VALUES (?, ?, ?, ?);"
            nna_data = [(denuncia_id, nna['nna_id'], nna['rol'], nna['detalle_participacion']) for nna in nna_involucrados]
            cursor.executemany(sql_nna, nna_data)

            # --- 3. Insertar Denunciantes ---
            sql_denunciante = "INSERT INTO denunciante (denuncia_id, persona_id, declaracion, lesiones) VALUES (?, ?, ?, ?);"
            denunciante_data = [(denuncia_id, d.get('persona_id'), d['declaracion'], d.get('lesiones')) for d in denunciantes]
            cursor.executemany(sql_denunciante, denunciante_data)

            # --- 4. Insertar Denunciados ---
            sql_denunciado = "INSERT INTO denunciado (denuncia_id, persona_id) VALUES (?, ?);"
            denunciado_data = [(denuncia_id, p_id) for p_id in denunciados]
            cursor.executemany(sql_denunciado, denunciado_data)
            
            conn.commit()
            return denuncia_id, "Denuncia y registros asociados creados exitosamente."
            
        except IntegrityError as e:
            conn.rollback()
            return None, f"Error de integridad (FK/Unique Constraint) al registrar la denuncia: {e}"
        except Error as e:
            conn.rollback()
            print(f"[ERROR_DENUNCIA] Error al crear denuncia: {e}")
            return None, f"Error interno al crear denuncia: {e}"
        finally:
            self.db.cerrarConexion()

    # ----------------------------------------------------------------------
    # Métodos de Seguimiento y Cierre
    # ----------------------------------------------------------------------

    def agregar_seguimiento(self, denuncia_id: int, consejero_id: int, observaciones: str) -> tuple[bool, str]:
        """
        Agrega un registro de seguimiento a una denuncia existente.
        """
        sql = "INSERT INTO seguimiento (denuncia_id, consejero_id, observaciones) VALUES (?, ?, ?);"
        conn = self.db.crearConexion()
        if conn is None:
            return False, "Error de conexión."
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (denuncia_id, consejero_id, observaciones))
            conn.commit()
            return True, "Seguimiento agregado exitosamente."
        except Error as e:
            print(f"[ERROR_SEGUIMIENTO] Error al agregar seguimiento: {e}")
            return False, f"Error al agregar seguimiento: {e}"
        finally:
            self.db.cerrarConexion()
            
    def cerrar_denuncia(self, denuncia_id: int, consejero_id: int, acta_cierre: str) -> tuple[bool, str]:
        """
        Registra el cierre de la denuncia y actualiza su estado.
        """
        conn = self.db.crearConexion()
        if conn is None:
            return False, "Error de conexión."
        try:
            cursor = conn.cursor()
            
            # 1. Insertar registro de cierre
            sql_cierre = "INSERT INTO cierre (denuncia_id, consejero_id, acta_cierre) VALUES (?, ?, ?);"
            cursor.execute(sql_cierre, (denuncia_id, consejero_id, acta_cierre))
            
            # 2. Actualizar estado de la denuncia principal a False (inactiva)
            sql_update = "UPDATE denuncia SET estado = FALSE WHERE id = ?;"
            cursor.execute(sql_update, (denuncia_id,))
            
            conn.commit()
            return True, "Denuncia cerrada exitosamente."
        except IntegrityError:
            conn.rollback()
            return False, "Error: Esta denuncia ya tiene un registro de cierre."
        except Error as e:
            conn.rollback()
            print(f"[ERROR_CIERRE] Error al cerrar denuncia: {e}")
            return False, f"Error al cerrar denuncia: {e}"
        finally:
            self.db.cerrarConexion()

    # ----------------------------------------------------------------------
    # Métodos de Consulta
    # ----------------------------------------------------------------------

    def _ejecutar_consulta(self, sql: str, params: tuple) -> Optional[List[Dict]]:
        """Método auxiliar para ejecutar consultas SELECT y mapear a lista de diccionarios."""
        conn = self.db.crearConexion()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            if rows:
                columnas = [desc[0] for desc in cursor.description]
                return [dict(zip(columnas, row)) for row in rows]
            return []
        except Error as e:
            print(f"[ERROR_CONSULTA] Error al ejecutar consulta: {e}")
            return None
        finally:
            self.db.cerrarConexion()

    def obtener_denuncia_por_id(self, denuncia_id: int) -> Optional[Dict]:
        """
        Obtiene los datos básicos de una denuncia y si está abierta o cerrada.
        """
        sql = """
            SELECT 
                d.id, d.consejero_id, d.fecha_denuncia, d.fecha_hechos, 
                d.descripcion, d.estado,
                p_con.primer_nombre || ' ' || p_con.primer_apellido AS nombre_consejero
            FROM denuncia d
            JOIN personal per ON d.consejero_id = per.persona_id
            JOIN persona p_con ON per.persona_id = p_con.id
            WHERE d.id = ?;
        """
        # Se reutiliza la lógica existente, pero adaptando para obtener un solo resultado
        resultados = self._ejecutar_consulta(sql, (denuncia_id,))
        return resultados[0] if resultados and resultados is not None else None

    def obtener_nna_involucrados(self, denuncia_id: int) -> Optional[List[Dict]]:
        """
        Obtiene la lista de NNA involucrados en una denuncia, incluyendo sus datos personales.
        """
        sql = """
            SELECT 
                ni.nna_id, ni.rol, ni.detalle_participacion, 
                p.documento_identidad, p.primer_nombre, p.primer_apellido, 
                n.fecha_nacimiento
            FROM nna_involucrado ni
            JOIN persona p ON ni.nna_id = p.id
            JOIN nna n ON ni.nna_id = n.persona_id
            WHERE ni.denuncia_id = ?;
        """
        return self._ejecutar_consulta(sql, (denuncia_id,))

    def obtener_denunciantes(self, denuncia_id: int) -> Optional[List[Dict]]:
        """
        Obtiene la lista de denunciantes de una denuncia.
        Si persona_id es NULL, el denunciante es anónimo.
        """
        sql = """
            SELECT 
                d.persona_id, d.declaracion, d.lesiones, 
                CASE 
                    WHEN p.id IS NOT NULL THEN p.primer_nombre || ' ' || p.primer_apellido
                    ELSE 'Anónimo' 
                END AS nombre_completo,
                p.documento_identidad
            FROM denunciante d
            LEFT JOIN persona p ON d.persona_id = p.id
            WHERE d.denuncia_id = ?;
        """
        return self._ejecutar_consulta(sql, (denuncia_id,))

    def obtener_denunciados(self, denuncia_id: int) -> Optional[List[Dict]]:
        """
        Obtiene la lista de denunciados de una denuncia, incluyendo sus datos personales y medidas.
        """
        sql = """
            SELECT 
                d.persona_id, d.medidas, 
                p.documento_identidad, p.primer_nombre, p.primer_apellido
            FROM denunciado d
            JOIN persona p ON d.persona_id = p.id
            WHERE d.denuncia_id = ?;
        """
        return self._ejecutar_consulta(sql, (denuncia_id,))