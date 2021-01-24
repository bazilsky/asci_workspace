import cube_plot as c
import iris

path='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-bc244/L1/L1_ccn0.2_Cloud_condensation_nuclei_at_a_supersaturation_of_0.2000.nc'

cube=iris.load(path)
cube=cube[0]

c.plot(cube)
