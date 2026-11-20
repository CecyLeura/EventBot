from src.configuracion import ConfiguracionEventBot

# ============================================
# EVENTBOT - APLICACIÓN PRINCIPAL
# Salón Destellos
# ============================================

from datetime import datetime
from pathlib import Path
import json

from src.base_conocimiento import BaseConocimiento
from src.detector_intenciones import DetectorIntenciones
from src.gestor_conversacion import GestorConversacion
from src.clasificador_imagenes import ClasificadorImagenes


class EventBot:
    """
    Clase principal del chatbot EventBot.

    Integra:
    - BaseConocimiento
    - DetectorIntenciones
    - GestorConversacion

    Administra una sesión y su historial.
    """


    def __init__(self, ruta_proyecto=None, ruta_modelo_cnn=None):

        if ruta_proyecto is None:
            self.config = ConfiguracionEventBot()
        else:
            self.config = ConfiguracionEventBot(
                ruta_proyecto=str(ruta_proyecto)
            )

        self.config.crear_directorios()

        self.ruta_proyecto = Path(
            self.config.ruta_proyecto
        )

        self.base = BaseConocimiento(
            self.config.ruta_data
        )

        self.detector = DetectorIntenciones()

        self.gestor = GestorConversacion(self.base)

        self.historial = []

        self.contexto = {
            "paquete": None
        }

        self.clasificador_visual = (
            ClasificadorImagenes(ruta_modelo_cnn)
            if ruta_modelo_cnn is not None
            else None
        )

        self.sesion_activa = False

    # ----------------------------------------
    # INICIAR SESIÓN
    # ----------------------------------------

    def iniciar_sesion(self):

        self.historial = []
        self.contexto = {
            "paquete": None
        }
        self.sesion_activa = True

        return (
            "¡Bienvenido a Salón Destellos! "
            "Soy EventBot, tu asistente virtual. "
            "Puedo ayudarte con paquetes, precios, "
            "disponibilidad, promociones y reservaciones. "
            "Escribe 'salir' para terminar la conversación."
        )

    # ----------------------------------------
    # PROCESAR MENSAJE
    # ----------------------------------------

    def responder(self, mensaje):

        if not self.sesion_activa:
            self.iniciar_sesion()

        if not isinstance(mensaje, str):
            raise TypeError("El mensaje debe ser texto.")

        if not mensaje.strip():
            return "Por favor, escribe una consulta."

        analisis = self.detector.analizar(mensaje)

        # Obtener entidades detectadas
        entidades = analisis["entidades"]

        # Guardar el paquete mencionado por el usuario
        if entidades.get("paquete"):
            self.contexto["paquete"] = entidades["paquete"]

        # Recuperar el paquete anterior en consultas de costos
        elif (
            analisis["intencion"] == "costos"
            and self.contexto.get("paquete")
        ):
            entidades["paquete"] = self.contexto["paquete"]

        # Detectar todas las intenciones del mensaje
        intenciones = (
            self.detector.detectar_intenciones_multiples(
                mensaje
            )
        )

        # Generar respuesta segun las intenciones
        if len(intenciones) > 1:
            respuesta = (
                self.gestor.generar_respuestas_multiples(
                    analisis,
                    intenciones
                )
            )
        else:
            respuesta = self.gestor.generar_respuesta(
                analisis
            )

        registro = {
            "fecha_hora": datetime.now().isoformat(
                timespec="seconds"
            ),
            "usuario": mensaje,
            "intencion": analisis["intencion"],
            "intenciones_detectadas": intenciones,
            "entidades": analisis["entidades"],
            "respuesta": respuesta
        }

        self.historial.append(registro)

        return respuesta

    # ----------------------------------------
    # OBTENER HISTORIAL
    # ----------------------------------------


    # ----------------------------------------
    # PROCESAR IMAGEN
    # ----------------------------------------

    def responder_imagen(self, ruta_imagen):
        """Clasifica una imagen y registra la respuesta."""

        if not self.sesion_activa:
            self.iniciar_sesion()

        if self.clasificador_visual is None:
            return (
                "El clasificador visual no está configurado. "
                "Proporciona la ruta del modelo CNN."
            )

        resultado = self.clasificador_visual.clasificar(
            ruta_imagen
        )

        nombres = {
            "boda": "boda",
            "corporativo": "evento corporativo",
            "xv_anos": "fiesta de XV años"
        }

        categoria = resultado["categoria"]
        confianza = resultado["confianza"]

        respuesta = (
            f"Según el análisis de la fotografía, "
            f"el evento parece ser una {nombres[categoria]} "
            f"(puntuación del modelo: {confianza:.1%}). "
            f"Esta clasificación es orientativa."
        )

        registro = {
            "fecha_hora": datetime.now().isoformat(
                timespec="seconds"
            ),
            "tipo_entrada": "imagen",
            "usuario": str(ruta_imagen),
            "intencion": "clasificacion_visual",
            "intenciones_detectadas": ["clasificacion_visual"],
            "entidades": {
                "categoria": categoria,
                "confianza": confianza
            },
            "respuesta": respuesta
        }

        self.historial.append(registro)

        return respuesta

    def obtener_historial(self):

        return [
            registro.copy()
            for registro in self.historial
        ]

    # ----------------------------------------
    # GUARDAR HISTORIAL
    # ----------------------------------------

    def guardar_historial(self, nombre_archivo=None):

        carpeta = self.ruta_proyecto / "evidencias"
        carpeta.mkdir(parents=True, exist_ok=True)

        if nombre_archivo is None:
            fecha = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            nombre_archivo = (
                f"conversacion_{fecha}.json"
            )

        ruta = carpeta / nombre_archivo

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(
                self.historial,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        return ruta

    # ----------------------------------------
    # FINALIZAR SESIÓN
    # ----------------------------------------

    def finalizar_sesion(self):

        self.sesion_activa = False

        return (
            "¡Gracias por visitar Salón Destellos! "
            "Esperamos ayudarte con tu próximo evento."
        )

    # ----------------------------------------
    # CONVERSACIÓN INTERACTIVA
    # ----------------------------------------

    def conversar(self):

        print("=" * 55)
        print("EVENTBOT - SALÓN DESTELLOS")
        print("=" * 55)

        print("\nEventBot:", self.iniciar_sesion())

        while self.sesion_activa:

            try:
                mensaje = input("\nCliente: ")

            except (EOFError, KeyboardInterrupt):
                print("\nSesión interrumpida.")
                break

            if mensaje.strip().lower() in {
                "salir", "exit", "terminar"
            }:
                print("\nEventBot:", self.finalizar_sesion())
                break

            respuesta = self.responder(mensaje)

            print("\nEventBot:", respuesta)

        self.sesion_activa = False

        if self.historial:
            ruta = self.guardar_historial()
            print("\nHistorial guardado en:", ruta)
