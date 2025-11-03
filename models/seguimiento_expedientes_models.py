import os
from datetime import datetime, date
from typing import List, Optional, Dict
import psycopg2
import psycopg2.extras

class SeguimientoModel:
    def __init__(self, dsn: Optional[str] = None):
        self.dsn = dsn or os.getenv("DATABASE_URL")
        if not self.dsn:
            raise RuntimeError("DATABASE_URL no definido. Define la variable de entorno con la cadena de conexión a PostgreSQL.")
        self._ensure_table()

    def _get_conn(self):
        conn = psycopg2.connect(self.dsn)
        return conn

    def _ensure_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS seguimiento (
            id SERIAL PRIMARY KEY,
            expediente_id INTEGER NOT NULL,
            fecha DATE NOT NULL,
            comentario TEXT,
            creado_en TIMESTAMPTZ DEFAULT now()
        );
        """
        conn = self._get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
        finally:
            conn.close()

    def registrar_seguimiento(self, expediente_id: int, comentario: str, fecha: Optional[str] = None) -> int:
        if fecha and fecha.strip():
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            except Exception as e:
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD.") from e
        else:
            fecha_obj = date.today()

        insert_sql = "INSERT INTO seguimiento (expediente_id, fecha, comentario) VALUES (%s, %s, %s) RETURNING id;"
        conn = self._get_conn()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(insert_sql, (expediente_id, fecha_obj, comentario))
                    new_id = cur.fetchone()[0]
            return new_id
        finally:
            conn.close()

    def obtener_seguimientos(self, expediente_id: Optional[int] = None, desde: Optional[str] = None, hasta: Optional[str] = None) -> List[Dict]:
        query = "SELECT id, expediente_id, to_char(fecha, 'YYYY-MM-DD') AS fecha, comentario, creado_en AT TIME ZONE 'UTC' AS creado_en FROM seguimiento WHERE 1=1"
        params = []
        if expediente_id is not None:
            query += " AND expediente_id = %s"
            params.append(expediente_id)
        if desde:
            try:
                datetime.strptime(desde, "%Y-%m-%d")
            except Exception:
                raise ValueError("Parámetro 'desde' con formato inválido. Use YYYY-MM-DD.")
            query += " AND fecha >= %s"
            params.append(desde)
        if hasta:
            try:
                datetime.strptime(hasta, "%Y-%m-%d")
            except Exception:
                raise ValueError("Parámetro 'hasta' con formato inválido. Use YYYY-MM-DD.")
            query += " AND fecha <= %s"
            params.append(hasta)
        query += " ORDER BY fecha DESC, creado_en DESC"
        conn = self._get_conn()
        try:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(query, tuple(params))
                    rows = cur.fetchall()
                    return [dict(r) for r in rows]
        finally:
            conn.close()

    def obtener_historial_por_expediente(self, expediente_id: int) -> List[Dict]:
        return self.obtener_seguimientos(expediente_id=expediente_id)