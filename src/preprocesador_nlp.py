# ============================================
# EVENTBOT - PREPROCESADOR NLP
# AVANCE DE PROYECTO 2
# ============================================
import re
import unicodedata
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.snowball import SnowballStemmer
class PreprocesadorNLP:
    def __init__(self):
        self.stemmer = SnowballStemmer("spanish")
        # Lista personalizada de palabras vacias
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
    def normalizar(self, texto):
        if not isinstance(texto, str):
            raise TypeError("El texto debe ser una cadena.")
        texto = texto.lower().strip()
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(
            caracter
            for caracter in texto
            if unicodedata.category(caracter) != "Mn"
        )
        texto = re.sub(r"[^a-z0-9\s]", " ", texto)
        texto = re.sub(r"\s+", " ", texto).strip()
        return texto
    def tokenizar(self, texto):
        texto = self.normalizar(texto)
        return wordpunct_tokenize(texto)
    def eliminar_stopwords(self, tokens):
        return [
            token for token in tokens
            if token not in self.stopwords
        ]
    def aplicar_stemming(self, tokens):
        return [
            self.stemmer.stem(token)
            for token in tokens
        ]
    def procesar(self, texto):
        normalizado = self.normalizar(texto)
        tokens = self.tokenizar(texto)
        relevantes = self.eliminar_stopwords(tokens)
        raices = self.aplicar_stemming(relevantes)
        return {
            "texto_original": texto,
            "texto_normalizado": normalizado,
            "tokens": tokens,
            "tokens_relevantes": relevantes,
            "tokens_stemming": raices,
            "texto_procesado": " ".join(raices)
        }
