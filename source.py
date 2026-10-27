import electroacPy as ep
from electroacPy import gtb

# Enclosure dimensions
Lx = 0.340
Ly = 0.6912
Lz = 0.3862

# initialize a shoebox object
box = gtb.shoebox(Lx, Ly, Lz, position="corner")

# add boundaries corresponding to drivers and port
box.addCircularBoundary("x", 72.5e-3, 0, 127e-3, 1, name="woofer")
box.addRectangularBoundary("x", 295.6e-3, -107.6e-3, 60e-3, 131e-3, 2, name="port")
box.addCircularBoundary("x", -223.1e-3, -70.6e-3, 61.5e-3, 3, name="midrange")
box.addCircularBoundary("x", -223.1e-3, 101.2e-3, 17.4e-3, 4, name="tweeter")

# build and save the mesh in the ../geo folder
box.build("../geo/mesh/automated_mesh.msh")