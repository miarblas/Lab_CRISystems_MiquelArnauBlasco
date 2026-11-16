# Follow Line — Diario del proyecto

Este proyecto parte del ejercicio **Follow Line de Unibotics**. La idea no es solo conseguir que el coche siga la línea roja, sino entender qué cambia cuando pasamos de un controlador proporcional (P) a uno PD, PI y, finalmente, PID.

Vamos probando los controladores en el simulador, apuntando lo que ocurre en las rectas y en las curvas y comparando sus resultados. Al final también queremos probar una **velocidad variable**: más rápida en recta y más prudente cuando la trayectoria se complica.

## Notas del proyecto

- [[01 - Fundamentos del control]] — Qué hace cada término P, I y D y qué esperamos de él.
- [[02 - Visión artificial]] — Cómo detectamos la línea roja y calculamos el error.
- [[03 - Experimentos P]] — Primeras pruebas y valores de Kp.
- [[04 - Experimentos PD]] — Qué ocurre al añadir el término derivativo.
- [[05 - Experimentos PI]] — Pruebas con la acción integral.
- [[06 - Experimentos PID]] — Combinación de los tres términos.
- [[07 - Velocidad adaptativa]] — Ajuste de velocidad en rectas y curvas.
- [[08 - Comparativa y conclusiones]] — Qué solución funcionó mejor y por qué.

> Las notas de experimentos y la comparativa final ya están preparadas. Las gráficas se guardan en `adjuntos/`.

## Cómo vamos a comparar

En cada configuración intentaremos completar **tres vueltas**, sin modificar a la vez la detección de línea, la velocidad y las ganancias del controlador. Apuntaremos el tiempo mostrado por Unibotics, si termina el recorrido, las pérdidas de línea y las oscilaciones que observemos.

**Importante:** el tiempo de la web puede depender de la carga gráfica del ordenador, en este caso tan solo acelerado por gráfica. Por eso no lo tomaremos como una medida perfecta del rendimiento del controlador: también importan la estabilidad y la capacidad de superar las curvas.


## Gráficas principales

![[01_comparativa_controladores.png]]

![[03_compromiso_velocidad_precision.png]]


