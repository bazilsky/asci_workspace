import numpy as np
from netCDF4 import Dataset
import glob as glb
import matplotlib.pyplot as plt
#import skill_metrics as sm
import cartopy.crs as ccrs
from mpl_toolkits.basemap import Basemap
import iris
import matplotlib


campaign = ['atom_1','atom_2','atom_3','atom_4']
col =['b','g','r','k']
col = ['#B5F2A7','#CAB182','#BBD4A6', '#FEBA02']
col = ['forestgreen','indianred','royalblue', '#FEBA02']
#col = ['b']
#col =['g','r','b','y']
atom1_path = '/group_workspaces/jasmin2/asci/eeara/atom/atom_batched/atom_1/'
atom2_path = '/group_workspaces/jasmin2/asci/eeara/atom/atom_batched/atom_2/'
atom3_path = '/group_workspaces/jasmin2/asci/eeara/atom/atom_batched/atom_3/'
atom4_path = '/group_workspaces/jasmin2/asci/eeara/atom/atom_batched/atom_4/'


atom_path = '/group_workspaces/jasmin2/asci/eeara/atom/atom_batched_2/'



atom1_files = glb.glob(atom1_path+'*.nc')
atom2_files = glb.glob(atom2_path+'*.nc')
atom3_files = glb.glob(atom3_path+'*.nc')
atom4_files = glb.glob(atom4_path+'*.nc')

plt.figure()
#campaign =['atom_1']
for i in range(len(campaign)):
    lat = []
    lon = []
    atom_files = glb.glob(atom_path+campaign[i]+'/*.nc')
    for j in atom_files:
        data = Dataset(j)
        lat_temp = np.asarray(data['latitude'])
        lon_temp = np.asarray(data['longitude'])
        lat = np.append(lat,lat_temp)
        lon = np.append(lon,lon_temp)
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=270))
    ax.stock_img()
    #plt.plot(lon, lat,
    #                          color=col[i],marker = 'o', alpha = 0.2,
    #                                  transform=ccrs.Geodetic(),
    #                                   )
    plt.plot(lon, lat,
                              color=col[i],marker = 'o', alpha = 0.2,linewidth = 0,
                                      transform=ccrs.Geodetic(),
                                       )
     
leg=plt.figlegend(['ATom 1','ATom 2','ATom 3','ATom 4'],loc='lower center',ncol = 4)
for l in leg.legendHandles:
    l.set_linewidth(5)
plt.show()

