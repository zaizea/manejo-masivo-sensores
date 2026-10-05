# Informe — Manejo Masivo de Datos

## Parte II. Aplicación al caso de Big Data

Los datos de `data/sensores_industriales.csv` son **simulados**. Una "alerta" es, en este ejercicio, una lectura con temperatura mayor que 85 °C (regla didáctica del examen).

### Resultados del análisis que se usan en este informe

Obtenidos con `analisis.py` sobre el CSV original:

| Resultado | Valor |
|---|---|
| Registros | 100,000 |
| Sensores distintos | 40 |
| Temperatura promedio por planta | Planta_1: 66.62 °C · Planta_2: 66.53 °C · Planta_3: 66.77 °C · Planta_4: 66.67 °C |
| Temperatura máxima | 104.99 °C, en 4 lecturas empatadas: S023 (01/09/26 22:23), S019 (02/09/26 13:11), S014 (02/09/26 15:23) y S030 (02/09/26 16:02) |
| Lecturas con alerta (> 85 °C) | 6,954 (6.95 % de las lecturas) |
| Planta con más alertas | Planta_3, con 1,777 alertas |

---

## 5. Las 5 V aplicadas al proyecto

| V | Cómo se relaciona con el sistema de sensores | Ejemplo concreto | ¿CSV actual o futura ampliación? |
|---|---|---|---|
| **Volumen** | Es la cantidad de datos que producen los sensores. Crece con el número de sensores y con la frecuencia de lectura. | El CSV tiene 100,000 registros de 40 sensores (unos 4.4 MiB). Si la empresa llegara, por ejemplo, a 5,000 sensores con una lectura por segundo, serían 432 millones de filas al día (unos 20 GB diarios con este mismo formato). | **CSV actual:** los 100,000 registros. **Futura ampliación:** los cientos de millones de filas al día (cifra estimada con un supuesto de 5,000 sensores). |
| **Velocidad** | Es qué tan rápido se generan los datos y qué tan rápido hay que reaccionar a ellos. | Según la descripción del caso, cada sensor registra una lectura por minuto. Con la ampliación serían lecturas cada segundo, y una temperatura mayor que 85 °C debería generar una alerta en pocos segundos. | **CSV actual:** la frecuencia de una lectura por minuto, pero el archivo ya está guardado y no llega en tiempo real. **Futura ampliación:** las lecturas cada segundo y las alertas casi inmediatas. |
| **Variedad** | Es la diversidad de tipos y formatos de los datos que se reciben. | El CSV solo trae datos tabulares: identificadores, fecha y hora, planta, temperatura y vibración. En la ampliación se sumarían mensajes JSON de los sensores, fotografías de las máquinas y reportes de mantenimiento en texto libre. | **CSV actual:** únicamente datos estructurados. **Futura ampliación:** JSON, fotografías y texto libre. |
| **Veracidad** | Es qué tan confiables y de qué calidad son los datos. Un sensor mal calibrado o con fallas produciría lecturas que no reflejan la máquina. | Los datos del CSV son simulados, así que no se puede asegurar que describan el estado real de ninguna máquina. Además, la temperatura máxima (104.99 °C) aparece en 4 lecturas de sensores distintos; con datos reales habría que verificar si son lecturas auténticas o un límite del sensor. El CSV no tiene una columna con el estado o la calibración del sensor. | **CSV actual:** la naturaleza simulada de los datos y las 4 coincidencias en el máximo. **Futura ampliación:** la validación de lecturas contra el estado real de sensores y máquinas. |
| **Valor** | Es la utilidad que se obtiene al analizar los datos para tomar decisiones. | Del análisis salen 6,954 alertas (6.95 % de las lecturas) y se ve que Planta_3 acumula más (1,777), lo que sirve para decidir dónde revisar primero. Con la ampliación el valor sería anticipar fallas y evitar paros. | **CSV actual:** los hallazgos del análisis (alertas y planta con más alertas). **Futura ampliación:** la predicción de fallas con fotos y reportes. |

---

## 6. Tipos de datos y procesamiento tradicional

### Clasificación

