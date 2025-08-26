#Box3
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib.animation import FuncAnimation

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()

# Use 3d view 
ax = plt.axes(projection = "3d")

def setaxis(x1, x2, y1, y2, z1, z2):
    # this function is used to fix the view to the values of input arguments
    # -----------------------------------------------------------------------
    # ARGUMENTS
    # x1, x2 -> numeric value
    # y1, y2 -> numeric value
    # y1, z2 -> numeric value
    # -----------------------------------------------------------------------
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)

def fix_system(axis_length, linewidth=5):
    # Fix system function 
    # Plots a 3D centered at [x,y,z] = [0,0,0]
    # -------------------------------------------------------------------
    # Arguments 
    # axis_length -> used to specify the length of the axis, in this case
    #                all axes are of the same length
    # -------------------------------------------------------------------
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length] 
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red', label="X axis",linewidth=linewidth)
    ax.plot3D(zp, y, zp, color='blue', label="Y axis",linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='green', label="Z axis",linewidth=linewidth)
    ax.legend()

def sind(t):
    # sind function
    # Computes the sin() trigonometric function in degrees
    # ----------------------------------------------------------------------
    # Arguments
    # t -> Numeric, angle in degrees. 
    # ----------------------------------------------------------------------
    res = np.sin(t*np.pi/180)
    return res

def cosd(t):
    # sind function
    # Computes the cos() trigonometric function in degrees
    # ----------------------------------------------------------------------
    # Arguments
    # t -> Numeric, angle in degrees. 
    # ----------------------------------------------------------------------
    res = np.cos(t*np.pi/180)
    return res

def RotX(t):
    Rx = np.array(([1,0,0],[0,cosd(t),-sind(t)],[0,sind(t),cosd(t)]))
    return Rx
def RotY(t):
    Ry = np.array(([cosd(t),0,sind(t)],[0,1,0],[-sind(t),0,cosd(t)]))
    return Ry
def RotZ(t):
    Rz = np.array(([cosd(t),-sind(t),0],[sind(t),cosd(t),0],[0,0,1]))
    return Rz

def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)

def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color = 'black'):
    drawScatter(p1)
    drawScatter(p2)
    drawScatter(p3)
    drawScatter(p4)
    drawScatter(p5)
    drawScatter(p6)
    drawScatter(p7)
    drawScatter(p8)

    drawVector(p1,p2,color = color)
    drawVector(p2,p3,color = color)
    drawVector(p3,p4,color = color)
    drawVector(p4,p1,color = color)
    drawVector(p5,p6,color = color)
    drawVector(p6,p7,color = color)
    drawVector(p7,p8,color = color)
    drawVector(p8,p5,color = color)
    drawVector(p4,p8,color = color)
    drawVector(p1,p5,color = color)
    drawVector(p3,p7,color = color)
    drawVector(p2,p6,color = color)

def drawScatter(point,color='black',marker='o'):
    ax.scatter(point[0],point[1],point[2],marker='o')

def rotate_box(p1,p2,p3,p4,p5,p6,p7,p8,axes=('z','x','y'), angles=(0,0,0)):
    rotations = {
        "x": RotX,
        "y": RotY,
        "z": RotZ
    }
    Rpoints = [p1,p2,p3,p4,p5,p6,p7,p8]
    for axis, angle in zip(axes, angles):
        if axis in rotations:
            R = rotations[axis](angle)
            Rpoints = [R.dot(p) for p in Rpoints]
    return tuple(Rpoints)


def animation_seq(p1,p2,p3,p4,p5,p6,p7,p8,
                  axes=('x','y','z'), angles=(0,0,0),
                  steps=30, show_original=True):
    """
    Anima en 3 fases: primero rota en axes[0], luego axes[1] (acumulado),
    y por último axes[2] (acumulado), con 'steps' frames por fase.
    Usa tu rotate_box sin modificarla.
    """
    # Estado inicial
    points_init = [p1,p2,p3,p4,p5,p6,p7,p8]

    # Construimos estados acumulados: [init, R1, R1*2, R1*2*3]
    states = [points_init]
    current = points_init
    for i in range(len(axes)):
        rotated = rotate_box(*current, axes=axes[:i+1], angles=angles[:i+1])
        states.append(list(rotated))   # guardar estado acumulado
        current = list(rotated)

    # Total de frames (incluimos un último frame para asegurar alpha=1)
    total_frames = steps * (len(states)-1)

    def interpolate(P0, P1, alpha):
        """Interpola linealmente entre dos configuraciones (8x3)."""
        P0 = np.array(P0, dtype=float)
        P1 = np.array(P1, dtype=float)
        return (1.0 - alpha) * P0 + alpha * P1

    def update(frame):
        """
        Llamada automáticamente por FuncAnimation con frame=0..total_frames.
        Decide en qué segmento estamos, calcula alpha y dibuja la caja.
        """
        ax.cla()
        setaxis(-15,15,-15,15,-15,15)
        fix_system(10,1)

        # Último frame
        if frame == total_frames:
            segment = len(states) - 2
            alpha = 1.0
        else:
            segment = frame // steps           # 0 -> 1er eje, 1 -> 2º eje, 2 -> 3er eje
            local_frame = frame % steps        # progreso dentro del segmento
            alpha = local_frame / steps        # 0.0 .. <1.0

        P0 = states[segment]
        P1 = states[segment+1]
        P = interpolate(P0, P1, alpha)

        if show_original:
            drawBox(*points_init, color='black')  # caja original
        drawBox(*P, color='red')                  # caja animada

    ani = FuncAnimation(fig, update, frames=total_frames+1, interval=50, repeat=False)
    plt.show()


# Set the view 
setaxis(-15,15,-15,15,-15,15)

# plot the axis
fix_system(10,1)

p1_init = [0,0,0]
p2_init = [7,0,0]
p3_init = [7,0,3]
p4_init = [0,0,3]
p5_init = [0,2,0]
p6_init = [7,2,0]
p7_init = [7,2,3]
p8_init = [0,2,3]

drawBox(p1_init, p2_init, p3_init, p4_init,
        p5_init, p6_init, p7_init, p8_init)

#Animacion eje por eje
animation_seq(p1_init, p2_init, p3_init, p4_init,
              p5_init, p6_init, p7_init, p8_init,
              axes=('x','y','z'), angles=(30,30,30),
              steps=40, show_original=True)

