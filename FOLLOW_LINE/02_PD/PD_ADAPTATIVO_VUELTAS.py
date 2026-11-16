import time
import cv2
import HAL
import WebGUI

# Ganancias PD ya ensayadas
KP = 0.010
KD = 0.001
ALPHA_D = 0.25

# Vision y busqueda
ROI_START = 0.45
MIN_AREA = 50.0
V_LOST = 4.0
W_LOST = 1.9
DT_MIN = 0.001
DT_MAX = 0.20
REPORT_EVERY = 2.0


MODO = 'referencia'
V_MIN = 8.0
V_MAX = 15.0
if MODO == 'referencia':
    K_V_ERROR = 0.020
    K_V_AHEAD = 0.030
elif MODO == 'curvas':
    K_V_ERROR = 0.025
    K_V_AHEAD = 0.045
else:
    raise ValueError('MODO debe ser referencia o curvas')


def band_center(mask, y0, y1):
    h = mask.shape[0]
    band = mask[int(h * y0):int(h * y1), :]
    m = cv2.moments(band, binaryImage=True)
    if m['m00'] < MIN_AREA:
        return None
    return m['m10'] / m['m00']


last_time = time.perf_counter()
start_time = last_time
last_report = last_time
prev_error = None
filtered_derivative = 0.0
last_dir = 1
lost = False
loss_events = 0
samples = 0
sum_abs_error = 0.0
sum_sq_error = 0.0
sum_speed = 0.0
current_error = None
current_angular = 0.0
current_speed = 0.0

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
    cx = cy = None
    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > MIN_AREA:
            M = cv2.moments(c)
            if M['m00'] > 0:
                cx = M['m10'] / M['m00']
                cy = M['m01'] / M['m00']
                found = True

    if found:
        error = cx - center
        current_error = error
        last_dir = 1 if error >= 0 else -1
        lost = False
        samples += 1
        sum_abs_error += abs(error)
        sum_sq_error += error * error

        if prev_error is not None and dt_valid:
            derivative = (error - prev_error) / raw_dt
            filtered_derivative = (
                ALPHA_D * derivative +
                (1.0 - ALPHA_D) * filtered_derivative
            )
        else:
            filtered_derivative = 0.0
        prev_error = error

        angular = -(KP * error + KD * filtered_derivative)
        current_angular = angular

        near_x = band_center(mask, 0.80, 0.95)
        far_x = band_center(mask, 0.55, 0.65)
        if near_x is None or far_x is None:
            # Reproduce la politica antigua en modo referencia.
            # En modo curvas, ante informacion incompleta, frena.
            ahead = 0.0
            speed = V_MIN if MODO == 'curvas' else max(
                V_MIN, min(V_MAX, V_MAX - K_V_ERROR * abs(error))
            )
        else:
            ahead = abs(far_x - near_x)
            speed = max(V_MIN, min(
                V_MAX,
                V_MAX - K_V_ERROR * abs(error) - K_V_AHEAD * ahead
            ))
        current_speed = speed
        sum_speed += speed
        HAL.setV(speed)
        HAL.setW(angular)
        cv2.circle(debug, (int(cx), int(cy)), 6, (0, 255, 0), -1)
    else:
        if not lost:
            loss_events += 1
        lost = True
        current_error = None
        current_angular = -last_dir * W_LOST
        prev_error = None
        filtered_derivative = 0.0
        current_speed = V_LOST
        HAL.setV(V_LOST)
        HAL.setW(current_angular)

    cv2.line(debug, (int(center), 0), (int(center), h), (255, 0, 0), 2)
    WebGUI.showImage(debug)

    if now - last_report >= REPORT_EVERY:
        mae = sum_abs_error / samples if samples else 0.0
        rmse = (sum_sq_error / samples) ** 0.5 if samples else 0.0
        err_txt = f'{current_error:.2f}' if current_error is not None else 'SIN LINEA'
        print(
            f'PD {MODO} | tiempo_ejecucion={now - start_time:.1f}s | '
            f'error={err_txt} px | de/dt={filtered_derivative:.2f} px/s | '
            f'w={current_angular:.3f} | V={current_speed:.2f} | '
            f'V_media={sum_speed / samples if samples else 0.0:.2f} | '
            f'MAE={mae:.2f} px | RMSE={rmse:.2f} px | '
            f'perdidas={loss_events} | muestras={samples}'
        )
        last_report = now
