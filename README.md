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
- No interpreta el contexto de mensajes anteriores.
- Los datos comerciales son simulados.
- No realiza reservaciones ni pagos reales.
- No procesa imágenes.
- No cuenta con integración web en tiempo real.

## Mejoras futuras

- Clasificación de intenciones mediante modelos NLP.
- Memoria conversacional.
- Integración con calendarios y APIs.
- Clasificación de imágenes de decoración.
- Interfaz web para clientes.

## Consideraciones

Este proyecto tiene fines exclusivamente académicos.
Salón Destellos y sus datos son ficticios.
```
