import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------- Funciones auxiliares ----------
def deg_wrap(rad):
    d = np.degrees(rad)
    return ((d + 180) % 360) - 180

# ---------- Funciones de vista 3D ----------
legend_done = False

def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)

def fix_system(axis_length, linewidth=2):
    global legend_done
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length]
    z = [-axis_length, axis_length]
    zp = [0,0]

    if not legend_done:
        ax.plot3D(x, zp, zp, color='red', linewidth=linewidth, label='Eje X')
        ax.plot3D(zp, y, zp, color='green', linewidth=linewidth, label='Eje Y')
        ax.plot3D(zp, zp, z, color='blue', linewidth=linewidth, label='Eje Z')
        ax.legend()
        legend_done = True
    else:
        ax.plot3D(x, zp, zp, color='red', linewidth=linewidth, label='_nolegend_')
        ax.plot3D(zp, y, zp, color='green', linewidth=linewidth, label='_nolegend_')
        ax.plot3D(zp, zp, z, color='blue', linewidth=linewidth, label='_nolegend_')

# ---------- Entrada ----------
L1 = float(input("Ingrese la longitud del primer brazo (L1): "))
L2 = float(input("Ingrese la longitud del segundo brazo (L2): "))
Xf = float(input("Ingrese la coordenada X final: "))
Yf = float(input("Ingrese la coordenada Y final: "))
Zf = float(input("Ingrese la coordenada Z final: "))
codo = input("Ingrese la posición del codo (arriba/abajo): ").strip().lower()

# ---------- Cinemática inversa ----------
# theta1: rotación de base
theta1 = np.arctan2(Yf, Xf)

# distancia radial en XY
r_xy = np.sqrt(Xf**2 + Yf**2)

# distancia total al punto
dist = np.sqrt(Xf**2 + Yf**2 + Zf**2)

# --------- FILTRO DE ALCANZABILIDAD ---------
if dist > (L1 + L2):
    print("El punto NO es alcanzable: √(Xf²+Yf²+Zf²) > L1+L2")
    raise SystemExit

# en el plano XZ resolvemos como un 2R
r2 = r_xy**2 + Zf**2
D = (r2 - L1**2 - L2**2) / (2*L1*L2)
D = np.clip(D, -1.0, 1.0)
s = np.sqrt(max(0.0, 1.0 - D*D))

# dos soluciones posibles para el codo
t3_a = np.arctan2(+s, D)
t3_b = np.arctan2(-s, D)

phi = np.arctan2(Zf, r_xy)
t2_a = phi - np.arctan2(L2*np.sin(t3_a), L1+L2*np.cos(t3_a))
t2_b = phi - np.arctan2(L2*np.sin(t3_b), L1+L2*np.cos(t3_b))

# elegir solución según codo
z1_a = L1*np.sin(t2_a)
z1_b = L1*np.sin(t2_b)

if codo.startswith("a"):
    theta2, theta3 = (t2_a, t3_a) if z1_a >= z1_b else (t2_b, t3_b)
else:
    theta2, theta3 = (t2_a, t3_a) if z1_a <= z1_b else (t2_b, t3_b)

print("Ángulos finales:")
print(f"θ1 = {deg_wrap(theta1):.2f}°  θ2 = {deg_wrap(theta2):.2f}°  θ3 = {deg_wrap(theta3):.2f}°")

# ---------- Gráfica 3D ----------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

rango = L1 + L2 + abs(Zf) + 1
setaxis(-rango, rango, -rango, rango, -rango, rango)
fix_system(rango)

# Dibujos iniciales
link1_line, = ax.plot([], [], [], 'b-', linewidth=5, label='Link 1')
link2_line, = ax.plot([], [], [], color='orange', linewidth=5, label='Link 2')
joints = ax.scatter([0,0,0],[0,0,0],[0,0,0], c=['black','green','purple'], s=60)
efector = ax.scatter([Xf],[Yf],[Zf], c='red', s=80, label='Punto final')

text_info = ax.text2D(0.02, 0.95,
                      f"θ1 = {deg_wrap(theta1):.1f}°\nθ2 = {deg_wrap(theta2):.1f}°\nθ3 = {deg_wrap(theta3):.1f}°",
                      transform=ax.transAxes)

# ---------- Animación ----------
frames = 80
def update(frame):
    alpha = frame / frames
    t1 = theta1 * alpha
    t2 = theta2 * alpha
    t3 = theta3 * alpha

    # cinemática directa en 3D
    x1 = L1 * np.cos(t2) * np.cos(t1)
    y1 = L1 * np.cos(t2) * np.sin(t1)
    z1 = L1 * np.sin(t2)

    x2 = x1 + L2 * np.cos(t2+t3) * np.cos(t1)
    y2 = y1 + L2 * np.cos(t2+t3) * np.sin(t1)
    z2 = z1 + L2 * np.sin(t2+t3)

    link1_line.set_data([0, x1], [0, y1])
    link1_line.set_3d_properties([0, z1])

    link2_line.set_data([x1, x2], [y1, y2])
    link2_line.set_3d_properties([z1, z2])

    joints._offsets3d = ([0, x1, x2],
                         [0, y1, y2],
                         [0, z1, z2])

    return link1_line, link2_line, joints, text_info

ani = FuncAnimation(fig, update, frames=frames+1, interval=30, blit=False)
plt.show()
