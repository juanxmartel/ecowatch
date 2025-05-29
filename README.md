
# ecowatch

* **Simulación de Fuentes de Logs:** Soporte para lectura de datos desde archivos CSV y datos en memoria.
* **Validación de Datos:** Reglas claras para asegurar la calidad de los datos de entrada.
* **Caché en Memoria:**  La principal optimización para el acceso rápido a datos recientes. Al mantener solo los últimos 5 minutos de datos en memoria y usar un deque para la purgar eficiente, se reduce significativamente la latencia de consulta en comparación con la lectura de una base de datos o disco.
* **Indexacion:**  _logs_by_room en EcoWatchCache Al mantener un diccionario de listas indexadas por sala, las consultas get_logs_by_room tienen un rendimiento cercano a O(1) (ignorando la iteración sobre la lista de logs de esa sala), en lugar de O(n) si se tuviera que filtrar el deque completo en cada consulta. 

* **Diseño Orientado a Objetos (POO):** Clases (`Log`, `Sensor`, `Sala`, `Report`) que encapsulan datos y comportamientos.
* **Generación de Reportes:**
    * Implementación de dos tipos de reportes: "Estado por Sala" y "Alertas Críticas".
    * Uso del patrón **Factory Method** para la creación de reportes.
    * Uso del patrón **Strategy** para la lógica de exportación de reportes (actualmente CSV).
    * Diseño extensible para añadir nuevos tipos de reportes sin modificar el código existente.
* **Logging:** Integración del módulo `logging` de Python para un control detallado de la salida del sistema.
* **Configuración:** Uso de variables de entorno (`.env`) para la configuración del sistema.


##  Configuración e Instalación

Para ejecutar este proyecto, sigue los siguientes pasos:

1.  **Clonar el repositorio**
2.  **Asegúrate de tener Python instalado.**
3.  **Crear un entorno virtual**:
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate

    ```
4.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Crear el archivo de configuración `.env`:**
    En la raíz del proyecto (al mismo nivel que la carpeta `ecowatch`), crea un archivo llamado `.env` con el siguiente contenido:
    ```ini
    CACHE_TTL_SECONDS=300
    REPORT_OUTPUT_DIR=reports_output
    ```
    * `CACHE_TTL_SECONDS`: Tiempo de vida de los logs en el caché en segundos (por defecto, 300 segundos = 5 minutos).
    * `REPORT_OUTPUT_DIR`: Directorio donde se guardarán los reportes generados.

##  Uso

Para ejecutar la simulación del sistema EcoWatch y generar los reportes:

```bash
python ecowatch/main.py

