import trimesh
geom = trimesh.creation.cylinder(10,10)
geom.apply_translation((2, 200, -0.005))
geom.visual.face_colors = (.6, .6, .6)
tm = trimesh.load("assets\Typhoon.stl")
sc = trimesh.Scene()
sc.add_geometry(geom)
sc.add_geometry(tm)
sc.show()