
# ============================================
# EVENTBOT - PROCESADOR DE TEXTO
# Salón Destellos
# ============================================

import re
import unicodedata

from nltk.tokenize import wordpunct_tokenize


class ProcesadorTexto:
    """
    Procesa las consultas escritas por los clientes.

    Utiliza NLTK para tokenización y técnicas
    básicas de normalización de texto.
    """

    def __init__(self):

        # Palabras frecuentes que no suelen aportar
        # información para identificar una intención.
        self.stopwords = {
            "el", "la", "los", "las",
            "un", "una", "unos", "unas",
            "de", "del", "al", "en",
            "por", "para", "con",
            "me", "te", "se", "le",
            "mi", "tu", "su",
            "que", "como", "cual",
            "es", "son", "ser",
            "puedes", "podrias",
            "favor", "quiero", "quisiera"
        }

    # ----------------------------------------
    # NORMALIZAR TEXTO
    # ----------------------------------------

    def normalizar(self, texto):
        """
        Convierte a minúsculas, elimina acentos
        y normaliza espacios.
        """

        if not isinstance(texto, str):
            raise TypeError("El texto debe ser una cadena.")

        texto = texto.lower().strip()

        # Separar caracteres acentuados
        texto = unicodedata.normalize("NFD", texto)

        # Eliminar marcas de acentuación
        texto = "".join(
            caracter
            for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )

        # Eliminar signos de puntuación
        # Conservamos números para fechas y cantidades.
        texto = re.sub(r"[^a-z0-9\s]", " ", texto)

        # Eliminar espacios adicionales
        texto = re.sub(r"\s+", " ", texto).strip()

        return texto

    # ----------------------------------------
    # TOKENIZACIÓN
    # ----------------------------------------

    def tokenizar(self, texto):
        """
        Divide el texto normalizado en palabras
        utilizando NLTK.
        """

        texto_normalizado = self.normalizar(texto)

        tokens = wordpunct_tokenize(texto_normalizado)

        return tokens

    # ----------------------------------------
    # ELIMINAR PALABRAS VACÍAS
    # ----------------------------------------

    def eliminar_stopwords(self, tokens):
        """
        Elimina palabras frecuentes de una lista
        de tokens.
        """

        return [
            token
            for token in tokens
            if token not in self.stopwords
        ]

    # ----------------------------------------
    # PROCESAR CONSULTA
    # ----------------------------------------

    def procesar(self, texto):
        """
        Ejecuta el procesamiento completo
        de una consulta.
        """

        texto_normalizado = self.normalizar(texto)

        tokens = self.tokenizar(texto)

        tokens_relevantes = self.eliminar_stopwords(tokens)

        return {
            "texto_original": texto,
            "texto_normalizado": texto_normalizado,
            "tokens": tokens,
            "tokens_relevantes": tokens_relevantes
        }
