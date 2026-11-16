# Controlador P — Seguimiento de línea

[[00 - Índice]] · [[01 - Fundamentos del control]] · [[02 - Visión artificial]]

## Qué queríamos comprobar

Empezamos con el controlador proporcional porque es la forma más sencilla de corregir la dirección a partir de la posición de la línea roja en la imagen. La orden angular se calcula con:

$$omega = -K_p e$$

Aquí, `e` es el desplazamiento horizontal, en píxeles, entre el centroide detectado de la línea y el centro de la imagen. La intención era observar cómo influía `Kp` en las curvas y en el zigzagueo de las rectas antes de introducir los términos integral y derivativo.

## Condiciones de las pruebas

- Circuito y algoritmo de visión: los mismos en todas las vueltas.
- Velocidad lineal de seguimiento: **10** (constante).
- `KI = 0`, `KD = 0`.
- Recuperación de línea: `V_LOST = 4`, `W_LOST = 1,9`.
- **Tres vueltas por cada valor de `Kp`**.
- Se registraron muestras, tiempo mostrado por la web, finalización, episodios de pérdida de línea, MAE y RMSE.

## Datos por vuelta

| Prueba | Kp | Muestras | Tiempo web (s) | Completa | Pérdidas | MAE (px) | RMSE (px) |
|---|---:|---:|---:|---:|---:|---:|---:|
| P-3-1 | 0,007 | 19478 | 88,84 | Sí | 0 | 130,11 | 158,74 |
| P-3-2 | 0,007 | 18417 | 85,25 | Sí | 1 | 162,85 | 184,91 |
| P-3-3 | 0,007 | 19528 | 86,20 | Sí | 1 | 130,23 | 157,29 |
| P-1-1 | 0,008 | 18191 | 83,66 | Sí | 2 | 153,65 | 176,94 |
| P-1-2 | 0,008 | 19691 | 87,33 | Sí | 0 | 130,14 | 156,80 |
| P-1-3 | 0,008 | 17627 | 85,23 | Sí | 1 | 157,91 | 180,39 |
| P-4-1 | 0,009 | 17122 | 83,50 | Sí | 0 | 146,90 | 171,35 |
| P-4-2 | 0,009 | 18122 | 84,16 | Sí | 1 | 144,90 | 169,42 |
| P-4-3 | 0,009 | 18214 | 84,93 | Sí | 0 | 142,71 | 168,27 |
| P-2-1 | 0,010 | 18852 | 89,09 | Sí | 1 | 128,95 | 157,58 |
| P-2-2 | 0,010 | 19127 | 85,75 | Sí | 1 | 122,27 | 151,67 |
| P-2-3 | 0,010 | 19892 | 89,78 | Sí | 0 | 121,99 | 152,03 |

## Resumen de resultados

| Kp | Tiempo medio (s) | Desv. típica tiempo (s) | MAE medio (px) | RMSE medio (px) | Pérdidas totales | Vueltas completas |
|---|---:|---:|---:|---:|---:|---:|
| 0,007 | 86,76 | 1,86 | 141,06 | 166,98 | 2 | 3/3 |
| 0,008 | 85,41 | 1,84 | 147,23 | 171,38 | 3 | 3/3 |
| 0,009 | **84,20** | **0,72** | 144,84 | 169,68 | **1** | 3/3 |
| 0,010 | 88,21 | 2,16 | **124,40** | **153,76** | 2 | 3/3 |

Las desviaciones típicas de tiempo son *muestrales*. El MAE y RMSE resumidos son la media de las métricas de las tres vueltas (no una combinación de todos los fotogramas).

## Lo que observamos

Con `Kp = 0,007`, el coche llegó a completar las tres vueltas, pero fue la configuración que dio peor sensación de conducción: al corregir la trayectoria pegaba bandazos y zigzagueaba continuamente. No parecía suficiente con mirar solo el tiempo para valorar el resultado.

Con `Kp = 0,008`, el seguimiento fue viable, aunque el error visual medio resultó el más alto de los cuatro ajustes estudiados. En esta configuración se contabilizaron tres pérdidas de detección entre las tres vueltas.

Con `Kp = 0,009`, los tiempos fueron bastante uniformes (83,50; 84,16; 84,93 s), y solo apareció una pérdida de línea. Es el mejor resultado en tiempo mostrado por la web, aunque no el mejor en error de seguimiento.

Con `Kp = 0,010`, los errores MAE y RMSE fueron claramente menores. A cambio, el tiempo medio mostrado por la web fue algo superior. En conjunto, es la configuración más interesante si priorizamos la precisión visual.

## Qué significa y qué no podemos concluir

El valor de `Kp` modifica el compromiso entre capacidad de corrección y calidad del seguimiento. Ninguno de los valores probados domina todos los indicadores: `0,009` destaca por tiempo y pocas pérdidas, mientras que `0,010` destaca por precisión visual. Por eso, no tiene sentido declarar un único ganador absoluto.

Además, **el tiempo que muestra Unibotics depende en parte del rendimiento del ordenador y de la carga gráfica**, por lo que lo utilizamos como indicador orientativo. El MAE y RMSE están expresados en **píxeles de imagen**, no en metros de desviación física. También pueden depender de la zona de imagen seleccionada y de la frecuencia de muestreo. Las pérdidas registradas se interpretan como episodios sin detección de línea, no necesariamente salidas de pista, siempre que el contador del código cuente episodios.

## Conclusión y siguiente paso

El controlador P consigue completar el circuito con los cuatro valores ensayados, pero las observaciones de zigzagueo y las diferencias entre métricas justifican explorar un controlador con mayor amortiguación. Para el siguiente bloque se elige **`Kp = 0,010`**, con **velocidad 10**, porque obtiene los menores errores visuales medios y permite comparar directamente P y PD manteniendo fija la parte proporcional.

El primer ensayo PD empleará `Kp = 0,010` y `Kd = 0,0005`. Después probaremos `Kd = 0,001` sin alterar el resto de condiciones. Así podremos comprobar qué aporta realmente el término derivativo.

→ [[04 - Experimentos PD]]