| Elemento | Tipo | Por qué |
|---|---|---|
| El CSV de sensores | **Estructurado** | Está organizado en filas y columnas fijas, con un esquema definido (`id_registro`, `fecha_hora`, `id_sensor`, `planta`, `temperatura_c`, `vibracion_mm_s`). |
| Un mensaje JSON enviado por un sensor | **Semiestructurado** | Tiene etiquetas y pares clave-valor que le dan cierta organización, pero no sigue una tabla rígida y sus campos pueden variar entre mensajes. |
| Una fotografía de una máquina | **No estructurado** | Es una imagen (píxeles) sin campos ni esquema; para extraer información hay que procesarla con técnicas de visión por computadora. |
| El texto libre de un reporte de mantenimiento | **No estructurado** | Es lenguaje natural sin formato fijo; para analizarlo se necesitaría procesamiento de texto. |

### ¿Por qué 100,000 registros no convierten automáticamente al archivo en Big Data?

Big Data no depende solo de la cantidad de filas. Se habla de Big Data cuando el volumen, la velocidad y la variedad de los datos superan lo que un sistema tradicional puede manejar con comodidad. Este archivo no cumple eso:

- Pesa unos 4.4 MiB y cabe sin problema en la memoria de una computadora personal.
- Mi programa lo leyó y lo analizó completo en pocos segundos, con una sola herramienta (Python con pandas) y en un solo equipo.
- Es un archivo estático, con un solo formato (tabular) y sin llegada continua de datos.

### Limitaciones al aumentar la escala

- **Memoria:** pandas carga todo el CSV en la RAM; con cientos de millones de filas no cabría.
- **Tiempo de procesamiento:** leer y recorrer un archivo gigantesco en un solo equipo tardaría mucho.
- **Almacenamiento:** con el supuesto de 5,000 sensores y una lectura por segundo, serían unos 20 GB diarios (más de 7 TB al año), sin contar fotografías y reportes.
- **Un solo equipo:** no se puede repartir el trabajo entre varias máquinas ni hay tolerancia a fallos si el equipo se cae.
- **Formato:** un CSV no guarda fotografías ni texto libre, no valida los datos y no tiene índices para consultar rápido.
- **Tiempo real:** un programa que lee un archivo ya guardado no puede avisar de una alerta cuando ocurre.

---

## 7. Batch y Streaming

### Procesamiento que realicé

Realicé **procesamiento por lotes (batch)**. `analisis.py` toma un archivo que ya existe y tiene un tamaño finito, lo procesa completo en una sola ejecución y entrega los resultados hasta el final. Se justifica porque no hacía falta responder en el momento en que se generó cada lectura: se analizó un historial ya guardado.

### Alerta pocos segundos después de recibir una lectura mayor que 85 °C

Usaría **streaming (procesamiento de flujo)**. Cada lectura se procesa como un evento en cuanto llega: se evalúa la regla `temperatura_c > 85` y, si se cumple, se emite la alerta de inmediato. Una arquitectura posible sería sensores que envían eventos a un sistema de mensajería (por ejemplo, Apache Kafka) y un procesador de flujo (por ejemplo, Spark Structured Streaming o Apache Flink) que aplica la regla y manda la notificación.

### Resumen al terminar el día

Usaría **batch**. Al cierre del día se procesan, en una tarea programada, todas las lecturas ya almacenadas para calcular promedios, máximos y conteo de alertas por planta. No hace falta el resultado al instante, y procesar el conjunto completo es más sencillo y barato.

### Relación con el tiempo en que se necesita cada resultado

| Necesidad | Enfoque | Cuándo se necesita el resultado |
|---|---|---|
| Alerta por temperatura mayor que 85 °C | Streaming | En pocos segundos |
| Resumen diario | Batch | Al terminar el día |
| Análisis del archivo `sensores_industriales.csv` (este trabajo) | Batch | Cuando termine la ejecución |

Mientras más pronto se necesita el resultado, más conviene procesar cada dato al llegar (streaming). Cuando se puede esperar, conviene acumular los datos y procesarlos juntos (batch).

---

## 8. Lambda y Kappa

### Escenario A: arquitectura Lambda

La empresa quiere combinar una ruta que recalcule el historial por lotes con otra que procese las mediciones recientes rápidamente. Eso es justo lo que hace **Lambda**: tiene una *capa batch* que recalcula todo el historial, una *capa speed* que procesa los datos recientes con baja latencia y una *capa de servicio* que une ambos resultados para consultarlos. Tiene dos rutas con lógica separada, lo que da respuestas rápidas y también cálculos completos y precisos del historial, a cambio de mantener dos códigos.

