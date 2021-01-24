import iris
import numpy as np
import matplotlib.pyplot as plt


mpath='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-ax424/All_time_steps/All_time_steps_m01s34i072_mass_fraction_of_sulfur_dioxide_in_air.nc'

cube=iris.load(mpath)
cube=cube[0]

alt_data=cube.coord('altitude').points
model_level_number=cube.coord('model_level_number').points
latitude=cube.coord('latitude').points
longitude=cube.coord('longitude').points


alt1=iris.coords.DimCoord(model_level_number,long_name='model_level_number')
alt2=iris.coords.DimCoord(latitude,standard_name='latitude')
alt3=iris.coords.DimCoord(longitude,standard_name='longitude')

newcube=iris.cube.Cube(alt_data,dim_coords_and_dims=[(alt1,0),(alt2,1),(alt3,2)],standard_name='altitude')

mean1=newcube.collapsed('latitude',iris.analysis.MEAN)
mean2=mean1.collapsed('longitude',iris.analysis.MEAN)

mean2_data=mean2.data
z=mean2.coord('model_level_number').points

mean2_data=mean2_data/1000
#plt.plot(z,mean2_data,'r*')
#plt.show()



