# Laboratorio de Control y Robótica

Este repositorio reúne las prácticas y pequeños proyectos que voy desarrollando en el laboratorio. La idea es tener el código, las pruebas y las notas en un mismo sitio, tanto para seguir la evolución de cada ejercicio como para poder volver a consultarlo más adelante.

No todos los proyectos tendrán la misma estructura: iré organizando cada uno según lo que necesite.

## Proyectos

### Follow Line — Unibotics

El primer ejercicio consiste en hacer que un vehículo simulado siga una línea roja utilizando la imagen de su cámara. A partir de una detección sencilla con OpenCV, he probado distintas estrategias de control de dirección:

- **P:** punto de partida para estudiar cómo afecta la ganancia proporcional.
- **PD:** incorporación de la derivada para reducir las oscilaciones.
- **PI:** pruebas con el término integral y análisis de sus efectos.
- **PID:** combinación de los tres términos y comparación con PD.
- **Velocidad adaptativa:** ajustes de velocidad según el error visual y la forma aparente de la línea.

En cada caso he registrado varias vueltas y he comparado el error medio absoluto (MAE), el error cuadrático medio (RMSE), las pérdidas de detección y el tiempo mostrado por el simulador.

**Resultado principal:** en las configuraciones ensayadas, PD consigue una mejora importante respecto a P. PID obtiene errores ligeramente menores, pero la diferencia es pequeña. Aumentar la velocidad permite completar el circuito en menos tiempo mostrado por la web, aunque empeora la precisión del seguimiento.

Los tiempos se interpretan con cautela porque pueden verse afectados por el rendimiento gráfico del equipo. El MAE y el RMSE corresponden al error en la imagen, no a la distancia física a la línea.

**Dónde encontrarlo:**

| Carpeta | Contenido |
| --- | --- |
| [`01_P/`](01_P/) | Control proporcional |
| [`02_PD/`](02_PD/) | Control PD y variantes adaptativas |
| [`03_PI/`](03_PI/) | Control PI |
| [`04_PID/`](04_PID/) | Control PID |
| [`05_velocidad_adaptativa/`](05_velocidad_adaptativa/) | Comparación de estrategias de velocidad |
| [`06_resultados/`](06_resultados/) | Registro de pruebas, tablas y gráficas |
| [`docs/`](docs/) | Notas del proyecto en Markdown / Obsidian |

La documentación empieza en **[Índice de Follow Line](docs/00%20-%20%C3%8Dndice.md)**. Para consultar los datos originales, se puede abrir [`registro.csv`](06_resultados/registro.csv).

