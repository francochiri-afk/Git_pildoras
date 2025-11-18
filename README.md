# Git_pildoras

## Tracking electoral con ponderación censal 2022

Este repositorio incluye un notebook (`tracking_electoral.ipynb`) que sigue la evolución de la imagen y la intención de voto de candidatos presidenciales en Argentina. El flujo ahora está alineado con los datos del Censo 2022 y con estratificación por provincias.

### Flujo
1. Carga múltiples CSV de encuestas (`data/encuestas_YYYY-MM.csv`) para simular distintas olas temporales.
2. Limpia y normaliza los campos clave:
   - `Estrato` se interpreta como provincia (códigos oficiales 01-24). Se corrigen nombres parciales como `cord` → `CORDOBA`.
   - `Sexo` acepta prefijos como `fe` o `mu` para femenino.
   - `Edad` se imputa con la mediana, se convierte a entero y se descartan menores de 16 o mayores de 95.
3. Pondera cada registro contra la distribución censal (`data/censo_2022_distribucion.csv`, población por provincia × sexo × grupo de edad). No hay valores hardcodeados: cualquier cambio en el CSV recalcula los pesos.
4. Calcula medias ponderadas sin suavizado para imagen e intención de voto del candidato objetivo y genera gráficos en `outputs/`.
5. Ejecuta tests de hipótesis y regresiones (OLS para imagen y logística para intención de voto) sobre variables sociodemográficas.

### Requisitos

- Python 3.10+
- pandas
- matplotlib
- seaborn
- statsmodels
- scipy

Instala dependencias con:

```bash
pip install pandas matplotlib seaborn statsmodels scipy
```

### Datos de ejemplo

En `data/` se incluyen:
- `censo_2022_distribucion.csv`: distribución poblacional aproximada del Censo 2022 por provincia (código y nombre), sexo y grupo de edad (`18-29`, `30-44`, `45-59`, `60+`).
- Tres olas de encuesta (`encuestas_2024-01.csv`, `encuestas_2024-02.csv`, `encuestas_2024-03.csv`) con valores de provincia escritos de forma parcial o abreviada para demostrar la normalización.

Puedes agregar nuevas olas siguiendo el patrón `encuestas_YYYY-MM.csv`; el notebook recalculará pesos y resultados automáticamente a partir de los CSV.

### Ejecución en VSCode

1. Abre `tracking_electoral.ipynb` en VSCode.
2. Selecciona un kernel de Python 3.10+ con las dependencias instaladas.
3. Ejecuta las celdas en orden. Se guardarán `outputs/imagen_ponderada.png` y `outputs/intencion_ponderada.png`, además de los resúmenes de regresiones e hipótesis en la salida de consola.
