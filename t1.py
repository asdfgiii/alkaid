# 先做个垃圾出来
# I really can't.
import os
import math
import numpy as np
import random
import matplotlib
import underworld as uw
from underworld import function as fn
import underworld.visualisation as vis

# 读取和保存路径
'''
outputPath = os.path.join(os.path.abspath("."),"t1/")
inputPath  = outputPath
if uw.mpi.rank==0:
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
uw.mpi.barrier()
'''
# 变量 几何形态 ？？？
s_age = 100 #Ma
xm = 10000.0*1e3 #x轴最远端位置
model_depth = 2800*1e3 # ？？？这么大数
xb = 0.0 #x轴近端位置
ym = 0.0 #y轴远端位置
yb = -model_depth #y轴近端位置
vplate = 5.0 #cm/yr

resx=int(xm/1e3/50*1/1)
resy=int((ym-yb)/1e3/50*1/1) #瞎写就so happy ^ ^
# print(resx,resy)

mesh = uw.mesh.FeMesh_Cartesian(elementRes = (resx, resy),
                                minCoord = (xb, yb),
                                maxCoord = (xm, ym))

velocityField = mesh.add_variable(nodeDofCount = 2)
pressureField = mesh.add_variable(nodeDofCount = 1)
temperatureField = mesh.add_variable(nodeDofCount = 1)
temperatureDotField = mesh.add_variable(nodeDofCount = 1)
# viscosityField = mesh.add_variable(nodeDofCount = 1)
# densityField = mesh.add_variable(nodeDofCount = 1)

velocityField.data[:] = [0., 0.]
pressureField.data[:] = 0.
temperatureField.data[:] = 0.
temperatureDotField.data[:] = 0.
# viscosityField.data[:] = 0.

swarm = uw.swarm.Swarm(mesh = mesh, particleEscape = True)
swarm.allow_parallel_nn=True
# By default, parallel nearest neighbour search is disabled
# as consistent results are not currently guaranteed. 
# Set this attribute to True to allow parallel NN. 并行最近邻搜索？
materialVariable = swarm.add_variable(dataType = 'int', count = 1)
# densitySwarm = swarm.add_variable(dataType = 'double', count=1 )
# viscositySwarm = swarm.add_variable(dataType = 'double', count=1 ) #粘度和密度变量为什么同时有mesh和swarm？
# timeSwarm?
layout = uw.swarm.layouts.PerCellSpaceFillerLayout(swarm, particlesPerCell = 20)
swarm.populate_using_layout(layout)

# 常数设置
alpha = 3.0e-5 # 地表热膨胀系数 K-1
kappa = 1.0e-6 # diffusivity
rho = 3416.0 # 参考密度 kg/m3
g = 9.8
tp0 = 1573.0 # potential temperature K
cp = 1250.0 # Jkg-1K-1
# ?缺温度压力？

def alpha_depth(depth):
    y = # from 3 × 10−5 K−1 at the surface to 1 × 10−5 K−1 at a depth of 2800 km

def T_profile(g,tp0):
    depth = np.arrange(2781) # 从0-2780，壳幔边界以上100km
    d_depth = depth[1] - depth[0]
    t = depth*0. + tp0
    p = 0.
    for i in range(2781):
        d_t = # 关于d_depth和alpha_depth？？？
        t[i+1] = t[i] + d_t
        
# 省略一些重要东西
mantleIndex = 0
crustIndex = 1
weakIndex = 2
materialVariable.data[:] = mantleIndex
radius = 800.0 # 弧对应半径 不要紧，瞎设的
for index in range(len(swarm.particleCoordinates.data)):
    coord = swarm.particleCoordinates.data[index][:]
    x = coord[0]/1000.0
    z = -coord[1]/1000.0
    if xm/1000/2 - 3000<x<xm/1000/2 and z<10:
        materialVariable.data[index] = weakIndex
    elif (radius-10)**2<(x-xm/1000/2)**2 + (radius-z)**2<radius**2 and x>xm/1000/2 and z<30:
        materialVariable.data[index] = weakIndex
    elif z<30:
        materialVariable.data[index] = crustIndex
    elif (radius-30)**2<(x-xm/1000/2)**2 + (radius-z)**2<radius**2 and x>xm/1000/2 and z<500:
        materialVariable.data[index] = crustIndex
    else:
        materialVariable.data[index] = mantleIndex

materialfigure = vis.Figure(figsize = (800,400))
materialfigure.append(vis.objects.Surface(mesh, materialVariable, onMesh = False))
materialfigure.show()
# 坏了，图幅设太大了

# 温度场