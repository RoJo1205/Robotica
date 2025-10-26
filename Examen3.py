import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

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

# Funciones Denavit-Hartenberg 

def dh_matrix_modified(alpha_prev, a_prev, d, theta):
    alpha_rad = np.deg2rad(alpha_prev)
    theta_rad = np.deg2rad(theta)

    Rx = np.array([
        [1, 0, 0, 0],
        [0, np.cos(alpha_rad), -np.sin(alpha_rad), 0],
        [0, np.sin(alpha_rad),  np.cos(alpha_rad), 0],
        [0, 0, 0, 1]
    ])
    
    Tx = np.array([
        [1, 0, 0, a_prev],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    
    Rz = np.array([
        [np.cos(theta_rad), -np.sin(theta_rad), 0, 0],
        [np.sin(theta_rad),  np.cos(theta_rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    
    Tz = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, d],
        [0, 0, 0, 1]
    ])
    
    T = Rx.dot(Tx).dot(Rz).dot(Tz)
    return T


def plot_robot(ax, theta1, theta2, d3, theta4):
    
    L1 = 475.0
    L2 = 375.0 
    d1 = 418.5
    d4_tool = 0   

    T0_1 = dh_matrix_modified(0, 0, d1, theta1)
    T1_2 = dh_matrix_modified(0, L1, 0, theta2)
    T2_3_base = dh_matrix_modified(180, L2, 0, 0)
    T2_3_tip = dh_matrix_modified(180, L2, d3, 0)
    T3_4 = dh_matrix_modified(0, 0, d4_tool, theta4)

    T0_0 = np.identity(4)
    T0_2 = T0_1 @ T1_2
    T0_3_base = T0_2 @ T2_3_base 
    T0_3_tip = T0_2 @ T2_3_tip   
    T0_4_EE = T0_3_tip @ T3_4 

    P0 = T0_0[0:3, 3] 
    P1 = T0_1[0:3, 3] 
    P2 = T0_2[0:3, 3] 
    P3 = T0_3_base[0:3, 3] 
    P4 = T0_3_tip[0:3, 3] 
    P5 = T0_4_EE[0:3, 3] 

    points = np.array([P0, P1, P2, P3, P4, P5])
    X = points[:, 0]
    Y = points[:, 1]
    Z = points[:, 2]

    # --- Dibujar ---
    # Eslabones
    line, = ax.plot(X, Y, Z, marker='o', markersize=8, markerfacecolor='red', color='blue', linewidth=3, label='Eslabonamiento del Robot')
    
    # Etiquetas
    t0 = ax.text(P0[0], P0[1], P0[2], ' P0 (Base)', c='k')
    t2 = ax.text(P2[0], P2[1], P2[2], ' P2 (Codo)', c='k')
    t5 = ax.text(P5[0], P5[1], P5[2], ' P5 (Herramienta)', c='red')

    # Devolver los objetos creados para poder borrarlos
    return [line, t0, t2, t5]


def main():
    
    # --- Configuración inicial del gráfico ---
    plt.ion() # Activar modo interactivo
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Límites y configuración estática (se define una vez)
    L1 = 475.0
    L2 = 375.0
    max_range = L1 + L2 + 100 # 950
    setaxis(ax, -max_range, max_range, -max_range, max_range, 0, max_range)
    fix_system(ax, 200) # Ejes de coordenadas
    ax.set_xlabel('Eje X (mm)')
    ax.set_ylabel('Eje Y (mm)')
    ax.set_zlabel('Eje Z (mm)')
    ax.set_box_aspect([1, 1, 1]) 

    # Pose actual (inicia en 0)
    current_pose = [0.0, 0.0, 0.0, 0.0] # t1, t2, d3, t4
    
    # Dibujar la pose inicial
    plot_handles = plot_robot(ax, *current_pose)
    ax.set_title(f'Robot SCARA i4-850H (Pose Inicial)')
    plt.show(block=False) # Muestra la ventana sin bloquear la ejecución
    
    while True:
        try:
            print("\n--- Ingrese la POSE OBJETIVO ---")
            theta1_t = float(input("Ingrese theta 1 (grados para rotación base): "))
            theta2_t = float(input("Ingrese theta 2 (grados para rotación codo): "))
            d3_t = float(input("Ingrese d3 (mm para extensor 0-210): "))
            theta4_t = float(input("Ingrese theta 4 (grados para rotación muñeca): "))
            
            target_pose = [theta1_t, theta2_t, d3_t, theta4_t]
            
            if not 0 <= d3_t <= 210:
                print(f"Advertencia: d3={d3_t}mm está fuera del rango de 0-210 mm.")

            N_STEPS = 40 # Número de pasos para la animación
            
            # Crear vectores de interpolación
            t1_steps = np.linspace(current_pose[0], target_pose[0], N_STEPS)
            t2_steps = np.linspace(current_pose[1], target_pose[1], N_STEPS)
            d3_steps = np.linspace(current_pose[2], target_pose[2], N_STEPS)
            t4_steps = np.linspace(current_pose[3], target_pose[3], N_STEPS)

            for i in range(N_STEPS):
                # 1. Limpiar los elementos anteriores del robot
                for handle in plot_handles:
                    handle.remove()
                
                # 2. Calcular y dibujar nueva pose
                t1_i = t1_steps[i]
                t2_i = t2_steps[i]
                d3_i = d3_steps[i]
                t4_i = t4_steps[i]
                
                plot_handles = plot_robot(ax, t1_i, t2_i, d3_i, t4_i)
                ax.set_title(f'Robot SCARA i4-850H (Moviendo...)')
                
                # 3. Forzar actualización del canvas
                plt.pause(0.01) 
            
            # Actualizar el título a la pose final
            ax.set_title(f'Robot SCARA i4-850H (θ1={theta1_t}°, θ2={theta2_t}°, d3={d3_t}mm, θ4={theta4_t}°)')
            plt.pause(0.1) # Pausa para ver el estado final
            
            # Actualizar la pose actual para el siguiente ciclo
            current_pose = target_pose
            
        except ValueError:
            print("Error: Por favor, ingrese solo números.")
            continue
        
        except KeyboardInterrupt:
            print("\nInterrupción detectada. Saliendo.")
            break
        
        cont = input("¿Desea ir a otra posición? (s/n): ").lower()
        if cont != 's':
            break
            
    print("Cerrando visualizador.")
    plt.ioff() # Desactivar modo interactivo
    plt.show() # Mantiene la ventana final abierta

# --- Ejecutar el programa ---
if __name__ == "__main__":
    main()