import iris
import cf
import cfplot as cfp

filename='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-bc046/L1/L1_ccn0.2_Cloud_condensation_nuclei_at_a_supersaturation_of_0.2000.nc'
cube1=iris.load(filename)
cube2=cf.read(filename)
print cube1
print '\n CUBE2....\n ', cube2
