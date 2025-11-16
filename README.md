# Git_pildoras

## Tracking electoral en Python

Este repositorio incluye un ejemplo de seguimiento electoral escrito en
Python utilizando `pandas`, `matplotlib` y `seaborn`. El objetivo es
mostrar cómo limpiar los datos de una encuesta, aplicar una **función de
ventana** para suavizar la intención de voto de un candidato y
visualizar los resultados.

### Requisitos

- Python 3.10+
- pandas
- matplotlib
- seaborn

Instalar dependencias:

```bash
pip install pandas matplotlib seaborn
```

### Estructura de datos

El archivo `data/encuestas.csv` contiene una muestra con las siguientes
columnas (todas las observaciones fueron estratificadas como **bajo**,
**medio** o **alto** de acuerdo con la cobertura de la canasta básica
total del hogar):

- Fecha
- Encuesta
- Estrato
- Sexo
- Edad
- Nivel Educativo
- Cantidad de Integrantes en el Hogar
- Imagen del Candidato
- Voto
- Voto Anterior
  - Los valores de voto siguen el formato `Candidato A`, `Candidato B`,
    `Candidato C`, etc.

### Ejecución

```bash
python tracking_electoral.py
```

La ejecución imprime en consola:

1. Indicadores sociodemográficos (imagen promedio e intención de voto por
   fecha, sexo y rango etario).
2. Serie temporal de intención de voto suavizada mediante una ventana
   móvil configurable.
3. La ruta del gráfico exportado automáticamente (por defecto en
   `output/tracking.png`).
