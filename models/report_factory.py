import pandas as pd

from models.reportes import Report, RoomStatusReport, CriticalAlertsReport
from config import REPORT_OUTPUT_DIR

class ReportFactory:
    """Factoría para crear diferentes tipos de reportes (Patrón Factory)."""
    _reports = {
        "room_status": RoomStatusReport,
        "critical_alerts": CriticalAlertsReport,
        # Aquí se pueden añadir nuevos tipos de reportes fácilmente
    }

    @staticmethod
    def create_report(report_type: str, data: pd.DataFrame, **kwargs) -> Report:
        report_class = ReportFactory._reports.get(report_type)
        if not report_class:
            raise ValueError(f"Tipo de reporte '{report_type}' no soportado.")
        return report_class(data, **kwargs)

    @staticmethod
    def get_available_reports():
        return list(ReportFactory._reports.keys())