
# ============================================
# EVENTBOT - GESTOR DE CONVERSACIÓN
# Salón Destellos
# ============================================

from datetime import date
from src.base_conocimiento import BaseConocimiento


class GestorConversacion:
    """
    Genera respuestas basadas en intenciones
    y en la información de Salón Destellos.
    """

    def __init__(self, base_conocimiento):
        self.base = base_conocimiento

    # ----------------------------------------
    # FORMATO DE PRECIOS
    # ----------------------------------------

    def _formatear_precio(self, precio):
        return f"${precio:,.2f} MXN"

    # ----------------------------------------
    # RESPUESTA PRINCIPAL
    # ----------------------------------------


    # ----------------------------------------
    # RESPUESTAS A MULTIPLES INTENCIONES
    # ----------------------------------------

    def generar_respuestas_multiples(
        self, analisis, intenciones
    ):

        respuestas = []

        # Evitar informacion repetida cuando se consulta
        # el precio y los servicios de un paquete especifico
        intenciones = list(intenciones)

        if (
            "costos" in intenciones
            and "paquetes" in intenciones
            and analisis["entidades"].get("paquete")
        ):
            intenciones.remove("paquetes")

        for intencion in intenciones:

            analisis_individual = {
                **analisis,
                "intencion": intencion
            }

            respuesta = self.generar_respuesta(
                analisis_individual
            )

            if respuesta not in respuestas:
                respuestas.append(respuesta)

        return " ".join(respuestas)

    def generar_respuesta(self, analisis):
        """
        Recibe el resultado de DetectorIntenciones
        y devuelve una respuesta para el cliente.
        """

        intencion = analisis["intencion"]
        entidades = analisis["entidades"]

        if intencion == "saludo":
            return self._responder_saludo()

        elif intencion == "costos":
            return self._responder_costos(entidades)

        elif intencion == "paquetes":
            return self._responder_paquetes(entidades)

        elif intencion == "disponibilidad":
            return self._responder_disponibilidad(entidades)

        elif intencion == "promociones":
            return self._responder_promociones()

        elif intencion == "amenidades":
            return self._responder_amenidades()

        elif intencion == "capacidad":
            return self._responder_capacidad(entidades)

        elif intencion == "ubicacion":
            return self._responder_ubicacion()

        elif intencion == "horarios":
            return self._responder_horarios()

        elif intencion == "reservacion":
            return self._responder_reservacion()

        elif intencion == "tipos_eventos":
            return self._responder_tipos_eventos()

        elif intencion == "agradecimiento":
            return "¡Con mucho gusto! ¿Puedo ayudarte con algo más?"

        elif intencion == "despedida":
            return (
                "¡Gracias por contactar a Salón Destellos! "
                "Esperamos ser parte de tu próxima celebración."
            )

        return (
            "Disculpa, no logré comprender tu consulta. "
            "Puedo ayudarte con paquetes, precios, fechas "
            "disponibles, promociones, capacidad y reservaciones."
        )

    # ----------------------------------------
    # SALUDO
    # ----------------------------------------

    def _responder_saludo(self):
        return (
            "¡Hola! Bienvenido a Salón Destellos. "
            "Soy EventBot, tu asistente virtual. "
            "Puedo ayudarte a consultar paquetes, precios, "
            "disponibilidad, promociones y reservaciones. "
            "¿En qué puedo ayudarte?"
        )

    # ----------------------------------------
    # COSTOS
    # ----------------------------------------

    def _responder_costos(self, entidades):

        nombre_paquete = entidades.get("paquete")
        invitados = entidades.get("invitados")

        if nombre_paquete:

            paquete = self.base.buscar_paquete(nombre_paquete)

            if paquete:
                servicios = ", ".join(paquete["servicios"])

                return (
                    f"El paquete {paquete['nombre']} tiene un costo "
                    f"de {self._formatear_precio(paquete['precio'])}. "
                    f"Tiene capacidad para hasta "
                    f"{paquete['capacidad_maxima']} invitados "
                    f"e incluye: {servicios}."
                )

        if invitados is not None:

            paquete = self.base.recomendar_paquete(invitados)

            if paquete:
                return (
                    f"Para un evento de {invitados} invitados, "
                    f"te recomendamos el paquete {paquete['nombre']}, "
                    f"con un costo de "
                    f"{self._formatear_precio(paquete['precio'])}. "
                    "El precio es de referencia y está sujeto "
                    "a confirmación."
                )

            return (
                f"No tenemos un paquete estándar para "
                f"{invitados} invitados. "
                "Nuestros paquetes están diseñados para eventos "
                "de entre 50 y 300 personas."
            )

        paquetes = self.base.obtener_paquetes()

        detalle = "; ".join(
            f"{p['nombre']}: {self._formatear_precio(p['precio'])}"
            for p in paquetes
        )

        return (
            f"Estos son nuestros paquetes y precios: {detalle}. "
            "¿Te interesa conocer los detalles de alguno?"
        )

    # ----------------------------------------
    # PAQUETES
    # ----------------------------------------

    def _responder_paquetes(self, entidades):

        nombre_paquete = entidades.get("paquete")
        invitados = entidades.get("invitados")

        if nombre_paquete:

            paquete = self.base.buscar_paquete(nombre_paquete)

            if paquete:

                servicios = ", ".join(paquete["servicios"])

                return (
                    f"El paquete {paquete['nombre']} incluye: "
                    f"{servicios}. "
                    f"Su precio es "
                    f"{self._formatear_precio(paquete['precio'])} "
                    f"y tiene capacidad para hasta "
                    f"{paquete['capacidad_maxima']} invitados."
                )

        if invitados is not None:

            paquete = self.base.recomendar_paquete(invitados)

            if paquete:

                return (
                    f"Para {invitados} invitados, "
                    f"te recomendamos el paquete "
                    f"{paquete['nombre']}, con capacidad "
                    f"para {paquete['capacidad_maxima']} personas "
                    f"y precio de "
                    f"{self._formatear_precio(paquete['precio'])}."
                )

            return (
                "No encontramos un paquete estándar para "
                f"{invitados} invitados. "
                "La capacidad contemplada es de 50 a 300 personas."
            )

        paquetes = self.base.obtener_paquetes()

        nombres = ", ".join(
            p["nombre"] for p in paquetes
        )

        return (
            f"En Salón Destellos ofrecemos cuatro paquetes: "
            f"{nombres}. "
            "¿De cuál te gustaría conocer los servicios?"
        )

    # ----------------------------------------
    # DISPONIBILIDAD
    # ----------------------------------------

    def _responder_disponibilidad(self, entidades):

        fecha = entidades.get("fecha")

        if not fecha:

            return (
                "Con gusto reviso la disponibilidad. "
                "¿Para qué fecha necesitas el salón? "
                "Puedes escribirla como 2026-11-15 "
                "o 15 de noviembre de 2026."
            )

        estado = self.base.consultar_disponibilidad(fecha)

        if estado == "disponible":
            return (
                f"Según nuestro calendario de demostración, "
                f"el {fecha} está disponible. "
                "Para reservarlo es necesario confirmar "
                "la fecha con un asesor."
            )

        elif estado == "ocupada":
            return (
                f"Lo sentimos, el {fecha} aparece como "
                "ocupado en nuestro calendario."
            )

        elif estado == "fecha_pasada":
            return (
                "La fecha indicada ya pasó. "
                "¿Te gustaría consultar una fecha futura?"
            )

        elif estado == "fecha_invalida":
            return (
                "No pude validar la fecha. "
                "Por favor utiliza el formato AAAA-MM-DD."
            )

        return (
            f"No tenemos información registrada para el {fecha}. "
            "Esto no significa que esté disponible. "
            "Es necesario confirmar con un asesor."
        )

    # ----------------------------------------
    # PROMOCIONES
    # ----------------------------------------

    def _responder_promociones(self):

        promociones = self.base.obtener_promociones()

        if not promociones:
            return (
                "Por el momento no tenemos promociones "
                "vigentes registradas."
            )

        detalle = "; ".join(
            f"{p['nombre']}: {p['descripcion']}"
            for p in promociones
        )

        return (
            f"Estas son nuestras promociones vigentes: "
            f"{detalle} "
            "La aplicación de descuentos está sujeta "
            "a las condiciones de cada promoción."
        )

    # ----------------------------------------
    # AMENIDADES
    # ----------------------------------------

    def _responder_amenidades(self):

        amenidades = self.base.obtener_amenidades()

        return (
            "Salón Destellos cuenta con las siguientes "
            "amenidades: " + ", ".join(amenidades) + "."
        )

    # ----------------------------------------
    # CAPACIDAD
    # ----------------------------------------

    def _responder_capacidad(self, entidades):

        informacion = self.base.obtener_informacion_salon()

        minimo = informacion["capacidad_minima"]
        maximo = informacion["capacidad_maxima"]

        invitados = entidades.get("invitados")

        if invitados is not None:

            if invitados > maximo:
                return (
                    f"Lo sentimos, no podemos recibir "
                    f"{invitados} invitados, ya que nuestra "
                    f"capacidad maxima es de {maximo} personas."
                )

            if invitados < minimo:
                return (
                    f"Nuestros eventos requieren un minimo "
                    f"de {minimo} invitados. "
                    "Te recomendamos consultar con un asesor."
                )

            return (
                f"Si, podemos recibir {invitados} invitados. "
                f"Nuestro salon tiene capacidad para "
                f"{minimo} a {maximo} personas."
            )

        return (
            f"Salon Destellos tiene capacidad para eventos "
            f"de {minimo} a {maximo} invitados."
        )

    # ----------------------------------------
    # UBICACIÓN
    # ----------------------------------------
    # UBICACIÓN
    # ----------------------------------------

    def _responder_ubicacion(self):

        informacion = self.base.obtener_informacion_salon()

        return (
            f"Salón Destellos se encuentra en "
            f"{informacion['ubicacion']}. "
            "Esta ubicación es simulada para el proyecto académico."
        )

    # ----------------------------------------
    # HORARIOS
    # ----------------------------------------

    def _responder_horarios(self):

        informacion = self.base.obtener_informacion_salon()

        return (
            "Nuestro horario de atención es: "
            f"{informacion['horario_atencion']}. "
            "La duración estándar de los eventos es de "
            f"{informacion['duracion_evento_horas']} horas."
        )

    # ----------------------------------------
    # RESERVACIONES
    # ----------------------------------------

    def _responder_reservacion(self):

        informacion = self.base.obtener_informacion_salon()

        return (
            "Para reservar en Salón Destellos: "
            f"{informacion['procedimiento_reservacion']} "
            "EventBot no realiza reservaciones ni pagos "
            "en esta versión."
        )

    # ----------------------------------------
    # TIPOS DE EVENTOS
    # ----------------------------------------

    def _responder_tipos_eventos(self):

        eventos = self.base.obtener_tipos_eventos()

        return (
            "En Salón Destellos organizamos eventos como: "
            + ", ".join(eventos)
            + ". ¿Qué tipo de evento estás planeando?"
        )
