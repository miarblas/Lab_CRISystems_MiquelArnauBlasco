Volver a [[00 - Índice]] · Anterior: [[04 - Experimentos PD]] · Siguiente: [[06 - Experimentos PID]]

## Qué queríamos comprobar

Después de ver la mejora del PD, tocaba estudiar qué ocurre al añadir la acción integral en lugar de la derivativa. La integral acumula el error con el tiempo y puede resultar útil si el coche mantiene una desviación persistente. La duda era si eso ayudaría a centrarlo o si, en un circuito con curvas continuas, acabaría empeorando las correcciones.

La expresión utilizada es:

$$
\omega = -\left(K_p e + K_i \int e\,dt\right)
$$

Se mantuvieron `KP = 0.010`, `KD = 0`, `V = 10`, `V_LOST = 4`, `W_LOST = 1.9` y el mismo procesamiento de imagen. La integral se acumula con el intervalo de tiempo válido, se limita a ±1000 píxel·segundo y se reinicia al perder la línea.

> **Nota sobre la tabla original:** en los datos compartidos, los valores `0.00001` y `0.00005` aparecían en la columna `kd`, con `ki = 0`. Aquí están registrados como **Ki**, porque estas pruebas se describieron como PI y el archivo `PI.py` compartido utiliza `KD = 0`. Conviene confirmar que los valores se introdujeron realmente en `KI` al ejecutar las pruebas.

## Resultados

| Prueba | Kp | Ki | Kd | Muestras | Tiempo web (s) | Completa | Pérdidas | MAE (px) | RMSE (px) |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| PI-1-1 | 0.010 | 0.00001 | 0 | 19418 | 91.49 | Sí | 0 | 153.67 | 174.62 |
| PI-1-2 | 0.010 | 0.00001 | 0 | 18595 | 92.32 | Sí | 0 | 147.58 | 172.61 |
| PI-1-3 | 0.010 | 0.00001 | 0 | 18120 | 89.31 | Sí | 0 | 144.63 | 167.97 |
| PI-2-1 | 0.010 | 0.00005 | 0 | 20137 | 92.35 | Sí | 0 | 122.97 | 151.40 |
| PI-2-2 | 0.010 | 0.00005 | 0 | 17825 | 87.22 | Sí | 0 | 146.58 | 172.57 |
| PI-2-3 | 0.010 | 0.00005 | 0 | 18207 | 90.91 | Sí | 0 | 147.43 | 172.83 |

### Resumen de las tres vueltas

| Ki | Tiempo medio web (s) | MAE medio (px) | RMSE medio (px) | Pérdidas totales | Vueltas completadas |
|---:|---:|---:|---:|---:|---:|
| 0.00001 | 91.04 | 148.63 | 171.73 | 0 | 3/3 |
| **0.00005** | **90.16** | **138.99** | **165.60** | **0** | **3/3** |

Con `KI = 0.00005` el error medio fue algo menor, aunque los resultados variaron bastante de una vuelta a otra. Ninguna de las seis vueltas perdió la detección de la línea.

## Comparación con P y PD

| Configuración | MAE medio (px) | RMSE medio (px) |
|---|---:|---:|
| P (`KP = 0.010`) | 124.40 | 153.76 |
| PI (`KI = 0.00001`) | 148.63 | 171.73 |
| PI (`KI = 0.00005`) | 138.99 | 165.60 |
| PD (`KD = 0.001`) | **58.88** | **85.19** |

En estas pruebas, **las dos configuraciones de PI tienen mayor MAE y RMSE que P**. Además, durante la primera configuración se observó que el coche zigzagueaba muchísimo, posiblemente más que con el control proporcional solo.

Una posible explicación es que la integral sigue acumulando desviación mientras el coche entra y sale de las curvas. Esa corrección acumulada puede dejar de ser útil cuando cambia la dirección del error, favoreciendo el balanceo. Es una interpretación razonable, pero no hemos medido la evolución completa de la integral para demostrarlo directamente.

## Interpretación y conclusión

La integral no ha mejorado el seguimiento en las configuraciones probadas. Aunque las seis vueltas terminaron sin pérdidas de detección, los errores visuales fueron superiores a los de P, y bastante mayores que los de PD.

Esto **no significa que PI sea siempre peor** ni que el término integral no sirva. Significa que, para este circuito, con estas ganancias y esta forma de detectar la línea, no ha aportado una mejora observable.

**Conclusión:** el resultado de PI justifica comprobar a continuación si un PID completo conserva las ventajas del término derivativo sin introducir demasiado efecto de la integral.

Los tiempos de la web se conservan como referencia, pero no se utilizan para establecer un ganador por la dependencia del rendimiento gráfico. Las métricas MAE y RMSE corresponden al error en la imagen y se han calculado únicamente con detecciones válidas.
