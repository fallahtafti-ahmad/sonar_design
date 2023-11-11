import trimesh as tm
import numpy as np
vertices=[]
r=1
hs=-5
he=5
s=-60/180*np.pi
e=60/180*np.pi
faces=[]
for z in np.linspace(hs,he,100):
    for tetha in np.linspace(s,e,100):
        x=r*np.sin(tetha)
        y=r*np.cos(tetha)
        vertices.append([x,y,z])
        faces.append([0,1,2])
print(len(vertices))
# mesh=tm.creation.capsule(height=5)
mesh = tm.Trimesh(vertices=[[0, 0, 0], [0, 0, 1], [0, 1, 0],[1,0,0]],
                       faces=[[0, 1, 2],[0, 1, 3],[0, 2, 3],[1,3,2]])
# mesh = tm.Trimesh(vertices=vertices,faces=faces)
mesh.show()