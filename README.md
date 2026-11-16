# Follow Line — Unibotics | P, PD, PI, PID

Archivos **independientes** para copiar y pegar en el editor de Unibotics. La segmentación HSV, región de interés, centroide, reacción a pérdida de línea y velocidad fija `V=10` se mantienen iguales en los cuatro controladores.

## Orden de trabajo

1. `01_P/P.py` — P de referencia. Probar `KP=0.006, 0.008, 0.010` (el valor 0.004 falló en una primera curva con el equipo anterior).
2. `02_PD/PD.py` — probar `KD=0.0005` y `KD=0.001` con `KP=0.010`.
3. `03_PI/PI.py` — probar `KI=0.00005` inicialmente, y modificar con prudencia. Si la integral empeora la conducción, registrarlo.
4. `04_PID/PID.py` — empezar con `KP=0.010`, `KI=0.00005`, `KD=0.0005` y reajustar si hace falta.
5. `05_velocidad_adaptativa/PD_adaptativo.py` — **segunda fase**, con PD de base. `V_MIN=8`, `V_MAX=15` son valores de prueba, NO velocidades seguras o verificadas.

## Variables y límites

- Los términos I y D están escalados por `dt` (reloj real de Python), por lo que sus ganancias NO son directamente equivalentes a implementaciones por fotograma. Su resultado puede variar con la carga computacional.
- `DT_MAX=0.20` rechaza intervalos anormalmente largos; la medida de tiempo de simulación sería mejor si la plataforma la expusiese.
- Integral limitada y reiniciada al perder la línea. Derivada filtrada con `ALPHA_D=0.25`.
- MAE y RMSE son **errores de posición de la línea en píxeles**, no distancia física. En consola se imprimen valores **acumulados desde el inicio de la ejecución** (no por vuelta). El conteo `perdidas` significa transiciones de detectado a no detectado, incluyendo una pérdida inicial si sucede.
- Para comparar con rigor: misma escena, condiciones iniciales, parámetros de visión y tres vueltas por configuración. Si reinicias código entre vueltas, reinicias también los contadores.
- Los tiempos de la web pueden variar por GPU; la prueba en laboratorio puede reducir esa variabilidad, pero no garantizar eliminarla.

## ¿Qué hace el modo adaptativo?

La velocidad se reduce cuando aumenta el error lateral y/o el desplazamiento horizontal de la línea entre una banda cercana y otra más lejana. **Esto no mide la curvatura real**, pero puede servir como indicio de giro próximo. No usar sus resultados para atribuir diferencias exclusivamente al PD.

## Resultados

Utilizar `resultados/registro.csv` y `docs/Notas_experimentos.md` para documentar tiempos y observaciones.
