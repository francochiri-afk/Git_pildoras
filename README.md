# Git_pildoras

## Tracking electoral en Python (notebook)

Este repositorio incluye un notebook (`tracking_electoral.ipynb`) para
seguir la evolución de la intención de voto y la imagen de un candidato
en Argentina. El flujo:

1. Carga múltiples CSV de encuestas (uno por mes) para simular el paso
   del tiempo.
2. Limpia y normaliza las variables clave (`Estrato` como bajo/medio/
   alto, `Voto` con el formato `Candidato A/B/C` y sexos homogéneos).
3. Pondera la muestra con una distribución simplificada basada en el
   Censo 2022 (sexo x grupo etario x estrato socioeconómico derivado de
   la canasta básica total).
4. Aplica una ventana móvil para suavizar series y genera gráficos de
   la imagen de *Candidato A* y de la intención de voto de tres
   candidatos.

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

En `data/` encontrarás varios archivos de ejemplo (`encuestas_2024-01.csv`,
`encuestas_2024-02.csv`, `encuestas_2024-03.csv`) con las siguientes
columnas estratificadas (bajo/medio/alto en función de la canasta básica):

- Fecha
- Encuesta
- Estrato
- Sexo
- Edad
- Nivel Educativo
- Cantidad de Integrantes en el Hogar
- Imagen del Candidato
- Voto (ejemplo: `Candidato A`, `Candidato B`, `Candidato C`)
- Voto Anterior

Puedes agregar nuevos archivos siguiendo el patrón `encuestas_YYYY-MM.csv`
para extender la serie temporal.

### Ejecución en VSCode

1. Abre `tracking_electoral.ipynb` en VSCode.
2. Selecciona un kernel de Python 3.10+ con las dependencias instaladas.
3. Ejecuta las celdas en orden. Se generarán las imágenes
   `outputs/imagen_candidato.png` e `outputs/intencion_voto.png` con la
   evolución ponderada y suavizada de la serie.
