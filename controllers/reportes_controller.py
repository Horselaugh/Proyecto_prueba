# controllers/reportes_controller.py
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

try:
    from models.reportes_model import ReportesModel, ExportadorService
except ImportError:
    # Fallback para desarrollo
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models.reportes_model import ReportesModel, ExportadorService

class ReportesController:
    """
    Controlador para manejar la lógica de reportes
    """
    
    def __init__(self, view):
        """
        Inicializa el controlador
        
        Args:
            view: Vista asociada al controlador
        """
        self.view = view
        self.model = ReportesModel()
        self.exportador = ExportadorService()
        
        # Crear tablas si no existen
        self.crear_tablas_si_no_existen()
        
        # Datos en memoria
        self.datos_nna = []
        self.datos_alertas = []
        self.datos_seguimientos = []
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
    
    def crear_tablas_si_no_existen(self):
        """Crea las tablas necesarias si no existen"""
        try:
            if hasattr(self.model, 'db') and self.model.db:
                self.model.db.create_tables()
                print("[OK] Tablas verificadas/creadas")
            else:
                print("[ERROR] No se puede acceder a la base de datos para crear tablas")
        except Exception as e:
            print(f"[ERROR] Error creando tablas: {e}")   
    
    def ejecutar(self):
        """
        Método principal para ejecutar la aplicación
        """
        try:
            print("[OK] Controlador de reportes ejecutándose")
            
            # Crear datos de prueba si no hay datos
            if not self.datos_nna and not self.datos_alertas and not self.datos_seguimientos:
                print("[INFO] No hay datos, generando datos de prueba...")
                self.crear_datos_prueba()
            
            # Actualizar la vista con los datos cargados
            if hasattr(self.view, 'actualizar_vista_datos'):
                self.view.actualizar_vista_datos()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Error ejecutando controlador: {e}")
            return False
    
    def cargar_datos_iniciales(self):
        """Carga los datos iniciales desde la base de datos"""
        try:
            print("[INFO] Cargando datos iniciales...")
            
            # Cargar datos de NNA
            self.datos_nna = self.model.obtener_todos_los_datos("nna")
            print(f"[OK] Cargados {len(self.datos_nna)} registros de NNA")
            
            # Cargar datos de alertas
            self.datos_alertas = self.model.obtener_todos_los_datos("alertas")
            print(f"[OK] Cargados {len(self.datos_alertas)} registros de alertas")
            
            # Cargar datos de seguimientos
            self.datos_seguimientos = self.model.obtener_todos_los_datos("seguimientos")
            print(f"[OK] Cargados {len(self.datos_seguimientos)} registros de seguimientos")
            
        except Exception as e:
            print(f"[ERROR] Error al cargar datos iniciales: {e}")
    
    def crear_datos_prueba(self):
        """
        Crea datos de prueba en la base de datos si no existen
        """
        try:
            # Verificar si ya hay datos
            nna_existentes = self.model.obtener_todos_los_datos("nna")
            if nna_existentes:
                print("[INFO] Ya existen datos en la base de datos")
                return
            
            print("[PROCESANDO] Creando datos de prueba...")
            
            # Asegurarse de que las tablas existen primero
            self.crear_tablas_si_no_existen()
            
            # Datos de prueba para NNA
            datos_nna = [
                {
                    'documento': '1001001001',
                    'nombre': 'Ana',
                    'apellido': 'García',
                    'fecha_nacimiento': '2010-05-15',
                    'genero': 'F',
                    'telefono': '0991234567',
                    'direccion': 'Calle Principal 123'
                },
                {
                    'documento': '1001001002', 
                    'nombre': 'Carlos',
                    'apellido': 'López',
                    'fecha_nacimiento': '2008-08-22',
                    'genero': 'M',
                    'telefono': '0987654321',
                    'direccion': 'Avenida Central 456'
                }
            ]
            
            # Insertar datos de prueba
            for nna in datos_nna:
                success = self.model.db.insert("nna", nna)
                if success == -1:
                    print(f"[ERROR] No se pudo insertar NNA: {nna['nombre']}")
                    print("[OK] Datos de prueba creados correctamente")
                    
                    # Recargar datos después de crear los de prueba
                    self.cargar_datos_iniciales()
                    
        except Exception as e:
            print(f"[ERROR] Error creando datos de prueba: {e}")
    
    def obtener_datos_por_tipo(self, tipo: str) -> List[Dict[str, Any]]:
        """
        Obtiene datos según el tipo especificado
        
        Args:
            tipo (str): Tipo de datos ('nna', 'alertas', 'seguimientos')
            
        Returns:
            List[Dict]: Lista de datos
        """
        if tipo == "nna":
            return self.datos_nna
        elif tipo == "alertas":
            return self.datos_alertas
        elif tipo == "seguimientos":
            return self.datos_seguimientos
        else:
            return []
    
    def cargar_datos_tipo(self, tipo: str):
        """Carga datos de un tipo específico y actualiza la vista
        Args: tipo (str): Tipo de datos a cargar """
        try:
            print(f"[PROCESANDO] Cargando datos de {tipo}")
            datos = self.obtener_datos_por_tipo(tipo)
            if datos:
                success_msg = f"Cargados {len(datos)} registros de {tipo}"
                print(f"[OK] {success_msg}")
                self.view.mostrar_mensaje("Éxito", success_msg)
            
            # Actualizar la vista con los datos
            if hasattr(self.view, 'actualizar_vista_datos'):
                self.view.actualizar_vista_datos()
            else:
                info_msg = f"No hay datos disponibles para {tipo}"
                print(f"[INFO] {info_msg}")
                self.view.mostrar_mensaje("Información", info_msg, "info")
            
        except Exception as e:
            error_msg = f"Error al cargar datos de {tipo}: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.view.mostrar_mensaje("Error", error_msg, "error")
    
    def cargar_nna(self):
        """Carga datos de NNA"""
        self.cargar_datos_tipo("nna")
    
    def cargar_denuncias(self):
        """Carga datos de denuncias"""
        self.cargar_datos_tipo("alertas")
        
    def cargar_expedientes(self):
        """Carga datos de expedientes"""
        self.cargar_datos_tipo("seguimientos")
        
    def mostrar_estadistica_genero(self):
        """Muestra estadística de NNA por género"""
    
        try:
            print("[PROCESANDO] Generando estadística por género")
        
            if not self.datos_nna:
                self.view.mostrar_mensaje("Info", "No hay datos de NNA para mostrar", "info")
                return
            
            # Calcular estadísticas por género
            estadisticas = {}
            for nna in self.datos_nna:
                genero = nna.get('genero', 'No especificado')
                if genero not in estadisticas:
                    estadisticas[genero] = 0
                    estadisticas[genero] += 1
                    
                    # Convertir a formato para la vista
                    datos_grafico = [{'genero': k, 'total': v} for k, v in estadisticas.items()]
                    
                    # Mostrar en la vista
                    if hasattr(self.view, 'mostrar_grafico'):
                        self.view.mostrar_grafico(datos_grafico, "NNA por Género", "pie")
        except Exception as e:
            error_msg = f"Error generando estadística de género: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.view.mostrar_mensaje("Error", error_msg, "error")
            
    def mostrar_estadistica_denuncias(self):
        """Muestra estadística de denuncias por estado"""
        try:
            print("[PROCESANDO] Generando estadística de denuncias")
        
            if not self.datos_alertas:
                self.view.mostrar_mensaje("Info", "No hay datos de alertas para mostrar", "info")
                return
            
            # Calcular estadísticas por estado
            estadisticas = {}
            for alerta in self.datos_alertas:
                estado = alerta.get('estado', 'No especificado')
                if estado not in estadisticas:
                    estadisticas[estado] = 0
                    estadisticas[estado] += 1
                    
            # Convertir a formato para la vista
            datos_grafico = [{'estado': k, 'total': v} for k, v in estadisticas.items()]
        
            # Mostrar en la vista
            if hasattr(self.view, 'mostrar_grafico'):
                self.view.mostrar_grafico(datos_grafico, "Alertas por Estado", "pie")
        
        except Exception as e:
            error_msg = f"Error generando estadística de denuncias: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.view.mostrar_mensaje("Error", error_msg, "error")

    def mostrar_estadistica_edad(self):
        """Muestra estadística de NNA por rango de edad"""
        try:
            print("[PROCESANDO] Generando estadística por edad")
            if not self.datos_nna:
                self.view.mostrar_mensaje("Info", "No hay datos de NNA para mostrar", "info")
                return
            # Calcular rangos de edad
            rangos = {
                '0-5 años': 0,
                '6-12 años': 0,
                '13-17 años': 0,
                '18+ años': 0
                }
            
            for nna in self.datos_nna:
                edad_str = str(nna.get('edad', ''))
                if edad_str.isdigit():
                    edad = int(edad_str)
                    if edad <= 5:
                        rangos['0-5 años'] += 1
                    elif edad <= 12:
                        rangos['6-12 años'] += 1
                    elif edad <= 17:
                        rangos['13-17 años'] += 1
                    else:
                        rangos['18+ años'] += 1
                else:
                    # Si no hay edad, contar en "No especificado"
                    
                    if 'No especificado' not in rangos:
                        rangos['No especificado'] = 0
                        rangos['No especificado'] += 1
                    # Convertir a formato para la vista
                        datos_grafico = [{'rango_edad': k, 'total': v} for k, v in rangos.items() if v > 0]
                        
                    # Mostrar en la vista
                        if hasattr(self.view, 'mostrar_grafico'):
                            self.view.mostrar_grafico(datos_grafico, "NNA por Rango de Edad", "bar")
        
        except Exception as e:
            error_msg = f"Error generando estadística de edad: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.view.mostrar_mensaje("Error", error_msg, "error")
    
    def exportar_datos(self, tipo: str):
        """Exporta datos a Excel o CSV
        Args:tipo (str): Tipo de datos a exportar"""
        try:
            print(f"[EXPORTANDO] Solicitando exportación de {tipo}")
            
            datos = self.obtener_datos_por_tipo(tipo)
            if not datos:
                error_msg = f"No hay datos de {tipo} para exportar"
                print(f"[ERROR] {error_msg}")
                self.view.mostrar_mensaje("Error", error_msg, "error")
                return
            
            # Solicitar archivo al usuario
            archivo = filedialog.asksaveasfilename(
                title=f"Exportar {tipo}",
                defaultextension=".xlsx",
                filetypes=[
                    ("Excel files", "*.xlsx"),
                    ("CSV files", "*.csv"),
                    ("All files", "*.*")
                ]
            )
            
            if not archivo:
                print("[INFO] Exportación cancelada por el usuario")
                return
            
            # Determinar formato y exportar
            if archivo.lower().endswith('.csv'):
                success = self.exportador.exportar_a_csv(datos, archivo)
                formato = "CSV"
            else:
                success = self.exportador.exportar_a_excel(datos, archivo)
                formato = "Excel"
            
            if success:
                success_msg = f"Datos de {tipo} exportados exitosamente a {formato}"
                print(f"[OK] {success_msg}")
                self.view.mostrar_mensaje("Éxito", success_msg)
            else:
                error_msg = f"Error al exportar datos de {tipo} a {formato}"
                print(f"[ERROR] {error_msg}")
                self.view.mostrar_mensaje("Error", error_msg, "error")
                
        except Exception as e:
            error_msg = f"Error al exportar {tipo}: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.view.mostrar_mensaje("Error", error_msg, "error")
    
    def exportar_pdf(self, tipo: str):
        """
        Exporta datos a PDF
        
        Args:
            tipo (str): Tipo de datos a exportar
        """
        try:
            print(f"[EXPORTANDO] Solicitando exportación PDF de {tipo}")
            
            datos = self.obtener_datos_por_tipo(tipo)
            if not datos:
                error_msg = f"No hay datos de {tipo} para exportar"
                print(f"[ERROR] {error_msg}")
                self.view.mostrar_mensaje("Error", error_msg, "error")
                return
            
            # Solicitar archivo al usuario
            archivo = filedialog.asksaveasfilename(
                title=f"Exportar {tipo} a PDF",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not archivo:
                print("[INFO] Exportación PDF cancelada por el usuario")
                return
            
            # Generar título del reporte
            titulos = {
                "nna": "Reporte de Niños, Niñas y Adolescentes",
                "alertas": "Reporte de Alertas",
                "seguimientos": "Reporte de Seguimientos"
            }
            titulo = titulos.get(tipo, f"Reporte de {tipo}")
            
            success = self.exportador.exportar_a_pdf(datos, archivo, titulo)
            
            if success:
                success_msg = f"Reporte PDF de {tipo} generado exitosamente"
                print(f"[OK] {success_msg}")
                self.view.mostrar_mensaje("Éxito", success_msg)
            else:
                error_msg = f"Error al generar PDF de {tipo}"
                print(f"[ERROR] {error_msg}")
                self.view.mostrar_mensaje("Error", error_msg, "error")
                
        except Exception as e:
            error_msg = f"Error al exportar PDF de {tipo}: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.view.mostrar_mensaje("Error", error_msg, "error")
    
    def agregar_nna(self, datos_nna: Dict[str, Any]):
        """
        Agrega un nuevo NNA al sistema
        """
        
        try:
            print(f"[PROCESANDO] Agregando nuevo NNA: {datos_nna.get('nombre', '')}")
            
            # Validar datos requeridos
            if not datos_nna.get('nombre') or not datos_nna.get('apellido'):
                error_msg = "Nombre y apellido son requeridos"
                print(f"[ERROR] {error_msg}")
                self.view.mostrar_mensaje("Error", error_msg, "error")
                return False
            
            datos_nna['id'] = len(self.datos_nna) + 1
            datos_nna['fecha_creacion'] = datetime.now().isoformat()
            
            self.datos_nna.append(datos_nna)
            success_msg = f"NNA '{datos_nna['nombre']} {datos_nna['apellido']}' agregado correctamente"
            print(f"[OK] {success_msg}")
            self.view.mostrar_mensaje("Éxito", success_msg)
            
            if hasattr(self.view,'actualizar_vista_datos'):
                self.view.actualizar_vista_datos()
                return True
            
        except Exception as e:
            error_msg = f"Error al agregar NNA: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.view.mostrar_mensaje("Error", error_msg, "error")
            return False
    
    def generar_datos_prueba(self):
        """
        Genera datos de prueba para demostración
        """
        try:
            print("[PROCESANDO] Generando datos de prueba...")
            
            # Datos de prueba para NNA
            datos_prueba_nna = [
                {
                    'id': 1,
                    'nombre': 'Ana',
                    'apellido': 'García',
                    'edad': 14,
                    'genero': 'Femenino',
                    'fecha_ingreso': '2024-01-15',
                    'estado': 'Activo'
                },
                {
                    'id': 2,
                    'nombre': 'Carlos',
                    'apellido': 'López',
                    'edad': 16,
                    'genero': 'Masculino',
                    'fecha_ingreso': '2024-02-20',
                    'estado': 'Activo'
                }
            ]
            
            # Datos de prueba para alertas
            datos_prueba_alertas = [
                {
                    'id': 1,
                    'nna_id': 1,
                    'tipo_alerta': 'Académica',
                    'descripcion': 'Bajo rendimiento escolar',
                    'fecha_alerta': '2024-03-01',
                    'estado': 'Pendiente'
                }
            ]
            
            # Datos de prueba para seguimientos
            datos_prueba_seguimientos = [
                {
                    'id': 1,
                    'nna_id': 1,
                    'fecha_seguimiento': '2024-03-05',
                    'observaciones': 'Mejoría notable en comportamiento',
                    'responsable': 'Psicóloga María'
                }
            ]
            
            # Reemplazar datos actuales con datos de prueba
            self.datos_nna = datos_prueba_nna
            self.datos_alertas = datos_prueba_alertas
            self.datos_seguimientos = datos_prueba_seguimientos
            
            success_msg = "Datos de prueba generados exitosamente"
            print(f"[OK] {success_msg}")
            self.view.mostrar_mensaje("Éxito", success_msg)
            
            # Actualizar vistas
            if hasattr(self.view, 'actualizar_vista_datos'):
                self.view.actualizar_vista_datos()
                
        except Exception as e:
            error_msg = f"Error al generar datos de prueba: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.view.mostrar_mensaje("Error", error_msg, "error")
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del sistema
        
        Returns:
            Dict: Estadísticas del sistema
        """
        try:
            print("[PROCESANDO] Obteniendo estadísticas...")
            
            estadisticas = {
                'total_nna': len(self.datos_nna),
                'total_alertas': len(self.datos_alertas),
                'total_seguimientos': len(self.datos_seguimientos),
                'nna_activos': len([nna for nna in self.datos_nna if nna.get('estado') == 'Activo']),
                'alertas_pendientes': len([alerta for alerta in self.datos_alertas if alerta.get('estado') == 'Pendiente']),
                'fecha_actualizacion': datetime.now().isoformat()
            }
            
            print(f"[OK] Estadísticas obtenidas: {estadisticas}")
            return estadisticas
            
        except Exception as e:
            print(f"[ERROR] Error al obtener estadísticas: {e}")
            return {}
    
    def buscar_datos(self, tipo: str, criterio: str, valor: str) -> List[Dict[str, Any]]:
        """
        Busca datos según criterios específicos
        
        Args:
            tipo (str): Tipo de datos a buscar
            criterio (str): Campo por el cual buscar
            valor (str): Valor a buscar
            
        Returns:
            List[Dict]: Resultados de la búsqueda
        """
        try:
            print(f"[BUSCANDO] Buscando {tipo} por {criterio}: {valor}")
            
            datos = self.obtener_datos_por_tipo(tipo)
            if not datos:
                return []
            
            # Filtrar datos (búsqueda simple)
            resultados = []
            for item in datos:
                if criterio in item and str(item.get(criterio, '')).lower().find(valor.lower()) != -1:
                    resultados.append(item)
            
            print(f"[OK] Encontrados {len(resultados)} resultados")
            return resultados
            
        except Exception as e:
            print(f"[ERROR] Error en búsqueda: {e}")
            return []