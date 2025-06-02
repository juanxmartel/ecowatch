from datetime import datetime

class Log:
    """Representa un registro de sensor individual."""
    def __init__(self, timestamp: str, sensor_type: str, room: str, temperature: float, humidity: float, co2_level: float):
        try:
            self.timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00')) 
        except ValueError:
            raise ValueError(f"Formato de timestamp inválido: {timestamp}")
        self.sensor_type = sensor_type
        self.room = room
        self.temperature = temperature
        self.humidity = humidity
        self.co2_level = co2_level

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "tipo": self.sensor_type,
            "sala": self.room,
            "temperatura": self.temperature,
            "humedad": self.humidity,
            "co2": self.co2_level,
        }

    def __repr__(self):
        return (f"Log(timestamp={self.timestamp}, tipo='{self.sensor_type}', sala='{self.room}', "
                f"temp={self.temperature}, hum={self.humidity}, co2={self.co2_level})")
