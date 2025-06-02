from abc import ABC, abstractmethod
import pandas as pd
import os

from models.reportes import Report

class ReportStrategy(ABC):
    """Interfaz para la estrategia de generación de reportes (Patrón Strategy)."""
    @abstractmethod
    def execute(self, data: pd.DataFrame, output_path: str):
        pass

class CSVReportStrategy(ReportStrategy):
    """Estrategia para guardar reportes en formato CSV."""
    def execute(self, report_instance: Report, output_path: str):
        os.makedirs(output_path, exist_ok=True)
        report_instance.generate(output_path)
        