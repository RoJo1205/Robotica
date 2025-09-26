import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def angulos_ambas_soluciones(L1, L2, Xf, Yf):
    """Devuelve (t1_a,t2_a), (t1_b,t2_b) en radianes para las dos soluciones posibles."""
    r2 = Xf**2 + Yf**2
    D = (r2 - L1**2 - L2**2) / (2 * L1 * L2)

    if D < -1 - 1e-9 or D > 1 + 1e-9:
        raise ValueError("Punto no alcanzable: D fuera de [-1,1].")
    D = np.clip(D, -1.0, 1.0)

    s = np.sqrt(max(0.0, 1.0 - D*D))
    # Dos posibles theta2
    t2_a = np.arctan2(+s, D)
    t2_b = np.arctan2(-s, D)

    # Para cada theta2, calcular theta1
    common = np.arctan2(Yf, Xf)
    t1_a = common - np.arctan2(L2 * np.sin(t2_a), L1 + L2 * np.cos(t2_a))
    t1_b = common - np.arctan2(L2 * np.sin(t2_b), L1 + L2 * np.cos(t2_b))

    return (t1_a, t2_a), (t1_b, t2_b)

def deg_wrap(rad):
    """Convierte rad -> grados y lo normaliza a (-180,180]."""
    d = np.degrees(rad)
    return ((d + 180) % 360) - 180

# ------------------ Entrada ------------------
L1 = float(input("Ingrese la longitud del primer brazo (L1): "))
L2 = float(input("Ingrese la longitud del segundo brazo (L2): "))
Xf = float(input("Ingrese la coordenada X del punto final (Xf): "))
Yf = float(input("Ingrese la coordenada Y del punto final (Yf): "))
codo = input("Ingrese la posición del codo (arriba/abajo): ").strip().lower()

# Verificación simple de alcanzabilidad
if np.sqrt(Xf**2 + Yf**2) > (L1 + L2):
    print("El punto NO es alcanzable: √(Xf² + Yf²) > L1 + L2.")
    raise SystemExit

# ------------------ Calcula las dos soluciones ------------------
(solA_t1, solA_t2), (solB_t1, solB_t2) = angulos_ambas_soluciones(L1, L2, Xf, Yf)

# Coordenadas del codo para cada solución
x1_a, y1_a = L1 * np.cos(solA_t1), L1 * np.sin(solA_t1)
x1_b, y1_b = L1 * np.cos(solB_t1), L1 * np.sin(solB_t1)

# ------------------ Elegir solución según 'codo' ------------------
if codo.startswith('a'):   # "arriba"
    chosen_idx = 0 if y1_a >= y1_b else 1
else:                      # "abajo"
    chosen_idx = 0 if y1_a <= y1_b else 1

if chosen_idx == 0:
    theta1, theta2 = solA_t1, solA_t2
    chosen_label = 'A'
else:
    theta1, theta2 = solB_t1, solB_t2
    chosen_label = 'B'

# Mostrar solo los ángulos finales
print("Ángulo θ1 = {:.2f}°, θ2 = {:.2f}°".format(deg_wrap(theta1), deg_wrap(theta2)))

# ------------------ Preparar animación 2D ------------------
fig, ax = plt.subplots()
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_aspect("equal")
rango = L1 + L2 + 1
ax.set_xlim(-rango, rango)
ax.set_ylim(-rango, rango)
ax.set_title("Animación: movimiento (XY)")

# Gráficos iniciales
link1_line, = ax.plot([], [], 'b-', linewidth=5, label='Link 1')
link2_line, = ax.plot([], [], color='orange', linewidth=5, label='Link 2')
joints = ax.scatter([0,0,0],[0,0,0], c=['black','green','purple'], s=60)
efector = ax.scatter([Xf],[Yf], c='red', s=80, label='Punto final')
ax.legend(loc='upper right')

# Texto fijo con la solución elegida
text_info = ax.text(0.02, 0.95,
                    f"Angulos: \nθ1 = {deg_wrap(theta1):.1f}°\nθ2 = {deg_wrap(theta2):.1f}°",
                    transform=ax.transAxes, verticalalignment='top')

# ------------------ Animación (interpolación conjunta) ------------------
frames = 80

def update(frame):
    alpha = frame / frames
    t1 = theta1 * alpha
    t2 = theta2 * alpha

    x1 = L1 * np.cos(t1)
    y1 = L1 * np.sin(t1)
    x2 = x1 + L2 * np.cos(t1 + t2)
    y2 = y1 + L2 * np.sin(t1 + t2)

    link1_line.set_data([0, x1], [0, y1])
    link2_line.set_data([x1, x2], [y1, y2])
    joints.set_offsets(np.column_stack(([0, x1, x2], [0, y1, y2])))

    return link1_line, link2_line, joints, text_info

ani = FuncAnimation(fig, update, frames=frames+1, interval=30, blit=True)
plt.show()
