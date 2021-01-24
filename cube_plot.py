import iris
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors

iris.FUTURE.cell_datetime_objects=True

# note that this plotting function is N96 

def plot(cube):
    
    cube=cube.collapsed('model_level_number', iris.analysis.MEAN)
     
    data=cube.data
    lon=cube.coord('longitude').points
    lat=cube.coord('latitude').points
  #  new_lon=[]

    
#..........

    new_lon=[]
    for k in range(len(lon)):
        if lon[k]>180:
            #temp=lon[k]
            temp=lon[k]-360
            new_lon=np.append(new_lon,temp)
        else:
            new_lon=np.append(new_lon,lon[k])
    #lon=lon-180    #basemap correction 
    #new_lon=temp

#..............basemap requires lat and lon to be in increasing order
    
    data_1=data[:,0:96]
    data_2=data[:,96:]
    data_21=np.hstack((data_2,data_1))

    new_lon_1=new_lon[0:96]
    new_lon_2=new_lon[96:]
    new_lon_21 = np.hstack((new_lon_2, new_lon_1))


    data_final=data_21
    new_lon_final=new_lon_21
#..............


    fig = plt.figure(num=None, figsize=(12, 8) )
   # m = Basemap(projection='moll',lon_0=0, resolution ='c')
    
    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,resolution='c')
    x,y=m(*np.meshgrid(new_lon_final,lat))
    m.drawcoastlines()
    m.drawmapboundary(fill_color='lightblue')

    limits=[pow(10,0),pow(10,1),pow(10,2),pow(10,3),pow(10,4),pow(10,5),pow(10,6)]

    m.pcolormesh(x,y,data_final,norm=colors.LogNorm(vmin=pow(10,0),vmax=pow(10,6)),cmap=plt.cm.jet)
   # m.pcolormesh(x,y,data_final,norm=colors.LogNorm(vmin=data.min(),vmax=data.max()),cmap=plt.cm.jet)
  
    m.colorbar(location='right')
    
    #plt.title('Number_concentration  || ALTITUDE = ');

    #file_name='file'+str(num)+'.png'
    plt.show()
    #plt.savefig(file_name)
    #return data,lat,new_lon 
    

