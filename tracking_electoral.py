"""Herramientas para realizar un tracking electoral con pandas.

El módulo carga una tabla de encuestas, limpia los datos, calcula
indicadores sociodemográficos básicos y aplica una función de ventana
para suavizar la intención de voto del candidato.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATA_COLUMNS = {
    "Fecha": "datetime64[ns]",
    "Encuesta": "string",
    "Estrato": "string",
    "Sexo": "category",
    "Edad": "Int64",
    "Nivel Educativo": "category",
    "Cantidad de Integrantes en el Hogar": "Int64",
    "Imagen del Candidato": "Float64",
    "Voto": "category",
    "Voto Anterior": "category",
}


@dataclass
class TrackingConfig:
    """Configuración reutilizable para el tracking electoral."""

    ventana: int = 3
    tipo_resumen: Literal["mean", "median"] = "mean"
    columna_objetivo: str = "IntencionVoto"
    candidato_objetivo: str = "Candidato A"
    ruta_grafico: Path | None = Path("output/tracking.png")


def cargar_datos(ruta_csv: str | Path) -> pd.DataFrame:
    """Carga el CSV asegurando los tipos de datos y ordenando por fecha."""

    df = pd.read_csv(ruta_csv, parse_dates=["Fecha"])
    for columna, dtype in DATA_COLUMNS.items():
        if columna in df.columns:
            df[columna] = df[columna].astype(dtype)
    return df.sort_values("Fecha").reset_index(drop=True)


def limpiar_datos(
    df: pd.DataFrame, *, candidato_objetivo: str = "Candidato A"
) -> pd.DataFrame:
    """Aplica reglas básicas de limpieza sobre el dataframe original."""

    df = df.drop_duplicates(subset=["Encuesta", "Estrato", "Sexo", "Edad"])

    # Eliminamos registros con información crítica faltante
    columnas_obligatorias = [
        "Fecha",
        "Imagen del Candidato",
        "Voto",
        "Voto Anterior",
    ]
    df = df.dropna(subset=columnas_obligatorias)

    # Normalizamos estratos a bajo/medio/alto (clasificación según canasta básica)
    estratos_validos = {"bajo": "Bajo", "medio": "Medio", "alto": "Alto"}
    df["Estrato"] = (
        df["Estrato"].astype(str).str.strip().str.lower().map(estratos_validos)
    )
    df = df.dropna(subset=["Estrato"])
    df["Estrato"] = pd.Categorical(
        df["Estrato"], categories=list(estratos_validos.values()), ordered=True
    )

    # Armonizamos valores de voto
    df["Voto"] = df["Voto"].astype(str).str.strip().str.title()
    df["Voto Anterior"] = df["Voto Anterior"].astype(str).str.strip().str.title()
    df["Voto"] = pd.Categorical(df["Voto"])
    df["Voto Anterior"] = pd.Categorical(df["Voto Anterior"])

    # Creamos variables derivadas normalizadas
    df["Imagen Normalizada"] = df["Imagen del Candidato"].clip(0, 100) / 100

    # Intención de voto binaria por el candidato objetivo
    df["IntencionVoto"] = (df["Voto"] == candidato_objetivo.title()).astype(int)

    # Edad agrupada en rangos metodológicos habituales
    df["Edad Rango"] = pd.cut(
        df["Edad"], bins=[17, 29, 44, 59, 120], labels=["18-29", "30-44", "45-59", "60+"]
    )

    return df


def indicadores_sociodemograficos(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula indicadores agregados por sexo y rango etario."""

    resumen = (
        df.groupby(["Fecha", "Sexo", "Edad Rango"], observed=True)
        .agg(
            n=("Encuesta", "count"),
            imagen_media=("Imagen del Candidato", "mean"),
            intencion_media=("IntencionVoto", "mean"),
        )
        .reset_index()
    )
    return resumen


def aplicar_funcion_ventana(
    df: pd.DataFrame,
    columna: str,
    ventana: int,
    funcion: Literal["mean", "median", "sum"] = "mean",
) -> pd.Series:
    """Aplica una función de ventana (rolling window) sobre una columna."""

    if ventana <= 0:
        raise ValueError("La ventana debe ser un entero positivo")

    rolling = df[columna].rolling(window=ventana, min_periods=1)
    if funcion == "mean":
        return rolling.mean()
    if funcion == "median":
        return rolling.median()
    if funcion == "sum":
        return rolling.sum()
    raise ValueError("Función de ventana no soportada")


def tracking_electoral(df: pd.DataFrame, config: TrackingConfig) -> pd.DataFrame:
    """Devuelve una serie temporal suavizada de la intención de voto."""

    serie_diaria = (
        df.groupby("Fecha")
        .agg(
            IntencionVoto=("IntencionVoto", "mean"),
            ImagenMedia=("Imagen Normalizada", "mean"),
        )
        .reset_index()
    )

    serie_diaria["TrackingSuavizado"] = aplicar_funcion_ventana(
        serie_diaria,
        config.columna_objetivo,
        ventana=config.ventana,
        funcion=config.tipo_resumen,
    )
    return serie_diaria


def graficar_tracking(tracking: pd.DataFrame, config: TrackingConfig) -> None:
    """Genera un gráfico de la serie diaria y su versión suavizada."""

    if config.ruta_grafico is None:
        return

    ruta = Path(config.ruta_grafico)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 5))
    sns.lineplot(
        data=tracking,
        x="Fecha",
        y="IntencionVoto",
        label="Media diaria",
        marker="o",
    )
    sns.lineplot(
        data=tracking,
        x="Fecha",
        y="TrackingSuavizado",
        label=f"Ventana {config.ventana}",
        linewidth=2.5,
    )
    plt.ylabel(f"Intención de voto {config.candidato_objetivo}")
    plt.xlabel("Fecha")
    plt.title("Tracking electoral (media diaria vs. ventana)")
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()
    print(f"Gráfico guardado en {ruta}")


def ejecutar_tracking(ruta_csv: str | Path, config: TrackingConfig) -> None:
    """Pipeline completo de carga, limpieza, reporte y visualización."""

    df = cargar_datos(ruta_csv)
    df = limpiar_datos(df, candidato_objetivo=config.candidato_objetivo)

    print("\n=== Indicadores sociodemográficos ===")
    indicadores = indicadores_sociodemograficos(df)
    print(indicadores.head())

    print("\n=== Tracking suavizado ===")
    tracking = tracking_electoral(df, config)
    print(tracking)
    graficar_tracking(tracking, config)


if __name__ == "__main__":
    ruta = Path("data/encuestas.csv")
    cfg = TrackingConfig(ventana=3, tipo_resumen="mean")
    if ruta.exists():
        ejecutar_tracking(ruta, cfg)
    else:
        raise SystemExit("No se encontró el archivo data/encuestas.csv")
