
# ============================================
# EVENTBOT - DETECTOR DE INTENCIONES
# Salón Destellos
# ============================================

import re
from datetime import date

from src.procesador_texto import ProcesadorTexto


class DetectorIntenciones:
    """
    Detecta la intención principal del usuario
    mediante reglas y palabras clave.

    También extrae entidades:
    - Paquete
    - Número de invitados
    - Fecha
    """

    def __init__(self):

        self.procesador = ProcesadorTexto()

        self.paquetes = {
            "esencial": "Esencial",
            "clasico": "Clásico",
            "premium": "Premium",
            "diamante": "Diamante"
        }

        self.meses = {
            "enero": 1,
            "febrero": 2,
            "marzo": 3,
            "abril": 4,
            "mayo": 5,
            "junio": 6,
            "julio": 7,
            "agosto": 8,
            "septiembre": 9,
            "setiembre": 9,
            "octubre": 10,
            "noviembre": 11,
            "diciembre": 12
        }

    # ----------------------------------------
    # DETECTAR INTENCIÓN
    # ----------------------------------------

    def detectar_intencion(self, texto):

        normalizado = self.procesador.normalizar(texto)
        tokens = set(self.procesador.tokenizar(texto))

        def contiene_frase(frase):
            return (
                f" {frase} " in f" {normalizado} "
            )

        # 1. Disponibilidad
        if (
            tokens & {
                "disponible", "disponibilidad",
                "libre", "ocupado", "ocupada",
                "fecha", "fechas"
            }
            or contiene_frase("tienen lugar")
        ):
            return "disponibilidad"

        # 2. Reservaciones
        if (
            tokens & {
                "reservar", "reservacion",
                "apartar", "aparto", "anticipo"
            }
            or contiene_frase("como reservo")
            or contiene_frase("como puedo reservar")
        ):
            return "reservacion"

        # 3. Promociones
        if tokens & {
            "promocion", "promociones",
            "descuento", "descuentos", "oferta", "ofertas"
        }:
            return "promociones"

        # 4. Costos y precios
        if (
            tokens & {
                "precio", "precios", "costo",
                "costos", "cuesta", "cuestan",
                "cotizacion", "cotizar", "presupuesto"
            }
            or contiene_frase("cuanto vale")
            or contiene_frase("cuanto cobran")
        ):
            return "costos"

        # 5. Paquetes
        if tokens & {
            "paquete", "paquetes", "incluye",
            "incluyen", "contiene", "servicios"
        }:
            return "paquetes"

        # 6. Capacidad
        if (
            tokens & {
                "capacidad", "caben", "aforo"
            }
            or contiene_frase("cuantas personas")
            or contiene_frase("cuantos invitados")
        ):
            return "capacidad"

        # 7. Ubicación
        if (
            tokens & {
                "ubicacion", "direccion",
                "ubicados", "ubicado", "donde"
            }
            or contiene_frase("como llego")
        ):
            return "ubicacion"

        # 8. Horarios
        if tokens & {
            "horario", "horarios", "hora",
            "horas", "abren", "cierran"
        }:
            return "horarios"

        # 9. Amenidades
        if tokens & {
            "amenidades", "estacionamiento",
            "clima", "sonido", "iluminacion",
            "mesas", "sillas", "pista"
        }:
            return "amenidades"

        # 10. Tipos de eventos
        if tokens & {
            "boda", "bodas", "bautizo", "bautizos",
            "graduacion", "graduaciones",
            "cumpleanos", "aniversario", "aniversarios",
            "xv", "quinceanera", "quinceaneras"
        }:
            return "tipos_eventos"

        # 11. Agradecimiento
        if tokens & {
            "gracias", "agradezco"
        }:
            return "agradecimiento"

        # 12. Despedida
        if (
            tokens & {"adios", "bye", "hasta", "chao"}
            or contiene_frase("nos vemos")
        ):
            return "despedida"

        # 13. Saludo
        if (
            tokens & {"hola", "buenas", "saludos", "hey"}
            or contiene_frase("buenos dias")
            or contiene_frase("buenas tardes")
            or contiene_frase("buenas noches")
        ):
            return "saludo"

        return "desconocida"

    # ----------------------------------------
    # EXTRAER PAQUETE
    # ----------------------------------------

    def extraer_paquete(self, texto):

        tokens = self.procesador.tokenizar(texto)

        for token in tokens:
            if token in self.paquetes:
                return self.paquetes[token]

        return None

    # ----------------------------------------
    # EXTRAER NÚMERO DE INVITADOS
    # ----------------------------------------

    def extraer_invitados(self, texto):

        normalizado = self.procesador.normalizar(texto)

        patrones = [
            r"\b(\d{1,4})\s*(?:invitados|invitadas|personas)\b",
            r"\b(?:para|somos|seremos)\s+(\d{1,4})\b"
        ]

        for patron in patrones:

            coincidencia = re.search(patron, normalizado)

            if coincidencia:
                cantidad = int(coincidencia.group(1))

                if cantidad > 0:
                    return cantidad

        return None

    # ----------------------------------------
    # EXTRAER FECHA
    # ----------------------------------------

    def extraer_fecha(self, texto):

        normalizado = self.procesador.normalizar(texto)

        # Formato YYYY-MM-DD
        coincidencia = re.search(
            r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b",
            texto
        )

        if coincidencia:
            anio, mes, dia = map(
                int, coincidencia.groups()
            )

            try:
                return date(anio, mes, dia).isoformat()
            except ValueError:
                return None

        # Formato DD/MM/YYYY
        coincidencia = re.search(
            r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b",
            texto
        )

        if coincidencia:
            dia, mes, anio = map(
                int, coincidencia.groups()
            )

            try:
                return date(anio, mes, dia).isoformat()
            except ValueError:
                return None

        # Formato "15 de noviembre de 2026"
        patron = (
            r"\b(\d{1,2})\s+de\s+"
            r"([a-z]+)\s+de\s+(\d{4})\b"
        )

        coincidencia = re.search(patron, normalizado)

        if coincidencia:

            dia = int(coincidencia.group(1))
            mes_texto = coincidencia.group(2)
            anio = int(coincidencia.group(3))

            mes = self.meses.get(mes_texto)

            if mes:
                try:
                    return date(
                        anio, mes, dia
                    ).isoformat()
                except ValueError:
                    return None

        return None

    # ----------------------------------------
    # ANÁLISIS COMPLETO
    # ----------------------------------------

    def analizar(self, texto):

        procesamiento = self.procesador.procesar(texto)

        return {
            "texto_original": texto,
            "texto_normalizado": procesamiento[
                "texto_normalizado"
            ],
            "tokens_relevantes": procesamiento[
                "tokens_relevantes"
            ],
            "intencion": self.detectar_intencion(texto),
            "entidades": {
                "paquete": self.extraer_paquete(texto),
                "invitados": self.extraer_invitados(texto),
                "fecha": self.extraer_fecha(texto)
            }
        }
