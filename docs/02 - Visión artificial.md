# Visión artificial: detectar la línea roja

El controlador necesita una referencia para saber hacia dónde girar. En nuestro caso, esa referencia sale de la imagen de la cámara del coche. Antes de hablar de P, PD o PID, tenemos que convertir la imagen en un dato sencillo: **dónde está la línea roja respecto al centro**.

## 1. Imagen y detección del rojo

Obtenemos un fotograma con `HAL.getImage()` y lo convertimos de BGR a HSV usando OpenCV. HSV nos permite separar mejor el tono del brillo y la saturación.

Como el rojo está situado en los extremos de la escala de tono de OpenCV, utilizamos **dos intervalos** y unimos sus máscaras:

```python
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv, (0, 125, 125), (10, 255, 255))
mask2 = cv2.inRange(hsv, (170, 125, 125), (180, 255, 255))
mask = mask1 | mask2
```

El resultado es una imagen binaria: los píxeles detectados como rojos aparecen en blanco y el resto en negro.

## 2. Nos quedamos con una región de interés

No hace falta analizar toda la imagen. Descartamos su parte superior y conservamos la zona inferior, donde normalmente aparece el tramo de línea más relevante para la corrección inmediata:

```python
mask[:int(h * 0.45)] = 0
```

Esto significa que **se elimina el 45 % superior** y se analiza el 55 % restante. No debemos confundirlo con «analizar solo el 45 % inferior».

## 3. Contorno y centroide

Buscamos los contornos de la máscara y seleccionamos el de mayor área, siempre que supere un tamaño mínimo. Calculamos su centroide con los momentos de OpenCV:

```python
contours, _ = cv2.findContours(
    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)

if contours:
    contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(contour)
    if cv2.contourArea(contour) > 50 and M["m00"] > 0:
        cx = M["m10"] / M["m00"]
```

La coordenada `cx` indica la posición horizontal del centroide. Si el ancho de imagen es `w`, el error que usamos es:

```python
error = cx - w / 2.0
```

Con ese error construimos la orden angular del controlador.

## 4. ¿Qué pasa si perdemos la línea?

Puede suceder en una curva cerrada o si el coche se desplaza demasiado. En ese caso no conviene continuar utilizando un centroide inexistente. Nuestro código reduce la velocidad y gira en la dirección en la que se detectó la línea por última vez, intentando recuperarla.

Es una solución sencilla, no una garantía de recuperación. Por eso también nos interesa registrar cuántas veces ocurre.

## Limitaciones de este método

El centroide de un contorno grande **no equivale exactamente a la posición del coche sobre la línea**. En una curva, la forma del tramo visible puede desplazar el centroide aunque el vehículo esté bien colocado. Además, la detección depende de la iluminación, la máscara HSV y la región elegida.

De momento conservaremos este método en todos los controladores para que las comparaciones sean justas. Cuando estudiemos la **velocidad adaptativa**, podremos utilizar puntos de la línea a distintas alturas de la imagen para estimar si se aproxima una curva.

Relacionado: [[01 - Fundamentos del control]] · [[03 - Experimentos P]] · [[07 - Velocidad adaptativa]]
