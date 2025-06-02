from datetime import datetime, timedelta
from collections import deque
from typing import List, Dict
import threading

from models.logs import Log
from config import CACHE_TTL_SECONDS

class EcoWatchCache:
    """
    Caché en memoria para almacenar logs recientes (últimos 5 minutos).
    Utiliza un deque para manejar eficientemente la ventana de tiempo.
    """
    def __init__(self, ttl_seconds: int = CACHE_TTL_SECONDS):
        self.ttl_seconds = ttl_seconds
        self._logs: deque[Log] = deque()
        self._logs_by_room: Dict[str, List[Log]] = {}
        self._lock = threading.Lock()
        
    def add_log(self, log: Log):
        """Añade un log al caché y mantiene la ventana de tiempo."""
        with self._lock:
            self._logs.append(log)
            self._prune_old_logs()
            self._update_indices()

    def add_logs(self, logs: List[Log]):
        """Añade múltiples logs al caché."""
        with self._lock:
            for log in logs:
                self._logs.append(log)
            self._logs = deque(sorted(self._logs, key=lambda l: l.timestamp))
            self._prune_old_logs()
            self._update_indices()

    def _prune_old_logs(self):
        """Elimina logs que están fuera de la ventana de tiempo (ttl_seconds)."""
        cutoff_time = datetime.now() - timedelta(seconds=self.ttl_seconds)
        while self._logs and self._logs[0].timestamp < cutoff_time:
            self._logs.popleft() # Elimina del inicio (los más antiguos)

    def _update_indices(self):
        """Reconstruye los índices para consultas rápidas."""
        self._logs_by_room.clear()
        for log in self._logs:
            if log.room not in self._logs_by_room:
                self._logs_by_room[log.room] = []
            self._logs_by_room[log.room].append(log)

    def get_logs_by_room(self, room: str) -> List[Log]:
        """Obtiene todos los logs recientes para una sala específica."""
        with self._lock:
            return self._logs_by_room.get(room, [])

    def get_logs_by_timestamp_range(self, start_time: datetime, end_time: datetime) -> List[Log]:
        """Obtiene logs dentro de un rango de tiempo específico."""
        with self._lock:
            result = []
            for log in self._logs:
                if start_time <= log.timestamp <= end_time:
                    result.append(log)
                elif log.timestamp > end_time: 
                    break
            return result
        
    def get_all_recent_logs(self) -> List[Log]:
        """Obtiene todos los logs actualmente en caché."""
        with self._lock:
            return list(self._logs)

    def __len__(self):
        with self._lock:
            return len(self._logs)

    def __repr__(self):
        with self._lock:
            return f"EcoWatchCache(logs={len(self._logs)}, ttl_seconds={self.ttl_seconds})"