from models.Sensor import Sensor
from models.logs import Log

class Sala:
    """Representa una sala o zona monitoreada."""
    def __init__(self, name: str):
        self.name = name
        self.sensors = {} # {sensor_id: Sensor_object}
        self.current_logs = [] # Logs más recientes para esta sala

    def add_sensor(self, sensor: Sensor):
        if sensor.room != self.name:
            raise ValueError(f"El sensor no pertenece a la sala {self.name}.")
        self.sensors[sensor.sensor_id] = sensor

    def update_logs(self, logs: list[Log]):
        # Esto podría ser más sofisticado, por ahora solo reemplaza los logs actuales
        self.current_logs = logs

    def __repr__(self):
        return f"Sala(name='{self.name}', sensores={len(self.sensors)})"
