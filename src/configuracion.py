
# ============================================
# EVENTBOT - CONFIGURACIÓN DEL PROYECTO
# ============================================

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConfiguracionEventBot:

    nombre_proyecto: str = "EventBot"
    nombre_salon: str = "Salón Destellos"

    ruta_proyecto: str = "/content/EventBot"

    idioma: str = "es"

    capacidad_minima: int = 50
    capacidad_maxima: int = 300

    @property
    def ruta_data(self):
        return Path(self.ruta_proyecto) / "data"

    @property
    def ruta_evidencias(self):
        return Path(self.ruta_proyecto) / "evidencias"

    @property
    def ruta_resultados(self):
        return Path(self.ruta_proyecto) / "resultados"

    def crear_directorios(self):
        self.ruta_data.mkdir(parents=True, exist_ok=True)
        self.ruta_evidencias.mkdir(parents=True, exist_ok=True)
        self.ruta_resultados.mkdir(parents=True, exist_ok=True)
