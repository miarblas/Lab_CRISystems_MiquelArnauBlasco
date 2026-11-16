# Fundamentos del control P, PI, PD y PID

## ¿Qué estamos controlando?

En **Follow Line**, el coche ve una línea roja mediante su cámara y debe intentar mantenerla cerca del centro de la imagen. Para ello enviamos dos órdenes al simulador: velocidad de avance (`HAL.setV`) y velocidad de giro (`HAL.setW`).

La idea básica es sencilla: si la línea aparece desplazada, tenemos que corregir la dirección. Lo interesante es decidir **cuánto girar** y **cómo evitar corregir demasiado**.

Llamamos *error* a la diferencia horizontal entre el centro de la línea detectada y el centro de la imagen:

$$e = x_{\text{línea}} - x_{\text{imagen}}$$

El signo de la orden de giro depende de cómo interprete Unibotics los giros. En nuestras pruebas usamos la convención `w = -control`, que hay que mantener igual al comparar los controladores.

## Control proporcional (P)

$$
u_P = K_p e
$$


El controlador P gira con una intensidad proporcional al error. Si la línea está lejos del centro, la corrección será mayor.

Es fácil de implementar y ya permite completar el circuito con algunas ganancias. Sin embargo, hemos visto que **puede zigzaguear en las rectas**. Si bajamos mucho `Kp`, el coche reacciona tan poco que puede salirse en las curvas. Hay un compromiso entre rapidez de reacción y suavidad.

## Control proporcional-derivativo (PD)

$$
u_{PD}=K_p e + K_d\frac{de}{dt}
$$

La parte derivativa mira **cómo está cambiando el error**, no solo cuánto vale. Puede ayudar a frenar las oscilaciones, aunque también es sensible al ruido de la cámara. Por eso conviene suavizar la derivada.

En las primeras pruebas con PD hemos observado movimientos más suaves que con P. Es un resultado prometedor, pero lo seguiremos contrastando.

## Control proporcional-integral (PI)

$$
u_{PI}=K_p e + K_i\int e\,dt
$$

La integral acumula el error a lo largo del tiempo. Su objetivo es corregir un **desplazamiento que se mantiene** pese a las correcciones proporcionales.

No siempre será útil aquí: las curvas hacen que el error cambie continuamente y una integral demasiado fuerte puede acumular corrección que ya no hace falta. Para evitarlo, limitaremos su valor (*anti-windup*) y la reiniciaremos si se pierde la línea.

## Control PID

$$
u_{PID}=K_p e + K_i\int e\,dt + K_d\frac{de}{dt}
$$

El PID reúne las tres ideas: reaccionar al error actual (P), corregir errores persistentes (I) y amortiguar cambios rápidos (D). En código calculamos una orden de giro a partir de esa suma.

**Más términos no significa automáticamente un mejor controlador.** Parte del trabajo consiste precisamente en comprobar si, para este circuito y esta cámara, merece la pena usar el PID completo o basta con PD.

## Para comparar con criterio

Empezaremos a la misma velocidad lineal y con la misma detección de línea. Modificaremos un parámetro cada vez y observaremos si el coche completa el recorrido, cómo gira en curvas y cuánto oscila en rectas. Después introduciremos una estrategia de velocidad adaptativa por separado.

Relacionado: [[02 - Visión artificial]] · [[03 - Experimentos P]] · [[04 - Experimentos PD]]
