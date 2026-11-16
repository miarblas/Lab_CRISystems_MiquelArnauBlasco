# Gráficas de los experimentos

Se han elaborado a partir de `registro.csv`. Las medias se calculan sobre las **tres vueltas completadas** por configuración.

- `01_comparativa_controladores.png`: MAE y RMSE a velocidad fija (mejor configuración probada de P, PI, PD y PID).
- `02_ajuste_derivativo.png`: efecto de probar Kd = 0,0005 y 0,001 en PD.
- `03_compromiso_velocidad_precision.png`: tiempo medio frente a MAE con velocidad adaptativa.
- `04_repeticiones_velocidad.png`: variación de tiempo entre las tres ejecuciones por configuración.

**Limitaciones:** el tiempo de la web puede variar con la carga gráfica; MAE/RMSE son errores en píxeles, no distancia física. Las barras/gráficas resumen medias por vuelta, no datos de fotogramas.

**Nota:** el CSV incluye filas vacías y parámetros anotados al pie; esas filas se excluyeron. VA-PD-4 se interpreta como V_MIN=10 y V_MAX=20, como registra la versión final del CSV.
