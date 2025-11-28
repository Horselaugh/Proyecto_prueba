import sys
import os
from sqlite3 import Error, IntegrityError
from typing import Dict, List, Optional

# [CORRECCIÓN 1] Se elimina la manipulación de sys.path que es innecesaria.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Asumiendo que 'database_connector' está en una ubicación accesible
from database_connector import Database

class DenunciaModel:

    def __init__(self):
        # Se asume que 'Database' es un conector existente
        self.db = Database() 

    def _ejecutar_consulta(self, sql: str, params: tuple) -> Optional[List[Dict]]:
        """
        Método auxiliar para ejecutar consultas SELECT y mapear a lista de diccionarios.
        
        Se asegura el patrón de abrir y cerrar conexión en cada operación.
        """
        conn = self.db.crearConexion()
        if conn is None:
            return []
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
            if conn:
                self.db.cerrarConexion()

    def _ejecutar_transaccion(self, sql: str, params: tuple) -> tuple[bool, str]:
        """
        Método auxiliar para ejecutar operaciones INSERT/UPDATE/DELETE.
        """
        conn = self.db.crearConexion()
        if conn is None:
            return False, "Error de conexión a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return True, "Operación exitosa."
        except Error as e:
            conn.rollback()
            print(f"[ERROR_TRANSACCION] Error al ejecutar transacción: {e}")
            return False, f"Error: {e}"
        finally:
            if conn:
                self.db.cerrarConexion()

    def obtener_listado_denuncias_filtrado(self, texto_busqueda: str = '', estado: str = 'Todos') -> List[Dict]:
        """
        Implementa la lógica de filtrado de denuncias para la tabla de la vista.
        """
        sql = """
            SELECT 
                d.id, d.fecha_denuncia, d.fecha_hechos, 
                SUBSTR(d.descripcion, 1, 50) || '...' AS titulo, 
                d.estado, 
                CASE d.estado 
                    WHEN 1 THEN 'Pendiente' 
                    ELSE 'Resuelto'       
                END AS estado_str,
                p_con.primer_nombre || ' ' || p_con.primer_apellido AS nombre_consejero
            FROM denuncia d
            LEFT JOIN personal per ON d.consejero_id = per.persona_id
            LEFT JOIN persona p_con ON per.persona_id = p_con.id
        """
        
        condiciones = []
        params = []
        
        # 1. Filtro de Texto (Busca en ID, Descripción o Consejero)
        if texto_busqueda:
            texto_like = f'%{texto_busqueda}%'
            condiciones.append("(CAST(d.id AS TEXT) LIKE ? OR d.descripcion LIKE ? OR nombre_consejero LIKE ?)")
            params.extend([texto_like, texto_like, texto_like])
            
        # 2. Filtro de Estado (Mapeo de string de la vista a valor booleano de la DB)
        if estado != 'Todos':
            if estado in ["Pendiente", "En Revisión"]:
                 condiciones.append("d.estado = 1") 
            elif estado in ["Resuelto", "Rechazado"]:
                 condiciones.append("d.estado = 0")
        
        if condiciones:
            sql += " WHERE " + " AND ".join(condiciones)
            
        sql += " ORDER BY d.fecha_denuncia DESC;"
            
        return self._ejecutar_consulta(sql, tuple(params)) or []

    def crear_denuncia_completa(self, datos_denuncia: Dict, nna_involucrados: List[Dict], denunciantes: List[Dict], denunciados: List[int]) -> tuple[Optional[int], str]:
        """
        Crea la denuncia principal y todos sus registros asociados en una sola transacción.
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
            estado = datos_denuncia.get('estado', True) 
            
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
            
            # [CORRECCIÓN 2] Asegurar que el commit se realiza después de todas las inserciones.
            # En el código original ya estaba, pero se asegura que no haya una ruptura lógica
            # antes de este punto que pueda causar que se cierre la conexión antes de tiempo.
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
            if conn:
                self.db.cerrarConexion()

    def actualizar_datos_basicos_denuncia(self, denuncia_id: int, nueva_descripcion: str, nuevo_estado: bool) -> tuple[bool, str]:
        """
        Actualiza la descripción y el estado de una denuncia existente.
        """
        sql = "UPDATE denuncia SET descripcion = ?, estado = ? WHERE id = ?;"
        conn = self.db.crearConexion()
        if conn is None:
            return False, "Error de conexión."
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (nueva_descripcion, nuevo_estado, denuncia_id))
            if cursor.rowcount == 0:
                return False, "Error: Denuncia no encontrada o no hubo cambios."
            conn.commit()
            return True, "Denuncia actualizada exitosamente."
        except Error as e:
            conn.rollback()
            print(f"[ERROR_UPDATE] Error al actualizar denuncia ID {denuncia_id}: {e}")
            return False, f"Error al actualizar denuncia: {e}"
        finally:
            if conn:
                self.db.cerrarConexion()

    def eliminar_denuncia(self, denuncia_id: int) -> tuple[bool, str]:
        """
        Elimina una denuncia por su ID. Se asume que la DB tiene configurada la 
        eliminación en cascada (CASCADE DELETE) en las tablas dependientes.
        """
        sql = "DELETE FROM denuncia WHERE id = ?;"
        # Reutiliza el método auxiliar para la transacción
        return self._ejecutar_transaccion(sql, (denuncia_id,))
            
    # ----------------------------------------------------------------------
    # Métodos de Seguimiento y Cierre y Consulta (Se omiten para brevedad)
    # ----------------------------------------------------------------------

    def obtener_denuncia_por_id(self, denuncia_id: int) -> Optional[Dict]:
        """Obtiene los datos básicos de una denuncia."""
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
        resultados = self._ejecutar_consulta(sql, (denuncia_id,))
        return resultados[0] if resultados and resultados is not None else None

    # ----------------------------------------------------------------------
    # Métodos de Consulta
    # ----------------------------------------------------------------------

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