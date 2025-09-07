# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()
ax = plt.axes(projection = "3d")

def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)

#para imprimir la leyenda una sola vez
legend_done = False

def fix_system(axis_length, linewidth=5):
    global legend_done
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length]
    z = [-axis_length, axis_length]
    zp = [0,0]

    if not legend_done:
        # primera vez: añadir labels y crear la leyenda
        ax.plot3D(x, zp, zp, color='red', linewidth=linewidth, label='Eje X')
        ax.plot3D(zp, y, zp, color='green', linewidth=linewidth, label='Eje Y')
        ax.plot3D(zp, zp, z, color='blue', linewidth=linewidth, label='Eje Z')
        ax.legend()
        legend_done = True
    else:
        # dibujar sin leyenda para que no se duplique
        ax.plot3D(x, zp, zp, color='red', linewidth=linewidth, label='_nolegend_')
        ax.plot3D(zp, y, zp, color='green', linewidth=linewidth, label='_nolegend_')
        ax.plot3D(zp, zp, z, color='blue', linewidth=linewidth, label='_nolegend_')


def sind(t):
    return np.sin(np.pi/180*t)

def cosd(t):
    return np.cos(np.pi/180*t)


def TRx(t):
    Rx = np.array(([1,0,0,0],[0,cosd(t),-sind(t),0],[0,sind(t),cosd(t),0],[0,0,0,1]))
    return Rx

def TRy(t):
    Ry = np.array(([cosd(t),0,sind(t),0],[0,1,0,0],[-sind(t),0,cosd(t),0],[0,0,0,1]))
    return Ry

def TRz(t):
    Rz = np.array(([cosd(t),-sind(t),0, 0],[sind(t),cosd(t),0, 0],[0,0,1, 0], [0,0,0,1]))
    return Rz

def TTx(t):
    Tx = np.array(([1, 0, 0, t],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]))
    return Tx

def TTy(t):
    Ty = np.array(([1, 0, 0, 0],[0, 1, 0, t],[0, 0, 1, 0],[0, 0, 0, 1]))
    return Ty

def TTz(t):
    Tz = np.array(([1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, t],[0,0,0,1]))
    return Tz


def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    line = ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)[0]
    return line  

def drawMobileFrame(origin, x, y, z):
    x_line = ax.plot3D([origin[0], origin[0]+x[0]],[origin[1], origin[1]+x[1]],[origin[2], origin[2]+x[2]], color="red")[0]
    y_line = ax.plot3D([origin[0], origin[0]+y[0]],[origin[1], origin[1]+y[1]],[origin[2], origin[2]+y[2]], color="green")[0]
    z_line = ax.plot3D([origin[0], origin[0]+z[0]],[origin[1], origin[1]+z[1]],[origin[2], origin[2]+z[2]], color="blue")[0]
    return [x_line, y_line, z_line]
    
def getUnitaryVectorsFromMatrix(TM):
    x      = [TM[0][0], TM[1][0], TM[2][0]]
    y      = [TM[0][1], TM[1][1], TM[2][1]]
    z      = [TM[0][2], TM[1][2], TM[2][2]]
    origin = [TM[0][3], TM[1][3], TM[2][3]]
    return [x,y,z,origin]

# Parametros del robot articulado
theta1 = 30
theta2 = 45
l1 = 4
theta3 = -45
l2 = 4
theta4 = 55
l3 = 3

# Lista para guardar las líneas de frames móviles
frames = []
# Lista para guardar los vectores finales 
final_vectors = []


# Operation 1 - Rotación en Y
n=0
while n <= theta1:
    for line in frames: line.remove()
    frames = []
    setaxis(-15,15,-15,15,-15,15)
    fix_system(10, linewidth=1)
    T1 = TRy(n)
    [x1,y1,z1,origin1] = getUnitaryVectorsFromMatrix(T1)
    frames = drawMobileFrame(origin1, x1, y1, z1)
    n += 1
    plt.draw()
    plt.pause(0.001)

# Operation 2 - Rotación Z + Traslación X
n=0
last_vec = None  # guarda el último vector dentro de bucle
while n <= theta2:
    for line in frames: line.remove()
    frames = []
    if last_vec: last_vec.remove()  #borra el vector anterior del bucle
    setaxis(-15,15,-15,15,-15,15)
    fix_system(10, linewidth=1)
    T2 = TRz(n)
    T12 = T1@T2
    [x2,y2,z2,origin2] = getUnitaryVectorsFromMatrix(T12)
    frames = drawMobileFrame(origin2, x2, y2, z2)

    T3 = TTx(l1)
    T123 = T12@T3
    [x3,y3,z3,origin3] = getUnitaryVectorsFromMatrix(T123)
    frames += drawMobileFrame(origin3, x3, y3, z3)

    # ← vector del eslabón, guardado en last_vec
    last_vec = drawVector(origin3, origin2, color="black", linewidth=4)

    n += 1
    plt.draw()
    plt.pause(0.001)

# al terminar el bucle, guardamos el último vector en lista final
final_vectors.append(last_vec)

# Operation 3 - Rotación Z + Traslación X
n=0
paso = -1  # para sentido horario
last_vec = None 
while n >= theta3:
    for line in frames: line.remove()
    frames = []
    if last_vec: last_vec.remove()  
    setaxis(-15,15,-15,15,-15,15)
    fix_system(10, linewidth=1)

    T4 = TRz(n)
    T1234 = T123@T4
    [x4,y4,z4,origin4] = getUnitaryVectorsFromMatrix(T1234)
    frames = drawMobileFrame(origin4, x4, y4, z4)

    T5 = TTx(l2)
    T12345 = T1234@T5
    [x5,y5,z5,origin5] = getUnitaryVectorsFromMatrix(T12345)
    frames += drawMobileFrame(origin5, x5, y5, z5)

    last_vec = drawVector(origin5, origin4, color="black", linewidth=4)

    n += paso
    plt.draw()
    plt.pause(0.001)

# al terminar el bucle, guardamos el último vector en lista final
final_vectors.append(last_vec)

# Operation 4 - Rotación Z + Traslación X
n=0
last_vec = None 
while n <= theta4:
    for line in frames: line.remove()
    frames = []
    if last_vec: last_vec.remove()  
    setaxis(-15,15,-15,15,-15,15)
    fix_system(10, linewidth=1)

    T6 = TRz(n)
    T123456 = T12345@T6
    [x6,y6,z6,origin6] = getUnitaryVectorsFromMatrix(T123456)
    frames = drawMobileFrame(origin6, x6, y6, z6)

    T7 = TTx(l3)
    T1234567 = T123456@T7
    [x7,y7,z7,origin7] = getUnitaryVectorsFromMatrix(T1234567)
    frames += drawMobileFrame(origin7, x7, y7, z7)

    last_vec = drawVector(origin7, origin6, color="black", linewidth=4)

    n += 1
    plt.draw()
    plt.pause(0.001)


final_vectors.append(last_vec)

plt.draw()
plt.show()
