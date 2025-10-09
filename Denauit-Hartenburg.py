import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D # Necesario para la proyección 3D

# ----------------------------------------------------
# ---------- Funciones que proporcionaste ----------
# (Estas funciones no cambian)
# ----------------------------------------------------

def deg_wrap(rad):
    """Convierte radianes a grados en el rango [-180, 180]."""
    d = np.degrees(rad)
    return ((d + 180) % 360) - 180

def setaxis(ax, x1, x2, y1, y2, z1, z2):
    """Establece los límites de los ejes 3D."""
    ax.set_xlim3d(x1, x2)
    ax.set_ylim3d(y1, y2)
    ax.set_zlim3d(z1, z2)

def fix_system(ax, axis_length, linewidth=2):
    """Dibuja los ejes coordenados X (rojo), Y (verde), Z (azul)."""
    x_axis = [-axis_length, axis_length]
    y_axis = [-axis_length, axis_length]
    z_axis = [-axis_length, axis_length]
    zero_point = [0, 0]
    
    ax.plot3D(x_axis, zero_point, zero_point, color='red', linewidth=linewidth, label='Eje X')
    ax.plot3D(zero_point, y_axis, zero_point, color='green', linewidth=linewidth, label='Eje Y')
    ax.plot3D(zero_point, zero_point, z_axis, color='blue', linewidth=linewidth, label='Eje Z')

def matrizDenavitHartenberg(theta, d, a, alpha):
    """Calcula la matriz de transformación homogénea de Denavit-Hartenberg."""
    ct = np.cos(theta)
    st = np.sin(theta)
    ca = np.cos(alpha)
    sa = np.sin(alpha)

    return np.array([
        [ct, -st * ca, st * sa, a * ct],
        [st, ct * ca, -ct * sa, a * st],
        [0, sa, ca, d],
        [0, 0, 0, 1]
    ])





# Parámetros para el Eslabón 1
d1 = float(input("Ingrese 'd' para el eslabón 1: "))
a1 = float(input("Ingrese 'a' (longitud) para el eslabón 1: "))
alpha1_deg = float(input("Ingrese 'alpha' (en grados) para el eslabón 1: "))
alpha1 = np.radians(alpha1_deg)

# Parámetros para el Eslabón 2
d2 = float(input("\nIngrese 'd' para el eslabón 2: "))
a2 = float(input("Ingrese 'a' (longitud) para el eslabón 2: "))
alpha2_deg = float(input("Ingrese 'alpha' (en grados) para el eslabón 2: "))
alpha2 = np.radians(alpha2_deg)

#  Pedir los ángulos finales deseados
print("\nIngrese los ángulos finales para la posición del robot")
theta1_final_deg = float(input("Ingrese el ángulo final 'theta1': "))
theta2_final_deg = float(input("Ingrese el ángulo final 'theta2': "))

# Convertir los ángulos finales a radianes
theta1_final_rad = np.radians(theta1_final_deg)
theta2_final_rad = np.radians(theta2_final_deg)


# 2. Configuración de la figura y el entorno 3D
fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111, projection='3d')

# 3. Matriz de rotación inicial de 90 grados (sin cambios)
rot_angle_base = np.radians(-90)
T_base = np.array([
    [1, 0, 0, 0],
    [0, np.cos(rot_angle_base), -np.sin(rot_angle_base), 0],
    [0, np.sin(rot_angle_base), np.cos(rot_angle_base), 0],
    [0, 0, 0, 1]
])

# Función de actualización modificada
def update(angle_pair, d1, a1, alpha1, d2, a2, alpha2):
    ax.cla()

    # Desempaquetar el par de ángulos para el frame actual
    theta1, theta2 = angle_pair

    # El resto de la cinemática y el dibujo es igual
    T0_1 = matrizDenavitHartenberg(theta1, d1, a1, alpha1)
    T1_2 = matrizDenavitHartenberg(theta2, d2, a2, alpha2)
    T_base_1 = T_base @ T0_1
    T_base_2 = T_base_1 @ T1_2
    
    p_origen = np.array([0, 0, 0])
    p1 = T_base_1[:3, 3]
    p2 = T_base_2[:3, 3]

    ax.plot3D([p_origen[0], p1[0]], [p_origen[1], p1[1]], [p_origen[2], p1[2]], color='darkcyan', linewidth=6, marker='o', markersize=10, label='Eslabón 1')
    ax.plot3D([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='purple', linewidth=6, marker='o', markersize=10, label='Eslabón 2')

    max_range = abs(a1) + abs(a2) + max(abs(d1), abs(d2)) + 0.5
    setaxis(ax, -max_range, max_range, -max_range, max_range, -max_range, max_range)
    fix_system(ax, max_range * 0.6)
    
    ax.view_init(elev=25, azim=45)
    ax.set_title('Animación de Robot a Posición Final')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.legend(loc='upper left')
    fig.tight_layout()

# Crear la secuencia de frames para la animación
num_steps = 120 # Define en cuántos pasos llegará el robot a su destino

# Generar la trayectoria de los ángulos desde 0 hasta el ángulo final
theta1_trajectory = np.linspace(0, theta1_final_rad, num_steps)
theta2_trajectory = np.linspace(0, theta2_final_rad, num_steps)


animation_frames = np.stack((theta1_trajectory, theta2_trajectory), axis=-1)


ani = FuncAnimation(fig, update, frames=animation_frames,
                    fargs=(d1, a1, alpha1, d2, a2, alpha2),
                    interval=40,
                    blit=False,
                    repeat=False) # <--- ¡Este es el cambio clave para que no se repita!

plt.show()