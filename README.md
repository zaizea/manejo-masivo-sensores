# Análisis de sensores industriales

## Objetivo

Analizar con Python las mediciones de temperatura y vibración de sensores instalados en cuatro plantas industriales: calcular estadísticas por planta, encontrar la temperatura máxima y detectar alertas de temperatura (lecturas mayores a 85 °C), exportando las alertas a un archivo CSV.

> **Nota:** los datos de `data/sensores_industriales.csv` son **simulados**. No corresponden a mediciones reales.

## Descripción de los datos

El archivo `data/sensores_industriales.csv` contiene 100,000 mediciones (una lectura por minuto por sensor).

| Columna | Significado |
|---|---|
| `id_registro` | Identificador de la medición |
| `fecha_hora` | Fecha y hora de la lectura |
| `id_sensor` | Identificador del sensor |
| `planta` | Planta donde está instalado |
| `temperatura_c` | Temperatura en grados Celsius |
| `vibracion_mm_s` | Vibración en milímetros por segundo |

Regla de alerta (criterio didáctico del examen): una lectura es **alerta de temperatura** cuando `temperatura_c` > 85 °C.

## Estructura del proyecto

```
.
├── analisis.py          # programa de análisis
├── requirements.txt     # dependencias con versiones
├── data/
│   └── sensores_industriales.csv
└── resultados/
    └── alertas.csv      # se genera al ejecutar el programa
```

## Instalación

Requiere Python 3.10 o superior y Git.

```bash
git clone https://github.com/zaizea/manejo-masivo-sensores.git
cd manejo-masivo-sensores
python -m venv .venv
```

Activar el entorno virtual:

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- Windows (CMD): `.venv\Scripts\activate.bat`
- macOS / Linux: `source .venv/bin/activate`

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:

```bash
python analisis.py
```

El programa imprime en pantalla:

1. Cantidad de registros y de sensores distintos.
2. Temperatura promedio de cada planta.
3. Temperatura máxima, con el sensor y la fecha (si hay empates, se muestran todos).
4. Cantidad de lecturas con temperatura mayor a 85 °C.
5. Planta con más alertas (si hay empates, se muestran todas).

Además, exporta todas las lecturas con alerta, con sus columnas originales, a `resultados/alertas.csv`.
