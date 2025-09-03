# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from matplotlib.animation import FuncAnimation

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()

# Use 3d view 
ax = plt.axes(projection = "3d")


def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)


def fix_system(axis_length, linewidth=5):
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length] 
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)
    ax.plot3D(zp, y, zp, color='blue',linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='green',linewidth=linewidth)
    

def sind(t):
    res = np.sin(t*np.pi/180)
    return res

def cosd(t):
    res = np.cos(t*np.pi/180)
    return res


def RotZ(t):
    Rz = np.array(([cosd(t),-sind(t),0],
                   [sind(t), cosd(t),0],
                   [0,0,1]))
    return Rz


def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)


def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='black'):
    drawScatter(p1,color=color)
    drawScatter(p2,color=color)
    drawScatter(p3,color=color)
    drawScatter(p4,color=color)
    drawScatter(p5,color=color)
    drawScatter(p6,color=color)
    drawScatter(p7,color=color)
    drawScatter(p8,color=color)

    drawVector(p1,p2,color=color)
    drawVector(p2,p3,color=color)
    drawVector(p3,p4,color=color)
    drawVector(p4,p1,color=color)
    drawVector(p5,p6,color=color)
    drawVector(p6,p7,color=color)
    drawVector(p7,p8,color=color)
    drawVector(p8,p5,color=color)
    drawVector(p4,p8,color=color)
    drawVector(p1,p5,color=color)
    drawVector(p3,p7,color=color)
    drawVector(p2,p6,color=color)


def drawScatter(point,color='black',marker='o'):
    ax.scatter(point[0],point[1],point[2],marker='o',color=color)


def move_Box(p1,p2,p3,p4,p5,p6,p7,p8, delta_x = 0, delta_y = 0, delta_z = 0):
    p1 = [p1[0], p1[1], p1[2], 1]
    p2 = [p2[0], p2[1], p2[2], 1]
    p3 = [p3[0], p3[1], p3[2], 1]
    p4 = [p4[0], p4[1], p4[2], 1]
    p5 = [p5[0], p5[1], p5[2], 1]
    p6 = [p6[0], p6[1], p6[2], 1]
    p7 = [p7[0], p7[1], p7[2], 1]
    p8 = [p8[0], p8[1], p8[2], 1]

    Translation_Matrix = np.array(([1,0,0, delta_x],
                                   [0, 1, 0, delta_y],
                                   [0, 0, 1, delta_z],
                                   [0, 0, 0, 1]))

    p1_t = Translation_Matrix.dot(p1)[:3]
    p2_t = Translation_Matrix.dot(p2)[:3]
    p3_t = Translation_Matrix.dot(p3)[:3]
    p4_t = Translation_Matrix.dot(p4)[:3]
    p5_t = Translation_Matrix.dot(p5)[:3]
    p6_t = Translation_Matrix.dot(p6)[:3]
    p7_t = Translation_Matrix.dot(p7)[:3]
    p8_t = Translation_Matrix.dot(p8)[:3]

    return [p1_t,p2_t, p3_t, p4_t, p5_t, p6_t, p7_t, p8_t]


# Set the view 
setaxis(-15,15,-15,15,-15,15)

# plot the axis
fix_system(10,linewidth=1)

p1_init = [0,0,0]
p2_init = [7,0,0]
p3_init = [7,0,3]
p4_init = [0,0,3]
p5_init = [0,2,0]
p6_init = [7,2,0]
p7_init = [7,2,3]
p8_init = [0,2,3]

# === ANIMACIÓN ===
dx, dy, dz = 5, 5, 2   # desplazamiento deseado
frames = 50            # pasos de interpolación
points_init = [p1_init, p2_init, p3_init, p4_init,
               p5_init, p6_init, p7_init, p8_init]

def update(frame):
    ax.cla()
    setaxis(-15,15,-15,15,-15,15)
    fix_system(10,linewidth=1)

    # Dibujar la caja original siempre en negro
    drawBox(*points_init, color='black')

    # Interpolación para la animada
    t = frame / frames
    moved = move_Box(*points_init, delta_x=dx*t, delta_y=dy*t, delta_z=dz*t)

    # Dibujar la caja en movimiento en rojo
    drawBox(*moved, color='red')

ani = FuncAnimation(fig, update, frames=frames+1, interval=100, repeat=False)

plt.show()
