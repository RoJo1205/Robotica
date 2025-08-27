#Box3
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib.animation import FuncAnimation

# Crear la figura y los ejes 3D
fig, ax = plt.subplots()
ax = plt.axes(projection="3d")

def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1, x2)
    ax.set_ylim3d(y1, y2)
    ax.set_zlim3d(z1, z2)
    ax.view_init(elev=30, azim=40)

def fix_system(axis_length, linewidth=5):
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length]
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color="red", label="X axis", linewidth=linewidth)
    ax.plot3D(zp, y, zp, color="blue", label="Y axis", linewidth=linewidth)
    ax.plot3D(zp, zp, z, color="green", label="Z axis", linewidth=linewidth)
    ax.legend()

def sind(t): return np.sin(np.radians(t))
def cosd(t): return np.cos(np.radians(t))

def RotX(t):
    return np.array([[1,0,0],[0,cosd(t),-sind(t)],[0,sind(t),cosd(t)]])
def RotY(t):
    return np.array([[cosd(t),0,sind(t)],[0,1,0],[-sind(t),0,cosd(t)]])
def RotZ(t):
    return np.array([[cosd(t),-sind(t),0],[sind(t),cosd(t),0],[0,0,1]])

def drawVector(p_fin, p_init=[0,0,0], color="black", linewidth=1):
    ax.plot3D([p_init[0], p_fin[0]],
              [p_init[1], p_fin[1]],
              [p_init[2], p_fin[2]],
              color=color, linewidth=linewidth)

def drawScatter(point, color="black", marker="o"):
    ax.scatter(point[0], point[1], point[2], marker=marker, color=color)

def drawBox(p1,p2,p3,p4,p5,p6,p7,p8, color="black"):
    for p in [p1,p2,p3,p4,p5,p6,p7,p8]:
        drawScatter(p)
    drawVector(p1,p2,color=color); drawVector(p2,p3,color=color)
    drawVector(p3,p4,color=color); drawVector(p4,p1,color=color)
    drawVector(p5,p6,color=color); drawVector(p6,p7,color=color)
    drawVector(p7,p8,color=color); drawVector(p8,p5,color=color)
    drawVector(p4,p8,color=color); drawVector(p1,p5,color=color)
    drawVector(p3,p7,color=color); drawVector(p2,p6,color=color)

def rotate_box(p1,p2,p3,p4,p5,p6,p7,p8, axes=("z","x","y"), angles=(0,0,0)):
    rotations = {"x": RotX, "y": RotY, "z": RotZ}
    Rpoints = [p1,p2,p3,p4,p5,p6,p7,p8]
    for axis, angle in zip(axes, angles):
        if axis in rotations:
            R = rotations[axis](angle)
            Rpoints = [R.dot(p) for p in Rpoints]
    return tuple(Rpoints)

def animation_diag(p1,p2,p3,p4,p5,p6,p7,p8,
                   axes=("x","y","z"), angles=(0,0,0),
                   steps=120, show_original=True):
    """
    Animación tipo robot: rota suavemente todos los ejes a la vez,
    interpolando los ángulos de forma continua.
    """
    points_init = [p1,p2,p3,p4,p5,p6,p7,p8]

    def update(frame):
        ax.cla()
        setaxis(-15,15,-15,15,-15,15)
        fix_system(10,1)

        alpha = frame / steps  # progreso [0,1]
        current_angles = [alpha * ang for ang in angles]

        rotated = rotate_box(*points_init, axes=axes, angles=current_angles)

        if show_original:
            drawBox(*points_init, color="black")  # caja original
        drawBox(*rotated, color="red")           # caja animada

    ani = FuncAnimation(fig, update, frames=steps+1, interval=50, repeat=False)
    plt.show()

# Setear vista y ejes
setaxis(-15,15,-15,15,-15,15)
fix_system(10,1)

# Caja inicial
p1_init = [0,0,0]
p2_init = [7,0,0]
p3_init = [7,0,3]
p4_init = [0,0,3]
p5_init = [0,2,0]
p6_init = [7,2,0]
p7_init = [7,2,3]
p8_init = [0,2,3]

drawBox(p1_init,p2_init,p3_init,p4_init,
        p5_init,p6_init,p7_init,p8_init)

# Animación suave (tipo robot)
animation_diag(p1_init,p2_init,p3_init,p4_init,
               p5_init,p6_init,p7_init,p8_init,
               axes=("x","y","z"), angles=(30,30,30),
               steps=120, show_original=True)