```
                  ┌──────────┐
                  │ Sensores │
                  └─────┬────┘
                        │ lecturas
          ┌─────────────┴────────────┐
          ▼                          ▼
┌────────────────────┐     ┌────────────────────┐
│ Capa batch         │     │ Capa speed         │
│ historial completo,│     │ lecturas recientes,│
│ se recalcula por   │     │ se procesan        │
│ lotes              │     │ rápidamente        │
└─────────┬──────────┘     └─────────┬──────────┘
          │ vistas batch             │ vistas rápidas
          └─────────────┬────────────┘
                        ▼
           ┌─────────────────────────┐
           │ Capa de servicio        │
           │ (une los resultados     │
           │ batch y speed)          │
           └────────────┬────────────┘
                        ▼
             ┌─────────────────────┐
             │ Consultas y alertas │
             └─────────────────────┘
```

### Escenario B: arquitectura Kappa

La empresa quiere una sola lógica de procesamiento de eventos y conservar las mediciones para volver a procesarlas cuando sea necesario. Eso corresponde a **Kappa**: todo se trata como un flujo de eventos, que se guardan en un registro (log) inmutable. Hay una única lógica de procesamiento, y si cambia, se vuelve a leer el log desde el inicio. Evita duplicar código, pero depende de conservar el log de eventos.

```
              ┌──────────┐
              │ Sensores │
              └─────┬────┘
                    │ eventos
                    ▼
     ┌─────────────────────────────┐
     │ Registro de eventos         │
     │ (log inmutable: se guardan  │
     │ todas las lecturas)         │
     └──────────────┬──────────────┘
                    │ se lee en orden
                    ▼
     ┌─────────────────────────────┐
     │ Procesamiento de flujo      │
     │ (una sola lógica para       │
     │ tiempo real e histórico)    │
     └──────────────┬──────────────┘
                    │
                    ▼
     ┌─────────────────────────────┐
     │ Resultados                  │
     │ (alertas y resúmenes)       │
     └─────────────────────────────┘
```

Si la lógica de procesamiento cambia, se despliega la nueva versión y se vuelve a leer el log desde el inicio para recalcular los resultados.

---

## 9. Analítica descriptiva, predictiva y prescriptiva

### Descriptiva (qué pasó)

Dos hallazgos reales de mi análisis:

1. **Alertas por planta:** hay 6,954 lecturas con temperatura mayor que 85 °C (6.95 % de las 100,000), y la planta con más alertas es **Planta_3**, con 1,777 (cerca de una cuarta parte del total de alertas). Las diferencias entre plantas son pequeñas: por ejemplo, el promedio de temperatura va de 66.53 °C (Planta_2) a 66.77 °C (Planta_3).
2. **Temperatura máxima:** el valor más alto es **104.99 °C**, registrado en 4 lecturas empatadas, de los sensores S023 (01/09/26 22:23), S019 (02/09/26 13:11), S014 (02/09/26 15:23) y S030 (02/09/26 16:02).

### Predictiva (qué podría pasar)

**Pregunta:** ¿qué máquinas tienen más probabilidad de sobrecalentarse o fallar en las próximas 24 horas?

Para investigarla necesitaría datos adicionales que el CSV no tiene:
- El historial de fallas y paros (fecha, máquina y tipo de falla), para saber qué pasó realmente después de cada alerta.
- La relación entre cada `id_sensor` y la máquina que monitorea (el CSV solo indica sensor y planta).
- Los reportes de mantenimiento, y la edad y el modelo de cada máquina.
- Las condiciones de operación, como la carga de trabajo y la temperatura ambiente.

Una lectura por encima del umbral indica una alerta del ejercicio; por sí sola no demuestra que una máquina vaya a fallar.

### Prescriptiva (qué hacer)

**Acción propuesta:** si el modelo predictivo señalara un riesgo alto de sobrecalentamiento en las máquinas de una planta (por ejemplo, Planta_3, la que más alertas acumula), la empresa podría **programar una inspección preventiva** de esas máquinas antes de que fallen.

Antes de decidir, revisaría:
- Si las alertas son picos aislados o lecturas altas sostenidas en el tiempo.
- Si coinciden con aumentos en la vibración del mismo sensor.
- Que el sensor esté calibrado y funcionando bien (veracidad del dato).
- El historial de mantenimiento de la máquina.
- El costo de detener la producción frente al riesgo de una falla.
