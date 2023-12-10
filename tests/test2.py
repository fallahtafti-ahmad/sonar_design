import trimesh
from PIL import Image
import io
tm = trimesh.load("assets\Typhoon.stl")
sc = trimesh.Scene()

# sc.add_geometry(tm)
slice = tm.section(plane_origin=tm.centroid,
                     plane_normal=[0,0,1])

sc.add_geometry(slice)
png=sc.save_image(resolution=(800,600))
sc.show(resolution=(800,600))
image=Image.open(io.BytesIO(png))
image.show()
