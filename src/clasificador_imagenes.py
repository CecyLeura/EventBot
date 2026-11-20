
from pathlib import Path
import numpy as np
import tensorflow as tf


class ClasificadorImagenes:
    """Clasifica imágenes de eventos utilizando EfficientNetB0."""

    CLASES = ["boda", "corporativo", "xv_anos"]

    def __init__(self, ruta_modelo):
        self.ruta_modelo = Path(ruta_modelo)

        if not self.ruta_modelo.is_file():
            raise FileNotFoundError(
                f"No se encontró el modelo CNN: {self.ruta_modelo}"
            )

        self.modelo = tf.keras.models.load_model(
            self.ruta_modelo
        )

    def preparar_imagen(self, ruta_imagen):
        """Prepara una fotografía para el modelo CNN."""

        ruta = Path(ruta_imagen)

        if not ruta.is_file():
            raise FileNotFoundError(
                f"No se encontró la imagen: {ruta}"
            )

        imagen = tf.keras.utils.load_img(
            ruta,
            target_size=(224, 224),
            color_mode="rgb"
        )

        arreglo = tf.keras.utils.img_to_array(imagen)

        return np.expand_dims(arreglo, axis=0)

    def clasificar(self, ruta_imagen):
        """Devuelve la categoría y probabilidades estimadas."""

        entrada = self.preparar_imagen(ruta_imagen)

        probabilidades = self.modelo.predict(
            entrada,
            verbose=0
        )[0]

        indice = int(np.argmax(probabilidades))
        categoria = self.CLASES[indice]
        confianza = float(probabilidades[indice])

        return {
            "categoria": categoria,
            "confianza": round(confianza, 4),
            "probabilidades": {
                clase: round(float(probabilidad), 4)
                for clase, probabilidad in zip(
                    self.CLASES,
                    probabilidades
                )
            }
        }
