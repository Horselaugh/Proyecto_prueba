import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

# ----------------------------------------------------------------------
# MOCKS (TEMPORAL)
# ----------------------------------------------------------------------
class MockReportesModel:
    """Simulación del modelo de base de datos para reportes."""
    def obtener_datos_nna(self):
        return [
            {'id': 1, 'nombre': 'Ana', 'genero': 'Femenino', 'edad': 10, 'alerta_activa': True},
            {'id': 2, 'nombre': 'Luis', 'genero': 'Masculino', 'edad': 12, 'alerta_activa': False},
            {'id': 3, 'nombre': 'Sofía', 'genero': 'Femenino', 'edad': 8, 'alerta_activa': True},
            {'id': 4, 'nombre': 'Pedro', 'genero': 'Masculino', 'edad': 15, 'alerta_activa': True},
        ]
    def obtener_datos_alertas(self):
        return [
            {'id': 101, 'nna_id': 1, 'estado': 'Abierto', 'tipo': 'Abandono'},
            {'id': 102, 'nna_id': 3, 'estado': 'Abierto', 'tipo': 'Maltrato'},
            {'id': 103, 'nna_id': 4, 'estado': 'Cerrado', 'tipo': 'Riesgo'},
        ]
    def obtener_total_nna(self): return len(self.obtener_datos_nna())
    def obtener_alertas_activas_count(self): return len([a for a in self.obtener_datos_alertas() if a['estado'] == 'Abierto'])

class MockExportadorService:
    """Simulación del servicio de exportación."""
    def exportar_csv(self, data, filename):
        return {"status": "success", "message": f"Datos exportados a CSV: {filename}.csv"}

# Asumiendo que el modelo real existe si no hay excepción
try:
    from models.reportes_model import ReportesModel, ExportadorService
except ImportError:
    ReportesModel = MockReportesModel
    ExportadorService = MockExportadorService


class ReportesControlador:
    """Controlador para manejar la lógica de reportes y estadísticas"""
    
    def __init__(self):
        self.vista = None
        self.model = ReportesModel()
        self.exportador = ExportadorService()
        
        # Definición de reportes disponibles para la vista
        self.reportes_disponibles = {
            "NNA_GENERAL": "Reporte General de NNA",
            "ALERTAS_ACTIVAS": "Alertas Activas y Estado",
            "NNA_POR_GENERO": "NNA por Género (Gráfico)",
        }
        self.data_cache: Dict[str, List[Dict]] = {} # Cache para datos del último reporte generado
        
    def set_view(self, view_instance):
        """Establece la instancia de la vista."""
        self.vista = view_instance

    def load_initial_data(self):
        """Llama a la vista para cargar los reportes disponibles y las estadísticas iniciales."""
        if not self.vista: return

        self.vista._cargar_reportes_disponibles(self.reportes_disponibles)
        
        try:
            # 1. Obtener estadísticas de resumen
            stats = self._obtener_estadisticas_resumen()
            self.vista.display_stats(stats)
            
            self.vista.display_message("Datos iniciales y estadísticas cargados. Seleccione un reporte.", is_success=True)

        except Exception as e:
            self.vista.display_message(f"❌ Error al cargar datos iniciales: {str(e)}", is_success=False)

    def _obtener_estadisticas_resumen(self) -> Dict:
        """Calcula y devuelve las estadísticas de resumen."""
        total_nna = self.model.obtener_total_nna()
        alertas_activas = self.model.obtener_alertas_activas_count()
        
        return {
            'total_nna': total_nna,
            'alertas_activas': alertas_activas,
            'fecha_actualizacion': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

    def _obtener_datos_genero_count(self) -> Dict[str, int]:
        """Prepara los datos para el gráfico de NNA por género."""
        nna_data = self.model.obtener_datos_nna()
        genero_counts = {}
        for nna in nna_data:
            genero = nna.get('genero', 'Desconocido')
            genero_counts[genero] = genero_counts.get(genero, 0) + 1
        return genero_counts

    def handle_generar_reporte(self, reporte_key: str):
        """Maneja la generación y visualización de un reporte específico."""
        if not self.vista: return

        try:
            if reporte_key == "NNA_GENERAL":
                data = self.model.obtener_datos_nna()
                self.data_cache["NNA_GENERAL"] = data
                # La vista recibe los datos, las columnas para la tabla, y el título
                self.vista.display_results(data, ["id", "nombre", "genero", "edad", "alerta_activa"], "Reporte General de NNA")
                self.vista._plot_chart(None, None) # Limpiar gráfico
                
            elif reporte_key == "ALERTAS_ACTIVAS":
                data = [a for a in self.model.obtener_datos_alertas() if a['estado'] == 'Abierto']
                self.data_cache["ALERTAS_ACTIVAS"] = data
                self.vista.display_results(data, ["id", "nna_id", "tipo", "estado"], "Alertas Activas")
                self.vista._plot_chart(None, None) # Limpiar gráfico
                
            elif reporte_key == "NNA_POR_GENERO":
                # Para gráficos, el controlador prepara los datos resumidos
                data = self._obtener_datos_genero_count()
                self.data_cache["NNA_POR_GENERO"] = [] # No exportable como tabla simple
                self.vista.display_results([], [], "Conteo de NNA por Género: Gráfico Generado")
                # La vista recibe el tipo de gráfico y los datos
                self.vista._plot_chart("bar_genero", data)
                
            else:
                self.vista.display_message("❌ Tipo de reporte no reconocido.", False)
                self.vista.display_results([], [], "Resultados")
                return # Salir si el reporte no es válido

            self.vista.display_message(f"✅ Reporte '{self.reportes_disponibles.get(reporte_key)}' generado.", True)

        except Exception as e:
            self.vista.display_message(f"❌ Error al generar reporte: {str(e)}", is_success=False)

    def handle_exportar_reporte(self, reporte_key: str):
        """Maneja la exportación del reporte actualmente en caché (solo para datos de tabla)."""
        if not self.vista: return
        
        data_to_export = self.data_cache.get(reporte_key)
        
        if not data_to_export:
            self.vista.display_message("❌ No hay datos en caché para exportar. Genere el reporte primero.", False)
            return

        try:
            # Simulación de la exportación con un nombre de archivo
            filename = f"Reporte_{reporte_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            resultado = self.exportador.exportar_csv(data_to_export, filename)
            
            if resultado.get("status") == "success":
                self.vista.display_message(f"✅ Exportación exitosa: {resultado['message']}", True)
            else:
                self.vista.display_message(f"❌ Error de exportación: {resultado.get('message', 'Desconocido')}", False)

        except Exception as e:
            self.vista.display_message(f"❌ Error interno al exportar: {str(e)}", is_success=False)