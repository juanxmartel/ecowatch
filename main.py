import time
from datetime import datetime, timedelta
import os
import pandas as pd
import logging

from models.Data_ingestion import CSVLogSource, InMemoryLogSource, LogProcessor
from cache import EcoWatchCache
from models.report_factory import ReportFactory
from models.report_strategy import CSVReportStrategy
from config import REPORT_OUTPUT_DIR


logging.basicConfig(
    level=logging.INFO, # Nivel de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(), 
        logging.FileHandler("ecowatch.log") 
    ]
)

logger = logging.getLogger(__name__)

def run_simulation():
    logger.info("Iniciando simulación del sistema EcoWatch...")

    # 1. Configuración de fuentes de logs
    csv_source = CSVLogSource("logs_ambientales_ecowatch.csv")
    csv_processor = LogProcessor(csv_source)

    # Simular una fuente en memoria para probar "late events"
    # Este log llegará con un timestamp antiguo pero será procesado después
    late_event_data = [
        {"timestamp": "2023-01-01T10:00:05Z", "tipo": "Temperatura", "sala": "Sala B", "temperatura": 22.5, "humedad": 55.0, "co2": 450.0},
        {"timestamp": "2023-01-01T10:01:10Z", "tipo": "CO2", "sala": "Sala C", "temperatura": 20.0, "humedad": 50.0, "co2": 900.0} # Alerta crítica
    ]
    in_memory_source = InMemoryLogSource(late_event_data)
    in_memory_processor = LogProcessor(in_memory_source)

    cache = EcoWatchCache()

    logger.info("\nProcesando logs desde CSV...")
    initial_logs = csv_processor.process_new_logs()
    logger.info(f"Logs leídos del CSV: {len(initial_logs)}")
    
    # Añadir al caché. Simular un lapso de tiempo para que algunos queden fuera del TTL
    # Para la simulación, vamos a añadir todos los logs del CSV, y luego los "late events".
    cache.add_logs(initial_logs)
    logger.info(f"Logs en caché después de CSV: {len(cache)}")
    
    # 4. Simular la llegada de "late events" después de un tiempo
    logger.info("\nSimulando la llegada de 'late events'...")
    time.sleep(2) # Esperar un poco para simular el paso del tiempo
    late_logs = in_memory_processor.process_new_logs()
    logger.info(f"Logs 'late events' procesados: {len(late_logs)}")
    cache.add_logs(late_logs)
    logger.info(f"Logs en caché después de 'late events': {len(cache)}")
    
    # 5. Realizar consultas al caché
    logger.info("\nConsultando el caché:")
    sala_a_logs = cache.get_logs_by_room("Sala A")
    logger.info(f"Logs recientes en 'Sala A': {len(sala_a_logs)}")
    if sala_a_logs:
        logger.info(f"Último log en Sala A: {sala_a_logs[-1]}")

    # Consultar logs en un rango de tiempo específico (ej. últimos 3 minutos, asumiendo datos simulados actuales)
    # Ajustar el rango de tiempo si los timestamps del CSV son muy antiguos.
    # Para este ejemplo, tomaremos los logs más recientes del caché.
    all_current_logs_in_cache = cache.get_all_recent_logs()
    if all_current_logs_in_cache:
        # Asumimos que los timestamps del CSV son relativamente recientes para esta simulación
        # Si no, ajusta el rango de tiempo o los datos del CSV.
        
        # Para que funcione con los datos del CSV adjunto:
        # Buscar el timestamp más reciente del CSV y usarlo como base.
        max_timestamp_csv = max(log.timestamp for log in initial_logs) if initial_logs else datetime.now()
        
        start_range = max_timestamp_csv - timedelta(minutes=2)
        end_range = max_timestamp_csv + timedelta(minutes=1) 
        
        logs_in_range = cache.get_logs_by_timestamp_range(start_range, end_range)
        logger.info(f"Logs entre {start_range.strftime('%H:%M:%S')} y {end_range.strftime('%H:%M:%S')}: {len(logs_in_range)}")


    
    logger.info("\nGenerando reportes...")
    os.makedirs(REPORT_OUTPUT_DIR, exist_ok=True)

    # Convertir los logs en caché a un DataFrame de pandas para los reportes
    if all_current_logs_in_cache:
        report_data = pd.DataFrame([log.to_dict() for log in all_current_logs_in_cache])
        report_data['timestamp'] = pd.to_datetime(report_data['timestamp'])

        # Reporte de Estado por Sala
        room_status_report = ReportFactory.create_report("room_status", report_data)
        csv_strategy = CSVReportStrategy()
        csv_strategy.execute(room_status_report, REPORT_OUTPUT_DIR)

        # Reporte de Alertas Críticas
        critical_alerts_report = ReportFactory.create_report("critical_alerts", report_data, co2_threshold=800, temp_threshold=30)
        csv_strategy.execute(critical_alerts_report, REPORT_OUTPUT_DIR)
        
        # Ejemplo de cómo sería un reporte con umbrales diferentes
        # critical_alerts_report_low_co2 = ReportFactory.create_report("critical_alerts", report_data, co2_threshold=400)
        # csv_strategy.execute(critical_alerts_report_low_co2, REPORT_OUTPUT_DIR)

    else:
        logger.info("No hay datos en caché para generar reportes.")

    logger.info("\nSimulación finalizada.")

if __name__ == "__main__":
    run_simulation()