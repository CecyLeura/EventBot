# EventBot – Salón Destellos

## Descripción

EventBot es un prototipo de chatbot desarrollado en Python
para apoyar la atención y cotización de eventos sociales
del Salón Destellos, un negocio ficticio ubicado en Monterrey,
Nuevo León, México.

El asistente permite consultar paquetes, precios,
disponibilidad de fechas, promociones, capacidad,
amenidades y procedimientos de reservación.

## Objetivo

Desarrollar un asistente conversacional modular basado
en reglas que permita automatizar respuestas a consultas
frecuentes de clientes interesados en eventos sociales.

## Tecnologías utilizadas

- Python 3.10 o superior
- NLTK
- Google Colab
- JSON
- Pandas y Matplotlib para evaluación y visualización
- Programación orientada a objetos

## Arquitectura

El proyecto incluye los siguientes módulos:

- `configuracion.py`: configuración y rutas.
- `base_conocimiento.py`: acceso a datos JSON.
- `procesador_texto.py`: normalización y tokenización.
- `detector_intenciones.py`: identificación de intenciones.
- `gestor_conversacion.py`: generación de respuestas.
- `eventbot.py`: integración y ejecución del chatbot.

## Funcionalidades

1. Consultar paquetes y precios.
2. Recomendar paquetes según invitados.
3. Consultar disponibilidad simulada.
4. Informar promociones.
5. Consultar capacidad y amenidades.
6. Informar ubicación y horarios.
7. Explicar el procedimiento de reservación.
8. Registrar conversaciones.

## Instalación

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución en Google Colab

Abrir el notebook `notebooks/EventBot_Colab.ipynb`
y ejecutar sus celdas en orden.

Para iniciar el chatbot desde Python:

```python
from src.eventbot import EventBot

bot = EventBot("/content/EventBot")
bot.conversar()
```

## Pruebas funcionales

Se realizaron 10 conversaciones de prueba con
50 consultas en total.

Resultados:
- Consultas evaluadas: 50.
- Intenciones correctas: 50.
- Exactitud de clasificación: 100%.

Este resultado corresponde únicamente al conjunto
de pruebas definido para el prototipo.

## Limitaciones

- El chatbot utiliza reglas predefinidas.
- Conserva el paquete mencionado durante la sesión, pero su memoria conversacional es limitada.
- Los datos comerciales son simulados.
- No realiza reservaciones ni pagos reales.
- Procesa imágenes mediante un método Python, pero todavía no dispone de carga directa desde una interfaz.
- No cuenta con integración web en tiempo real.

## Mejoras futuras

- Mejorar e integrar progresivamente el clasificador NLP entrenado en el flujo conversacional.
- Ampliar la memoria conversacional y el manejo del contexto.
- Integración con calendarios y APIs.
- Mejorar la clasificación visual con más datos y etiquetas verificadas.
- Interfaz web para clientes.

## Consideraciones

Este proyecto tiene fines exclusivamente académicos.
Salón Destellos y sus datos son ficticios.
```

---

## Ampliación del proyecto - Avance 2

### Problema y objetivo

Los clientes de Salón Destellos necesitan consultar información
sobre eventos sociales de manera rápida y sencilla.

En el Avance 2 se amplía el prototipo conversacional con
componentes de inteligencia artificial para clasificar
intenciones textuales y fotografías de eventos.

El objetivo es desarrollar y evaluar estos componentes,
manteniendo una arquitectura modular que permita
su integración con el chatbot.

### Usuarios

- Clientes interesados en paquetes, precios y reservaciones.
- Personal del salón encargado de atender consultas.
- Administradores que podrían utilizar las clasificaciones
  para apoyar la organización de información sobre eventos.

### Alcance

El sistema permite:

1. Responder preguntas frecuentes mediante el chatbot.
2. Mantener un contexto conversacional básico.
3. Clasificar intenciones con un modelo NLP experimental.
4. Clasificar fotografías de bodas, XV años y
   eventos corporativos.
5. Comunicar los resultados visuales en lenguaje natural.
6. Registrar consultas textuales y visuales en el historial.

Los datos comerciales son simulados y el sistema
no realiza reservaciones ni pagos reales.

### Arquitectura del Avance 2

**Componente conversacional:**

- `src/eventbot.py`: coordinación del chatbot e integración visual.
- `src/detector_intenciones.py`: detección de intenciones
  en el flujo conversacional existente.
- `src/gestor_conversacion.py`: generación de respuestas.
- `src/base_conocimiento.py`: información del salón.

**Componente NLP:**

- `src/preprocesador_nlp.py`: normalización, tokenización,
  eliminación de stopwords y stemming.
- `src/clasificador_intenciones.py`: representación TF-IDF
  y clasificación mediante LinearSVC.

El clasificador NLP se desarrolló y evaluó como
componente experimental. La conversación principal
conserva su detector de intenciones basado en reglas.

**Componente visual:**

- `src/clasificador_imagenes.py`: carga del modelo CNN,
  preparación de imágenes y generación de predicciones.
- EfficientNetB0 con transferencia de aprendizaje
  y pesos preentrenados de ImageNet.

El método `EventBot.responder_imagen()` permite utilizar
el clasificador visual y registrar su resultado
en el historial de la sesión.

### Resultados de evaluación

| Métrica | NLP | CNN |
|---|---:|---:|
| Accuracy | 79.49 % | 66.67 % |
| Precision macro | 78.97 % | 69.05 % |
| Recall macro | 79.49 % | 66.67 % |
| F1-score macro | 76.90 % | 66.67 % |

El clasificador NLP se evaluó con 39 consultas.
El clasificador CNN se evaluó con 15 fotografías de prueba.

Las métricas corresponden a tareas diferentes
y no representan una comparación directa
entre técnicas de aprendizaje.

### Limitaciones del Avance 2

- Los conjuntos de entrenamiento y evaluación son reducidos.
- El modelo NLP presenta dificultades con algunas intenciones,
  especialmente las relacionadas con costos.
- La CNN puede confundir eventos con decoraciones similares.
- El fine-tuning no mejoró las métricas de clasificación
  observadas en validación.
- La clasificación visual es orientativa.
- La integración visual recibe una ruta de archivo;
  todavía no incluye una interfaz gráfica para subir imágenes.

### Archivos y evidencias

- `EventBot_Avance2.ipynb`: notebook de desarrollo.
- `resultados/avance2/`: resultados del componente NLP.
- `resultados/avance2/cnn/`: métricas, matriz de confusión
  y evidencias de integración.

Las fotografías y los modelos entrenados se conservan
fuera del repositorio, en Google Drive.

### Mejoras para la versión final

1. Ampliar y diversificar los datasets.
2. Mejorar la clasificación de intenciones problemáticas.
3. Revisar las etiquetas de fotografías ambiguas.
4. Incorporar una interfaz para cargar imágenes.
5. Fortalecer la integración entre el clasificador NLP
   y la lógica conversacional.
6. Evaluar el sistema con nuevos datos independientes.
