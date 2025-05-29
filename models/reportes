from pandas import pd
from datetime import datetime

class Report:
    """Clase base abstracta para todos los reportes."""
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.report_name = "Base Report"

    def generate(self, output_path: str):
        """Genera el reporte y lo guarda."""
        raise NotImplementedError

    def _prepare_data(self) -> pd.DataFrame:
        """Método para la pre-procesamiento de datos específico del reporte."""
        return self.data

class RoomStatusReport(Report):
    """Reporte del estado actual por sala."""
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        self.report_name = "Room_Status_Report"

    def _prepare_data(self) -> pd.DataFrame:
        # Agrupa por sala y obtiene el último registro para cada una
        latest_logs = self.data.loc[self.data.groupby('sala')['timestamp'].idxmax()]
        return latest_logs[['sala', 'temperatura', 'humedad', 'co2', 'timestamp']]

    def generate(self, output_path: str):
        prepared_data = self._prepare_data()
        filepath = f"{output_path}/{self.report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        prepared_data.to_csv(filepath, index=False)
        print(f"Reporte '{self.report_name}' generado en: {filepath}")

class CriticalAlertsReport(Report):
    """Reporte de alertas críticas (ej. CO2 > 800 ppm o Temp > 30)."""
    def __init__(self, data: pd.DataFrame, co2_threshold: int = 800, temp_threshold: int = 30):
        super().__init__(data)
        self.report_name = "Critical_Alerts_Report"
        self.co2_threshold = co2_threshold
        self.temp_threshold = temp_threshold

    def _prepare_data(self) -> pd.DataFrame:
        critical_alerts = self.data[
            (self.data['co2'] > self.co2_threshold) |
            (self.data['temperatura'] > self.temp_threshold)
        ]
        return critical_alerts[['timestamp', 'sala', 'temperatura', 'humedad', 'co2']]

    def generate(self, output_path: str):
        prepared_data = self._prepare_data()
        if not prepared_data.empty:
            filepath = f"{output_path}/{self.report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            prepared_data.to_csv(filepath, index=False)
            print(f"Reporte '{self.report_name}' generado en: {filepath}")
        else:
            print(f"No se encontraron alertas críticas para el reporte '{self.report_name}'.")
