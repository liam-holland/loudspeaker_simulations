import marimo

__generated_with = "0.25.1"
app = marimo.App()


@app.cell
def _():
    import electroacPy as ep
    from electroacPy import gtb
    import numpy as np

    return ep, gtb, np


@app.cell
def _(ep, np):
    # Frequency axis and system initialization
    frequency = np.arange(10,10000,1)
    system = ep.loudspeakerSystem(frequencyRange=frequency)
    return (system,)


@app.cell
def _(gtb):
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
    box.build("./mesh/automated_mesh.msh")
    return


@app.cell
def _(system):
    # Woofer parameters
    Re = 6.2        # Ohm
    Le = 1.2e-3     # H
    Bl = 16         # T.m
    Mms = 84.9e-3   # kg
    Cms = 560e-6    # m/N
    Rms = 2.35      # kg/s
    Sd = 508e-4     # m^2

    system.lem_driver("SB34", 1, Le, Re, Cms, Mms, Rms, Bl, Sd)

    # Midrange parameters
    Re = 6.2        # Ohm
    Le = 1.1e-3     # H
    Bl = 6.5         # T.m
    Mms = 11.8e-3   # kg
    Cms = 223e-6    # m/N
    Rms = 0.4      # kg/s
    Sd = 119e-4     # m^2

    system.lem_driver("MR16", 1, Le, Re, Cms, Mms, Rms, Bl, Sd)

    # Tweeter parameters
    Re = 3.0        # Ohm
    Le = 0.02e-3     # H
    Bl = 3.1         # T.m
    Mms = 0.44e-3   # kg
    Fs = 700        # Hz
    Cms = 223e-3    # m/N
    Rms = 0.084      # kg/s
    Qms = 2.1
    Sd = 9.6e-4     # m^2

    system.lem_driver("TW29", 1, Le, Re, Cms, Mms, Rms, Bl, Sd)
    return


@app.cell
def _():
    # Use the tools to investigate the 

    # system.driver["TW29"].sealedAlignment()
    # system.driver["TW29"].portedAlignment()
    return


@app.cell
def _(system):
    # Add enclosures

    system.lem_enclosure("ported_LF", 40e-3, 
                         Lp=35e-2, Sp=78.6e-4, 
                         Qab=120, Qal=30,
                         ref2bem=[1, 2], 
                         setDriver="SB34", Nd=1,
                         wiring="parallel")

    system.lem_enclosure("sealed_MF", 5.1e-3,
                         ref2bem=3, setDriver="MR16")

    return


@app.cell
def _(system):
    # plot data
    system.enclosure["ported_LF"].plotZe()
    system.enclosure["ported_LF"].plotXVA()
    return


@app.cell
def _(ep, system):
    ep.save("03_LEM_Recap", system)
    return


@app.cell
def _(system):
    system.study_acousticBEM("free-field","mesh/automated_mesh.msh",["ported_LF","TW29","sealed_MF"],domain="exterior")
    return


@app.cell
def _():
    from electroacPy.acousticSim.bem import boundaryConditions

    return (boundaryConditions,)


@app.cell
def _(boundaryConditions, system):
    bc = boundaryConditions()

    # What do these parameters do?
    bc.addInfiniteBoundary(normal="z", offset=-1)
    system

    system.study_acousticBEM("inf_ground","mesh/automated_mesh.msh",["ported_LF","TW29","sealed_MF"],domain="exterior",boundary_conditions=bc)
    return


@app.cell
def _(system):
    system.run()
    return


if __name__ == "__main__":
    app.run()
