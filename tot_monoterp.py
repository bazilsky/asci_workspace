import iris
import numpy as np 
import matplotlib.pyplot as plt 
import iris.quickplot as qplt
import matplotlib.colors as colors

#filename = 'MEGAN-MACC_biogenic_C5H8_clim_2001-2010.nc'
filename = 'MEGAN-MACC_biogenic_Monoterp_clim_2001-2010.nc'
filepath = '/home/users/eeara/emis_files/'

cube = iris.load(filepath+filename)[0]

cube = cube.collapsed('time',iris.analysis.SUM)
cube = cube.collapsed('model_level_number',iris.analysis.SUM)
cube = cube.collapsed('latitude',iris.analysis.SUM)
cube = cube.collapsed('longitude',iris.analysis.SUM)

print 'Total emission flux in (kg.m-2.s-1) = ',cube.data
earth_surfarea = 510 * 1e6 * ((1e3)**2)  # 510 million km2 ... convert to meter
sec_in_year = 365*3600*24 
kg_to_tg = 1e-12
print 'Teragram of monoterp/yr = ', cube.data * earth_surfarea * sec_in_year * kg_to_tg

"""
print np.min(cube_tmean.data) # the minimum values of this array are equal to zero


ticks6 = [1e-12,5e-12,1e-11,5e-11,1e-10,5e-10,1e-9,5e-9,1e-8]
#qplt.contourf(cube_tmean[0,:,:],cmap = 'RdYlBu_r',norm=colors.LogNorm(vmin=1e-12,vmax=1e-8),vmin = 1e-12,vmax = 1e-8)
qplt.contourf(cube_tmean[0,:,:],cmap = 'RdYlBu_r',norm=colors.LogNorm(vmin=np.min(ticks6),vmax=np.max(ticks6)),levels = ticks6)

plt.gca().coastlines()
plt.show()
"""
