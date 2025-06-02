from models.logs import Log

class Sensor:
    """Representa un sensor con sus atributos."""
    def __init__(self, sensor_id: str, sensor_type: str, room: str):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.room = room
        self.logs = [] # Podría almacenar un historial de logs asociados a este sensor

    def add_log(self, log: Log):
        if log.room != self.room or log.sensor_type != self.sensor_type:
            raise ValueError("El log no corresponde a este sensor.")
        self.logs.append(log)

    def __repr__(self):
        return f"Sensor(id='{self.sensor_id}', tipo='{self.sensor_type}', sala='{self.room}')"
