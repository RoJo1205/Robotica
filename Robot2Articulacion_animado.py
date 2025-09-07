# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

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
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)
    ax.plot3D(zp, y, zp, color='green',linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='blue',linewidth=linewidth)

def mobile_frame(origin, x, y, z):
    # This function draws a movile frame 
    #--------------------------------------------------------------------
    xx = x[0]
    xy = x[1]
    xz = x[2]
    

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

def TRx(t):
    Rx = 0
    return Rx

def TRy(t):
    Ry = 0
    return Ry

def TRz(t):
    Rz = np.array(([cosd(t),-sind(t),0, 0],[sind(t),cosd(t),0, 0],[0,0,1, 0], [0,0,0,1]))
    return Rz

def TTx(t):
    Tx = 0
    return Tx

def TTy(t):
    Ty = 0
    return Ty

def TTz(t):
    Tz = np.array(([1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, t],[0,0,0,1]))
    return Tz

def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)


def drawMobileFrame(origin, x, y, z):
    x = [(origin[0] + x[0]), (origin[1] + x[1]), (origin[2] + x[2])]
    y = [(origin[0] + y[0]), (origin[1] + y[1]), (origin[2] + y[2])]
    z = [(origin[0] + z[0]), (origin[1] + z[1]), (origin[2] + z[2])]

    drawVector(x,origin, color="red")
    drawVector(y,origin, color="green")
    drawVector(z,origin, color="blue")

def getUnitaryVectorsFromMatrix(TM):
    x      = [TM[0][0], TM[1][0], TM[2][0]]
    y      = [TM[0][1], TM[1][1], TM[2][1]]
    z      = [TM[0][2], TM[1][2], TM[2][2]]
    origin = [TM[0][3], TM[1][3], TM[2][3]]

    return[x,y,z,origin]


l1 = 15
theta1 = 30

# Operation 1 - (Rotate the main origin 30 deg along the z axis)

n = 0
while n <= theta1:
    ax.cla()

    # Set the view 
    setaxis(-15,15,-15,15,-15,15)

    # plot the axis
    fix_system(10,linewidth=1)

    T1 = TRz(n)

    [x1,y1,z1,origin1] = getUnitaryVectorsFromMatrix(T1)

    drawMobileFrame(origin1, x1, y1, z1)

    # Operation 2 - Translate  the mobile ref along the x axis 

    # Compute the single Transformation matrix
    T2 = TTx(l1)

    # Operate both T1 and T2

    T12 = T1.dot(T2)

    [x2, y2, z2, origin2] = getUnitaryVectorsFromMatrix(T12)

    drawMobileFrame(origin2, x2, y2, z2)

    drawVector(origin2, origin1, color="black", linewidth=4)

    n = n+1

    plt.draw()
    plt.pause(0.001)







# show image.
plt.draw()
plt.show()


