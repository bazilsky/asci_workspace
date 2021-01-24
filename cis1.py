


from cis import read_data, read_data_list, get_variables
import numpy as np
import iris.analysis
import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt

dir_file='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-ba850/L1/'
#filename='L1_rad_accsol_Radius_of_mode_accsol.nc'
#filename='L1_air_density_Density of air.nc'
filename='L1_ccn0.2_Cloud_condensation_nuclei_at_a_supersaturation_of_0.2000.nc'
filename=dir_file+filename

#----------------------------------------------------

var=get_variables(filename)
#output from cis should be in a set form 
"""
#var_name=[]
#for i in var:
#    var_name=np.append(var_name,i)

"""

var=list(var)
data0=read_data(filename,var[0])
mean=data0.collapsed(['latitude','longitude'],iris.analysis.MEAN)
mean2=data0.collapsed(['model_level_number'],iris.analysis.MEAN)
mean2.plot(yaxis='latitude')
plt.show()
time.sleep(20)
plt.close()

#print data0.info()
#print var

#----------------------------------------------------

"""
cube=iris.load(filename)
cube=cube[0].collapsed('model_level_number',iris.analysis.MEAN)

qplt.contourf(cube,25)
plt.gca().coastlines()
plt.show()
"""






