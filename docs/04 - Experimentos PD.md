Volver a [[00 - Índice]] · Anterior: [[03 - Experimentos P]] · Siguiente: [[05 - Experimentos PI]]

## Qué queríamos comprobar

Después de probar el controlador P, el coche seguía la línea, pero tendía a zigzaguear, especialmente en las rectas. La idea al añadir el término derivativo era ver si conseguíamos suavizar esas correcciones sin perder capacidad de giro en las curvas.

El controlador utilizado fue:

$$
\omega = -\left(K_p e + K_d \frac{de}{dt}\right)
$$

Se mantuvieron `KP = 0.010`, `V = 10`, `V_LOST = 4`, `W_LOST = 1.9`, la misma detección HSV, la región de interés y el filtro de la derivada (`ALPHA_D = 0.25`). Se probaron dos valores de `KD`, con tres vueltas cada uno.

## Resultados

| Prueba | Kp | Kd | Muestras | Tiempo web (s) | Completa | Pérdidas | MAE (px) | RMSE (px) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PD-1-1 | 0.010 | 0.0010 | 20115 | 87.10 | Sí | 0 | 59.78 | 85.69 |
| PD-1-2 | 0.010 | 0.0010 | 18021 | 82.95 | Sí | 0 | 56.18 | 82.50 |
| PD-1-3 | 0.010 | 0.0010 | 17759 | 85.46 | Sí | 0 | 60.68 | 87.38 |
| PD-2-1 | 0.010 | 0.0005 | 19369 | 87.25 | Sí | 0 | 62.20 | 90.45 |
| PD-2-2 | 0.010 | 0.0005 | 18978 | 84.64 | Sí | 0 | 61.08 | 90.13 |
| PD-2-3 | 0.010 | 0.0005 | 18837 | 90.14 | Sí | 0 | 63.40 | 90.70 |

### Resumen de las tres vueltas

| Kd | Tiempo medio web (s) | MAE medio (px) | RMSE medio (px) | Pérdidas totales | Vueltas completadas |
|---:|---:|---:|---:|---:|---:|
| 0.0005 | 87.34 | 62.23 | 90.43 | 0 | 3/3 |
| **0.0010** | **85.17** | **58.88** | **85.19** | **0** | **3/3** |

Los dos ajustes completaron el circuito sin perder la detección de la línea. `KD = 0.001` obtuvo los menores errores medios de los dos.

## Comparación con P

Tomamos como referencia P con `KP = 0.010`, cuyo MAE medio fue **124.40 px** y RMSE medio **153.76 px**. Al añadir la derivada (`KD = 0.001`), los valores bajaron a **58.88 px** y **85.19 px**, respectivamente. Eso equivale a una reducción aproximada del **52.7 % en MAE** y del **44.6 % en RMSE**.

En las pruebas iniciales del PD también se observó que el coche zigzagueaba mucho menos y tomaba las curvas de manera más suave. Esta impresión coincide con la reducción del error visual registrada en las vueltas posteriores, aunque la suavidad del giro no se midió directamente.

## Interpretación y conclusión

El término derivativo parece aportar una mejora clara en este circuito: tiene en cuenta cómo cambia el error y ayuda a evitar correcciones excesivas. Entre los dos valores probados, elegiría **`KP = 0.010`, `KD = 0.001`** para seguir experimentando.

No consideramos el tiempo web una medida exacta de rendimiento porque puede variar con la carga gráfica del simulador. Además, el MAE y el RMSE reflejan el error horizontal del centroide en la imagen, no la distancia física del vehículo a la línea.

**Conclusión:** dentro de los ajustes ensayados, PD ha sido más preciso que P y no ha registrado pérdidas de detección. Es un buen candidato para la posterior prueba de velocidad adaptativa.
