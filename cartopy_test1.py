import iris
#import matplotlib.pyplot as plt 
import cartopy.crs as ccrs

#import mptoolkits
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
#matplotlib inline  
import warnings
import matplotlib.cbook

import matplotlib.colors as colors


path='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-bc046/L1/L1_ccn0.2_Cloud_condensation_nuclei_at_a_supersaturation_of_0.2000.nc'

cube=iris.load(path)
cube=cube[0]
#mean=cube.collapsed('model_level_number',iris.analysis.MEAN)
data=cube[0].data
lat=cube.coord('latitude').points
lon=cube.coord('longitude').points

#basemap correction 
lon=lon-180


fig = plt.figure(num=None, figsize=(12, 8) )
#fig=plt.figure()
#m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,resolution='c')
m = Basemap(projection='moll',lon_0=0,resolution='c')
x,y=m(*np.meshgrid(lon,lat))

m.drawcoastlines()
#m.fillcontinents(color='tan',lake_color='lightblue')
m.drawmapboundary(fill_color='lightblue')


#m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)
#m.colorbar(location='right')

m.pcolormesh(x,y,data,norm=colors.LogNorm(vmin=data.min(),vmax=data.max()),cmap=plt.cm.jet)
m.colorbar(location='right')

plt.title("Mollweide Projection");


plt.show()


"""
data=mean.data
lat=cube.coord('latitude').points
lon=cube.coord('longitude').points


ax=plt.axes(projection=ccrs.PlateCarree())

plt.contourf(lon, lat, data,60, transform=ccrs.PlateCarree())

ax.coastlines()
plt.show()
"""
