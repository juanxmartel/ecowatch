import pandas as pd
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from models.logs import Log
import functools

# Decorador para logging 
def log_method_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"DEBUG: Llamando a {func.__name__} con args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"DEBUG: {func.__name__} completado.")
        return result
    return wrapper

class LogValidator:
    """Clase para validar la estructura y el contenido de los logs."""
    REQUIRED_FIELDS = ["timestamp", "tipo", "sala", "temperatura", "humedad", "co2"]

    @staticmethod
    def validate(log_data: Dict[str, Any]) -> bool:
        """Valida que un diccionario de log contenga los campos requeridos y tipos correctos."""
        for field in LogValidator.REQUIRED_FIELDS:
            if field not in log_data:
                print(f"WARN: Log mal formado - falta el campo '{field}': {log_data}")
                return False
        
        # Validar tipos de datos básicos (ejemplo)
        if not isinstance(log_data.get("timestamp"), str): return False
        if not isinstance(log_data.get("tipo"), str): return False
        if not isinstance(log_data.get("sala"), str): return False
        if not isinstance(log_data.get("temperatura"), (int, float)): return False
        if not isinstance(log_data.get("humedad"), (int, float)): return False
        if not isinstance(log_data.get("co2"), (int, float)): return False
        
        return True

class LogSource(ABC):
    """Interfaz abstracta para diferentes fuentes de logs."""
    @abstractmethod
    def read_logs(self) -> List[Dict[str, Any]]:
        pass

class CSVLogSource(LogSource):
    """Implementación para leer logs desde un archivo CSV."""
    def __init__(self, filepath: str):
        self.filepath = filepath

    @log_method_call
    def read_logs(self) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(self.filepath)
            # Renombrar columnas para que coincidan con los campos esperados
            df = df.rename(columns={
                "Timestamp": "timestamp",
                "SensorType": "tipo",
                "Room": "sala",
                "Temperature": "temperatura",
                "Humidity": "humedad",
                "CO2Level": "co2"
            })
            return df.to_dict(orient="records")
        except FileNotFoundError:
            print(f"ERROR: Archivo no encontrado en {self.filepath}")
            return []
        except Exception as e:
            print(f"ERROR: Error al leer CSV: {e}")
            return []

class InMemoryLogSource(LogSource):
    """Implementación para simular logs en memoria."""
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    @log_method_call
    def read_logs(self) -> List[Dict[str, Any]]:
        return self.data

class LogProcessor:
    """Procesa logs de una fuente, los valida y los convierte a objetos Log."""
    def __init__(self, source: LogSource):
        self.source = source

    @log_method_call
    def process_new_logs(self) -> List[Log]:
        raw_logs = self.source.read_logs()
        processed_logs = []
        for log_data in raw_logs:
            if LogValidator.validate(log_data):
                try:
                    processed_logs.append(Log(**log_data))
                except ValueError as e:
                    print(f"WARN: Error al crear objeto Log: {e} en datos: {log_data}")
            else:
                print(f"WARN: Log descartado por validación fallida: {log_data}")
        return processed_logs