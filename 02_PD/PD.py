"""Unibotics Follow Line — PD.
Mismo procesamiento de cámara y recuperación para comparar controladores.
Ajusta las ganancias indicadas y ejecuta en el editor de Unibotics.
"""
import time
import cv2
import HAL
import WebGUI

# ---------- Configuración experimental ----------
KP = 0.010
KI = 0.0
KD = 0.0005
V = 10.0  # velocidad constante en P/PD/PI/PID
ROI_START = 0.45
MIN_AREA = 50.0
V_LOST = 4.0
W_LOST = 1.9
ALPHA_D = 0.25            # filtro derivativo: 0 < ALPHA_D <= 1
INTEGRAL_MAX = 1000.0    # límite en unidades de píxel*segundo
DT_MIN = 0.001
DT_MAX = 0.20             # evita saltos grandes tras bloqueos del simulador
REPORT_EVERY = 2.0       # segundos reales entre informes (evita saturar consola)

LABEL = "PD"

# ---------- Estado interno ----------
last_time = time.perf_counter()
last_report = last_time
prev_error = None
filtered_derivative = 0.0
integral = 0.0
last_dir = 1
lost = False
loss_events = 0
samples = 0
sum_abs_error = 0.0
sum_sq_error = 0.0
current_error = None
current_derivative = 0.0
current_angular = 0.0

while True:
    now = time.perf_counter()
    raw_dt = now - last_time
    last_time = now
    dt_valid = DT_MIN <= raw_dt <= DT_MAX

    img = HAL.getImage()
    if img is None:
        continue

    h, w = img.shape[:2]
    center = w / 2.0
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = (
        cv2.inRange(hsv, (0, 125, 125), (10, 255, 255)) |
        cv2.inRange(hsv, (170, 125, 125), (180, 255, 255))
    )
    mask[:int(h * ROI_START)] = 0
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    debug = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    found = False
    cx = None
    cy = None

    if contours:
        contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(contour) > MIN_AREA:
            moments = cv2.moments(contour)
            if moments["m00"] > 0:
                cx = moments["m10"] / moments["m00"]
                cy = moments["m01"] / moments["m00"]
                found = True

    if found:
        error = cx - center
        current_error = error
        last_dir = 1 if error >= 0 else -1
        lost = False
        samples += 1
        sum_abs_error += abs(error)
        sum_sq_error += error * error

        # La derivada debe expresarse en píxeles/segundo.
        # Sin muestra anterior válida se empieza con derivada cero.
        if prev_error is not None and dt_valid:
            raw_derivative = (error - prev_error) / raw_dt
            filtered_derivative = (
                ALPHA_D * raw_derivative +
                (1.0 - ALPHA_D) * filtered_derivative
            )
        else:
            filtered_derivative = 0.0

        # Integral con dt y límite anti-windup.
        if dt_valid:
            integral += error * raw_dt
            integral = max(-INTEGRAL_MAX, min(INTEGRAL_MAX, integral))
        prev_error = error

        current_derivative = filtered_derivative
        angular = -(
            KP * error +
            KI * integral +
            KD * filtered_derivative
        )
        current_angular = angular
        velocity = V
        HAL.setV(velocity)
        HAL.setW(angular)
        cv2.circle(debug, (int(cx), int(cy)), 6, (0, 255, 0), -1)
    else:
        if not lost:
            loss_events += 1
        lost = True
        current_error = None
        current_derivative = 0.0
        current_angular = -last_dir * W_LOST
        prev_error = None
        filtered_derivative = 0.0
        integral = 0.0
        HAL.setV(V_LOST)
        HAL.setW(-last_dir * W_LOST)

    cv2.line(debug, (int(center), 0), (int(center), h), (255, 0, 0), 2)
    WebGUI.showImage(debug)

    if now - last_report >= REPORT_EVERY:
        mae = sum_abs_error / samples if samples else 0.0
        rmse = (sum_sq_error / samples) ** 0.5 if samples else 0.0
        error_text = f"{current_error:.2f}" if current_error is not None else "SIN LINEA"
        print(
            f"{LABEL} | error={error_text} px | "
            f"de/dt={current_derivative:.2f} px/s | "
            f"w={current_angular:.3f} | "
            f"MAE={mae:.2f} px | RMSE={rmse:.2f} px | "
            f"perdidas={loss_events} | muestras={samples}"
        )
        last_report = now
