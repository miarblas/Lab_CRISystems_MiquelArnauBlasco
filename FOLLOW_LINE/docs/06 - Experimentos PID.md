Volver a [[00 - Índice]] · Anterior: [[05 - Experimentos PI]] · Siguiente: [[07 - Velocidad adaptativa]]

## Objetivo

Después de comprobar que el PD seguía la línea con bastante menos error que P, quedaba una pregunta: **¿mejora algo añadir también la integral?** Para responderla mantuvimos `KP = 0.010`, `KD = 0.001` y la velocidad lineal constante (`V = 10`), y probamos dos valores de `KI`.

La orden angular del controlador es:

$$
\omega = -\left(K_p e + K_i\int e\,dt + K_d\frac{de}{dt}\right)
$$

La cámara detecta la línea roja por HSV. Se calcula el centroide dentro de la misma región de interés utilizada en los ensayos anteriores. La integral incluye un límite de ±1000 px·s, la derivada está filtrada (`ALPHA_D = 0.25`) y el comportamiento al perder la línea se mantiene en `V_LOST = 4`, `W_LOST = 1.9`.

## Resultados de las seis vueltas

| Prueba | Kp | Ki | Kd | Muestras | Tiempo web (s) | Completa | Pérdidas | MAE (px) | RMSE (px) |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| PID-1-1 | 0.010 | 0.00005 | 0.001 | 17595 | 84.61 | Sí | 0 | 59.14 | 87.02 |
| PID-1-2 | 0.010 | 0.00005 | 0.001 | 17396 | 90.25 | Sí | 0 | 60.03 | 84.23 |
| PID-1-3 | 0.010 | 0.00005 | 0.001 | 18452 | 86.84 | Sí | 0 | 55.46 | 82.29 |
| PID-2-1 | 0.010 | 0.00001 | 0.001 | 18401 | 90.79 | Sí | 0 | 58.83 | 86.08 |
| PID-2-2 | 0.010 | 0.00001 | 0.001 | 17243 | 89.89 | Sí | 0 | 57.81 | 84.60 |
| PID-2-3 | 0.010 | 0.00001 | 0.001 | 17030 | 90.22 | Sí | 0 | 56.61 | 81.45 |

## Resumen

| Ki | Tiempo web medio | MAE medio | RMSE medio | Pérdidas | Vueltas completas |
|---:|---:|---:|---:|---:|---:|
| 0.00005 | 87.23 s | 58.21 px | 84.51 px | 0 | 3/3 |
| **0.00001** | 90.30 s | **57.75 px** | **84.04 px** | **0** | **3/3** |

La diferencia entre los dos ajustes es pequeña. El valor `KI = 0.00001` obtiene el menor error visual medio, mientras que `KI = 0.00005` registra un menor tiempo web. Como ya observamos durante el proyecto, el cronómetro puede variar por la carga gráfica del ordenador, así que no es suficiente para decidir qué ajuste es realmente más rápido.

## Comparación con los controladores anteriores

Se toma como representante de cada familia el ajuste probado con menor MAE medio, todos con velocidad lineal 10.

| Controlador | Ganancias | MAE medio (px) | RMSE medio (px) | Pérdidas en 3 vueltas |
|---|---|---:|---:|---:|
| P | Kp=0.010 | 124.40 | 153.76 | 2 |
| PI | Kp=0.010; Ki=0.00005 | 138.99 | 165.60 | 0 |
| PD | Kp=0.010; Kd=0.001 | 58.88 | 85.19 | 0 |
| **PID** | Kp=0.010; Ki=0.00001; Kd=0.001 | **57.75** | **84.04** | **0** |

La mejora grande apareció al introducir la derivada: el PD redujo considerablemente el error respecto a P. En cambio, añadir la integral al PD solo redujo el MAE de **58.88 a 57.75 px**, aproximadamente un **1.9 %**, y el RMSE de **85.19 a 84.04 px**. Con tres vueltas por configuración, esa diferencia no basta para afirmar que PID sea claramente superior.

Es interesante que PI, sin derivada, ofreciera más error que P en las ganancias estudiadas, mientras que PID quedó prácticamente empatado con PD. La acción integral **no ha demostrado una mejora importante** en este recorrido, aunque eso no significa que sea inútil en otros circuitos o con otros ajustes.

## Conclusión y siguiente paso

El PID completo ha obtenido el menor error medio de los ensayos a velocidad fija, pero la ganancia respecto al PD es pequeña. **Para este circuito, PD parece ofrecer un equilibrio muy razonable entre simplicidad y precisión.**

Por eso, en la siguiente fase compararemos **PD (`KP = 0.010`, `KD = 0.001`)** y **PID (`KP = 0.010`, `KI = 0.00001`, `KD = 0.001`)** con una estrategia de velocidad variable. El objetivo será ver si pueden acelerar en las rectas y reducir velocidad en las curvas sin perder la línea.

> **Limitaciones:** MAE y RMSE miden la desviación horizontal del centroide en la imagen, no una distancia física. Los datos son promedios de tres vueltas y el muestreo depende del rendimiento de la simulación. No se han medido directamente la curvatura física ni la velocidad real del vehículo.
