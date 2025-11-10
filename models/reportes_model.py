# En models/reportes_model.py - Actualizar la clase ExportadorService
import sys
import os
import sqlite3
from sqlite3 import Error
from typing import List, Dict, Optional, Any
import pandas as pd
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database_connector import Database
except ImportError:
    from models.database_connector import Database

class ReportesModel:
    """
    Modelo para manejar las operaciones de base de datos para reportes
    """
    
    def __init__(self):
        """Inicializa el modelo con la conexión a la base de datos"""
        try:
            self.db = Database()
            print("[OK] ReportesModel inicializado correctamente")
        except Exception as e:
            print(f"[ERROR] Error al inicializar ReportesModel: {e}")
            self.db = None
    
    def obtener_todos_los_datos(self, tabla: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los datos de una tabla específica
        
        Args:
            tabla (str): Nombre de la tabla
            
        Returns:
            List[Dict]: Lista de diccionarios con los datos
        """
        try:
            if not self.db:
                print("[ERROR] No hay conexión a la base de datos")
                return []
                
            query = f"SELECT * FROM {tabla}"
            resultados = self.db.fetch_all(query)
            print(f"[OK] Obtenidos {len(resultados)} registros de la tabla {tabla}")
            return resultados
            
        except Exception as e:
            print(f"[ERROR] Error al obtener datos de {tabla}: {e}")
            return []
    
    def obtener_datos_con_filtros(self, tabla: str, filtros: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Obtiene datos de una tabla con filtros opcionales
        
        Args:
            tabla (str): Nombre de la tabla
            filtros (Dict): Diccionario con los filtros a aplicar
            
        Returns:
            List[Dict]: Lista de diccionarios con los datos filtrados
        """
        try:
            if not self.db:
                print("[ERROR] No hay conexión a la base de datos")
                return []
                
            if not filtros:
                return self.obtener_todos_los_datos(tabla)
            
            # Construir la consulta con filtros
            condiciones = []
            parametros = []
            
            for campo, valor in filtros.items():
                condiciones.append(f"{campo} = ?")
                parametros.append(valor)
            
            where_clause = " AND ".join(condiciones)
            query = f"SELECT * FROM {tabla} WHERE {where_clause}"
            
            resultados = self.db.fetch_all(query, parametros)
            print(f"[OK] Obtenidos {len(resultados)} registros filtrados de {tabla}")
            return resultados
            
        except Exception as e:
            print(f"[ERROR] Error al obtener datos filtrados de {tabla}: {e}")
            return []
    
    def obtener_estadisticas_basicas(self, tabla: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas básicas de una tabla
        
        Args:
            tabla (str): Nombre de la tabla
            
        Returns:
            Dict: Diccionario con estadísticas
        """
        try:
            if not self.db:
                return {"error": "No hay conexión a la base de datos"}
                
            # Contar total de registros
            query_count = f"SELECT COUNT(*) as total FROM {tabla}"
            resultado_count = self.db.fetch_one(query_count)
            total_registros = resultado_count['total'] if resultado_count else 0
            
            # Obtener estructura de la tabla
            query_estructura = f"PRAGMA table_info({tabla})"
            estructura = self.db.fetch_all(query_estructura)
            columnas = [col['name'] for col in estructura] if estructura else []
            
            return {
                "total_registros": total_registros,
                "columnas": columnas,
                "tabla": tabla,
                "fecha_consulta": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"[ERROR] Error al obtener estadísticas de {tabla}: {e}")
            return {"error": str(e)}
    
    def obtener_tablas_disponibles(self) -> List[str]:
        """
        Obtiene la lista de tablas disponibles en la base de datos
        
        Returns:
            List[str]: Lista de nombres de tablas
        """
        try:
            if not self.db:
                return []
                
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            resultados = self.db.fetch_all(query)
            tablas = [tabla['name'] for tabla in resultados]
            print(f"[OK] Tablas disponibles: {tablas}")
            return tablas
            
        except Exception as e:
            print(f"[ERROR] Error al obtener tablas disponibles: {e}")
            return []

class ExportadorService:
    """
    Servicio para exportar datos a diferentes formatos
    """
    
    @staticmethod
    def exportar_a_dataframe(datos: List[Dict]) -> pd.DataFrame:
        """Convierte datos a DataFrame de pandas"""
        if not datos:
            print("[ADVERTENCIA] No hay datos para exportar")
            return pd.DataFrame()
        
        try:
            df = pd.DataFrame(datos)
            print(f"[OK] DataFrame creado con {len(df)} filas y {len(df.columns)} columnas")
            print(f"[INFO] Columnas: {list(df.columns)}")
            return df
        except Exception as e:
            print(f"[ERROR] Error al crear DataFrame: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def exportar_a_excel(datos: List[Dict], nombre_archivo: str) -> bool:
        """Exporta datos a archivo Excel"""
        try:
            print(f"[PROCESANDO] Intentando exportar a Excel: {nombre_archivo}")
            df = ExportadorService.exportar_a_dataframe(datos)
            
            if df.empty:
                print("[ERROR] DataFrame vacío, no se puede exportar")
                return False
            
            # Verificar que el directorio existe
            directorio = os.path.dirname(nombre_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            
            # Intentar con diferentes motores
            try:
                df.to_excel(nombre_archivo, index=False, engine='openpyxl')
                print(f"[OK] Excel exportado exitosamente con openpyxl: {nombre_archivo}")
                return True
            except Exception as e1:
                print(f"[ADVERTENCIA] Error con openpyxl: {e1}. Intentando con xlsxwriter...")
                try:
                    df.to_excel(nombre_archivo, index=False, engine='xlsxwriter')
                    print(f"[OK] Excel exportado exitosamente con xlsxwriter: {nombre_archivo}")
                    return True
                except Exception as e2:
                    print(f"[ERROR] Error con xlsxwriter: {e2}")
                    return False
                    
        except Exception as e:
            print(f"[ERROR] Error general al exportar a Excel: {e}")
            return False
    
    @staticmethod
    def exportar_a_csv(datos: List[Dict], nombre_archivo: str) -> bool:
        """Exporta datos a archivo CSV"""
        try:
            print(f"[PROCESANDO] Intentando exportar a CSV: {nombre_archivo}")
            df = ExportadorService.exportar_a_dataframe(datos)
            
            if df.empty:
                return False
            
            # Verificar que el directorio existe
            directorio = os.path.dirname(nombre_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
                
            df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
            print(f"[OK] CSV exportado exitosamente: {nombre_archivo}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error al exportar a CSV: {e}")
            return False
    
    @staticmethod
    def exportar_a_pdf(datos: List[Dict], nombre_archivo: str, titulo: str = "Reporte") -> bool:
        """Exporta datos a archivo PDF"""
        try:
            print(f"[PROCESANDO] Intentando exportar a PDF: {nombre_archivo}")
            
            # Verificar si reportlab está instalado
            try:
                from reportlab.lib.pagesizes import letter, A4
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.lib import colors
                from reportlab.pdfbase import pdfmetrics
                from reportlab.pdfbase.ttfonts import TTFont
            except ImportError as e:
                print(f"[ERROR] ReportLab no está instalado: {e}")
                print("[INFO] Instálelo con: pip install reportlab")
                return False
            
            df = ExportadorService.exportar_a_dataframe(datos)
            if df.empty:
                print("[ERROR] No hay datos para exportar a PDF")
                return False
            
            # Verificar que el directorio existe
            directorio = os.path.dirname(nombre_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            
            # Crear documento PDF
            doc = SimpleDocTemplate(
                nombre_archivo,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=40
            )
            
            story = []
            styles = getSampleStyleSheet()
            
            # Título
            titulo_style = styles["Heading1"]
            titulo_style.alignment = 1  # Centrado
            story.append(Paragraph(titulo, titulo_style))
            story.append(Spacer(1, 20))
            
            # Fecha de generación
            fecha_style = styles["Normal"]
            fecha_style.alignment = 1
            fecha_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            story.append(Paragraph(f"<b>Generado el:</b> {fecha_str}", fecha_style))
            story.append(Spacer(1, 30))
            
            # Preparar datos para la tabla
            # Convertir DataFrame a lista de listas
            datos_tabla = [df.columns.tolist()]  # Encabezados
            
            for _, fila in df.iterrows():
                datos_tabla.append([str(valor) for valor in fila.values])
            
            # Crear tabla
            tabla = Table(datos_tabla, repeatRows=1)
            
            # Estilo de la tabla
            estilo_tabla = TableStyle([
                # Encabezados
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Filas de datos
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
            
            # Aplicar estilo alternado a las filas
            for i in range(1, len(datos_tabla)):
                if i % 2 == 0:
                    estilo_tabla.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F9FA'))
            
            tabla.setStyle(estilo_tabla)
            story.append(tabla)
            story.append(Spacer(1, 20))
            
            # Resumen
            total_registros = len(df)
            resumen_style = styles["Normal"]
            resumen_style.alignment = 1
            story.append(Paragraph(f"<b>Total de registros:</b> {total_registros}", resumen_style))
            
            # Generar PDF
            doc.build(story)
            print(f"[OK] PDF exportado exitosamente: {nombre_archivo}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error al exportar a PDF: {e}")
            import traceback
            traceback.print_exc()
            return False