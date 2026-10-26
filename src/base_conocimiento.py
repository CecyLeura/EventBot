
# ============================================
# EVENTBOT - BASE DE CONOCIMIENTO
# Salón Destellos
# ============================================

import json
from pathlib import Path
from datetime import date


class BaseConocimiento:
    """
    Administra la información del Salón Destellos
    almacenada en archivos JSON.
    """

    def __init__(self, ruta_data):

        self.ruta_data = Path(ruta_data)

        self.informacion_salon = self._cargar_json(
            "informacion_salon.json"
        )

        self.paquetes = self._cargar_json(
            "paquetes.json"
        )

        self.disponibilidad = self._cargar_json(
            "disponibilidad.json"
        )

        self.promociones = self._cargar_json(
            "promociones.json"
        )

    # ----------------------------------------
    # CARGA DE ARCHIVOS
    # ----------------------------------------

    def _cargar_json(self, nombre_archivo):
        """Carga un archivo JSON y devuelve sus datos."""

        ruta = self.ruta_data / nombre_archivo

        if not ruta.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo: {ruta}"
            )

        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    # ----------------------------------------
    # INFORMACIÓN GENERAL
    # ----------------------------------------

    def obtener_informacion_salon(self):
        """Devuelve la información general del salón."""

        return self.informacion_salon.copy()

    def obtener_capacidad(self):
        """Devuelve la capacidad máxima del salón."""

        return self.informacion_salon["capacidad_maxima"]

    def obtener_amenidades(self):
        """Devuelve las amenidades disponibles."""

        return self.informacion_salon["amenidades"].copy()

    def obtener_tipos_eventos(self):
        """Devuelve los tipos de eventos que se atienden."""

        return self.informacion_salon["tipos_eventos"].copy()

    # ----------------------------------------
    # PAQUETES Y PRECIOS
    # ----------------------------------------

    def obtener_paquetes(self):
        """Devuelve todos los paquetes disponibles."""

        return [p.copy() for p in self.paquetes]

    def buscar_paquete(self, nombre):
        """Busca un paquete por su nombre."""

        nombre = nombre.strip().casefold()

        for paquete in self.paquetes:

            if paquete["nombre"].casefold() == nombre:
                return paquete.copy()

        return None

    def recomendar_paquete(self, invitados):
        """
        Recomienda el paquete de menor capacidad
        que pueda atender al número de invitados.
        """

        if not isinstance(invitados, int) or isinstance(invitados, bool):
            raise ValueError(
                "El número de invitados debe ser un entero."
            )

        if invitados < self.informacion_salon["capacidad_minima"]:
            return None

        opciones = [
            paquete
            for paquete in self.paquetes
            if paquete["capacidad_maxima"] >= invitados
        ]

        if not opciones:
            return None

        opciones.sort(
            key=lambda p: (p["capacidad_maxima"], p["precio"])
        )

        return opciones[0].copy()

    # ----------------------------------------
    # DISPONIBILIDAD DE FECHAS
    # ----------------------------------------

    def consultar_disponibilidad(self, fecha):
        """
        Consulta una fecha en formato YYYY-MM-DD.

        Posibles resultados:
        disponible, ocupada, no_registrada,
        fecha_pasada o fecha_invalida.
        """

        try:
            fecha_consulta = date.fromisoformat(fecha)
        except (ValueError, TypeError):
            return "fecha_invalida"

        if fecha_consulta < date.today():
            return "fecha_pasada"

        return self.disponibilidad.get(
            fecha,
            "no_registrada"
        )

    def obtener_fechas_disponibles(self):
        """Devuelve fechas futuras registradas como disponibles."""

        hoy = date.today()

        fechas = [
            fecha
            for fecha, estado in self.disponibilidad.items()
            if estado == "disponible"
            and date.fromisoformat(fecha) >= hoy
        ]

        return sorted(fechas)

    # ----------------------------------------
    # PROMOCIONES
    # ----------------------------------------

    def obtener_promociones(self, fecha_consulta=None):
        """
        Devuelve promociones vigentes en una fecha.

        Si no se proporciona una fecha,
        utiliza la fecha actual.
        """

        if fecha_consulta is None:
            fecha_consulta = date.today()

        elif isinstance(fecha_consulta, str):
            fecha_consulta = date.fromisoformat(fecha_consulta)

        promociones_vigentes = []

        for promocion in self.promociones:

            inicio = date.fromisoformat(
                promocion["fecha_inicio"]
            )

            fin = date.fromisoformat(
                promocion["fecha_fin"]
            )

            if inicio <= fecha_consulta <= fin:
                promociones_vigentes.append(
                    promocion.copy()
                )

        return promociones_vigentes
