# ============================================
# EVENTBOT - CLASIFICADOR DE INTENCIONES
# AVANCE DE PROYECTO 2
# ============================================
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from src.preprocesador_nlp import PreprocesadorNLP
class ClasificadorIntenciones:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.preprocesador = PreprocesadorNLP()
        self.pipeline = Pipeline([
            (
                "preprocesamiento",
                FunctionTransformer(
                    self._preprocesar_textos,
                    validate=False
                )
            ),
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2)
                )
            ),
            (
                "clasificador",
                LinearSVC(
                    random_state=self.random_state,
                    max_iter=5000
                )
            )
        ])
    def _preprocesar_textos(self, textos):
        return [
            self.preprocesador.procesar(texto)[
                "texto_procesado"
            ]
            for texto in textos
        ]
    def entrenar(self, ruta_dataset):
        datos = pd.read_csv(ruta_dataset)
        X = datos["texto"]
        y = datos["intencion"]
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.30,
            random_state=self.random_state,
            stratify=y
        )
        self.pipeline.fit(X_train, y_train)
        predicciones = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, predicciones)
        reporte = classification_report(
            y_test,
            predicciones,
            zero_division=0,
            output_dict=True
        )
        etiquetas = sorted(y.unique())
        matriz = confusion_matrix(
            y_test,
            predicciones,
            labels=etiquetas
        )
        return {
            "accuracy": accuracy,
            "reporte": reporte,
            "matriz_confusion": matriz,
            "etiquetas": etiquetas,
            "X_test": X_test,
            "y_test": y_test,
            "predicciones": predicciones
        }
    def predecir(self, texto):
        return self.pipeline.predict([texto])[0]
    def guardar_modelo(self, ruta):
        joblib.dump(self.pipeline, ruta)
    def cargar_modelo(self, ruta):
        self.pipeline = joblib.load(ruta)
