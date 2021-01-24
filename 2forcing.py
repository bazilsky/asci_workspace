import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt
import numpy as np
#dir=''
#stash section1 517
cube1=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uax428-mt_results/All_time_steps/All_time_steps_m01s01i517_CLEAN-AIR_UPWARD_SW_FLUX_ON_LEVELS__.nc')
cube2=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uax428-mt_results/All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')
cube1=cube1[0]
cube2=cube2[0]
cube1=cube1.collapsed(['time'],iris.analysis.MEAN)
cube2=cube2.collapsed(['time'],iris.analysis.MEAN)

c1_data=cube2.data-cube1.data
latitude=cube2.coord('latitude').points
longitude=cube2.coord('longitude').points

alt1=iris.coords.DimCoord(latitude,standard_name='latitude')
alt2=iris.coords.DimCoord(longitude,standard_name='longitude')

c1=iris.cube.Cube(c1_data,dim_coords_and_dims=[(alt1,0),(alt2,1)],long_name='flux_preindustria;')



#cube1.units='W m-2'
#c1=cube2-cube1

cube3=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uax424_results/All_time_steps/All_time_steps/All_time_steps_m01s01i517_CLEAN-AIR_UPWARD_SW_FLUX_ON_LEVELS__.nc')
#note that cube 2 directory is somewhat different
cube4=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uax424_results/All_time_steps/All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')
cube3=cube3[0]
cube4=cube4[0]


cube3=cube3.collapsed(['time'],iris.analysis.MEAN)
cube4=cube4.collapsed(['time'],iris.analysis.MEAN)

c2_data=cube4.data-cube3.data
latitude=cube4.coord('latitude').points
longitude=cube4.coord('longitude').points

alt1=iris.coords.DimCoord(latitude,standard_name='latitude')
alt2=iris.coords.DimCoord(longitude,standard_name='longitude')

c2=iris.cube.Cube(c2_data,dim_coords_and_dims=[(alt1,0),(alt2,1)],long_name='flux_presentday')

#cube3.units='W m-2'
#c2=cube4-cube3


#cube1=cube1[0]
#cube2=cube2[0]

#c1=c1.collapsed(['time'],iris.analysis.MEAN)
#c2=c2.collapsed(['time'],iris.analysis.MEAN)

#net_climate_effect

diff=(c2-c1)
#diff.data=np.absolute(diff.data)
qplt.contourf(diff)
plt.title('direct aerosol radiative effect: (present_day - pre_industrial).... uax424')
plt.gca().coastlines()
plt.savefig('fig3.pdf')
plt.show()


