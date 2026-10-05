from pathlib import Path

import pandas as pd

RUTA_CSV = Path("data") / "sensores_industriales.csv"
RUTA_ALERTAS = Path("resultados") / "alertas.csv"
UMBRAL_ALERTA = 85  # °C, regla didáctica del examen


def main():
    # fecha_hora se deja como texto para conservar el formato original al exportar
    df = pd.read_csv(RUTA_CSV)

    # 1. Cantidad de registros y sensores distintos
    print(f"Registros: {len(df)}")
    print(f"Sensores distintos: {df['id_sensor'].nunique()}")

    # 2. Temperatura promedio por planta
    print("\nTemperatura promedio por planta (°C):")
    print(df.groupby("planta")["temperatura_c"].mean().round(2))

    # 3. Temperatura máxima, sensor y fecha (se muestran todos los empates)
    temp_max = df["temperatura_c"].max()
    filas_max = df[df["temperatura_c"] == temp_max]
    print(f"\nTemperatura máxima: {temp_max} °C ({len(filas_max)} lectura(s))")
    for _, fila in filas_max.iterrows():
        print(f"  Sensor: {fila['id_sensor']} | Fecha y hora: {fila['fecha_hora']}")

    # 4. Lecturas con temperatura mayor que 85 °C
    alertas = df[df["temperatura_c"] > UMBRAL_ALERTA]
    print(f"\nLecturas con alerta (> {UMBRAL_ALERTA} °C): {len(alertas)}")

    # 5. Planta con más alertas
    if alertas.empty:
        print("No hay alertas, así que no hay planta con más alertas.")
    else:
        conteo = alertas["planta"].value_counts()
        maximo = conteo.max()
        # si hay empate, se muestran todas las plantas empatadas
        for planta in conteo[conteo == maximo].index:
            print(f"Planta con más alertas: {planta} ({maximo} alertas)")

    # 6. Exportar alertas con las columnas originales
    RUTA_ALERTAS.parent.mkdir(exist_ok=True)
    alertas.to_csv(RUTA_ALERTAS, index=False)
    print(f"\nAlertas exportadas a {RUTA_ALERTAS}")


if __name__ == "__main__":
    main()
