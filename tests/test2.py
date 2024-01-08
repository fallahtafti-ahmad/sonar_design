import trimesh
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

import io
tm = trimesh.load("assets\Typhoon.stl")
sc = trimesh.Scene()

# sc.add_geometry(tm)
# slice = tm.section(plane_origin=tm.centroid,
                    #  plane_normal=[0,0,1])

# sc.add_geometry(slice)
slice = trimesh.intersections.slice_mesh_plane(tm,plane_origin=tm.centroid,plane_normal=[0,0,-1])

sc.add_geometry(slice)
ang=[np.deg2rad(0),np.deg2rad(0),np.deg2rad(90)]
sc.set_camera(angles=tuple(ang))
png=sc.save_image(resolution=(800,600))

# sc.show(resolution=(800,600))
# sc.export("snap.jpg")
# image=Image.open(io.BytesIO(png))
image = img.imread(io.BytesIO(png))
# plt.imshow(image[:,:,0]==1)
# plt.show()
# print(image==1)
# image.show()
image2 =np.ones((600,900))
image2[:,50:850] = image[:,:,0]
""" Lattice Boltzmann Simulation """

# Simulation parameters
# Nx                     = 400    # resolution x-dir
# Ny                     = 100    # resolution y-dir
Ny,Nx = image2.shape
rho0                   = 100    # average density
tau                    = 0.6    # collision timescale
Nt                     = 4000   # number of timesteps
plotRealTime = True # switch on for plotting as the simulation goes along

# Lattice speeds / weights
NL = 9
idxs = np.arange(NL)
cxs = np.array([0, 0, 1, 1, 1, 0,-1,-1,-1])
cys = np.array([0, 1, 1, 0,-1,-1,-1, 0, 1])
weights = np.array([4/9,1/9,1/36,1/9,1/36,1/9,1/36,1/9,1/36]) # sums to 1

# Initial Conditions
F = np.ones((Ny,Nx,NL)) #* rho0 / NL
# F = image[:]
np.random.seed(42)
F += 0.01*np.random.randn(Ny,Nx,NL)
X, Y = np.meshgrid(range(Nx), range(Ny))
F[:,:,3] += 2 * (1+0.2*np.cos(2*np.pi*X/Nx*4))
rho = np.sum(F,2)
for i in idxs:
    F[:,:,i] *= rho0 / rho

# Cylinder boundary
# X, Y = np.meshgrid(range(Nx), range(Ny))
# cylinder = (X - Nx/4)**2 + (Y - Ny/2)**2 < (Ny/4)**2
cylinder = image2[:,:]<1
# Prep figure
fig = plt.figure(figsize=(4,2), dpi=80)

# Simulation Main Loop
for it in range(Nt):
    print(it)
    
    # Drift
    for i, cx, cy in zip(idxs, cxs, cys):
        F[:,:,i] = np.roll(F[:,:,i], cx, axis=1)
        F[:,:,i] = np.roll(F[:,:,i], cy, axis=0)
    
    
    # Set reflective boundaries
    bndryF = F[cylinder,:]
    bndryF = bndryF[:,[0,5,6,7,8,1,2,3,4]]

    
    # Calculate fluid variables
    rho = np.sum(F,2)
    ux  = np.sum(F*cxs,2) / rho
    uy  = np.sum(F*cys,2) / rho
    
    
    # Apply Collision
    Feq = np.zeros(F.shape)
    for i, cx, cy, w in zip(idxs, cxs, cys, weights):
        Feq[:,:,i] = rho * w * ( 1 + 3*(cx*ux+cy*uy)  + 9*(cx*ux+cy*uy)**2/2 - 3*(ux**2+uy**2)/2 )
    
    F += -(1.0/tau) * (F - Feq)
    
    # Apply boundary 
    F[cylinder,:] = bndryF
    
    
    # plot in real time - color 1/2 particles blue, other half red
    if (plotRealTime and (it % 10) == 0) or (it == Nt-1):
        plt.cla()
        ux[cylinder] = 0
        uy[cylinder] = 0
        vorticity = (np.roll(ux, -1, axis=0) - np.roll(ux, 1, axis=0)) - (np.roll(uy, -1, axis=1) - np.roll(uy, 1, axis=1))
        vorticity[cylinder] = np.nan
        vorticity = np.ma.array(vorticity, mask=cylinder)
        plt.imshow(vorticity, cmap='bwr')
        plt.imshow(~cylinder, cmap='gray', alpha=0.3)
        plt.clim(-.1, .1)
        ax = plt.gca()
        ax.invert_yaxis()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)	
        ax.set_aspect('equal')	
        plt.pause(0.001)
        

# Save figure
plt.savefig('latticeboltzmann.png',dpi=240)
plt.show()