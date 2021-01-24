import iris,glob,datetime, time,re,sys
import numpy as np
import scipy as sp
import numpy.ma as ma
import matplotlib.pyplot as plt
import iris.coord_categorisation
import cf_units
import iris.quickplot as qplt

from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors


iris.FUTURE.cell_datetime_objects=True


trial1=iris.cube.CubeList()
trial2=iris.cube.CubeList()

path = '/group_workspaces/jasmin2/gassp/eeara/CARIBIC/'#ANANTH

mpath1='/group_workspaces/jasmin2/gassp/eeara/model_runs/cats_ukesm_2014/L1/'
#mpath2='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-bc244/L1/'

alt_path='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-bc046/L1/'
#mpath2='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-bc244/L1/'
cutoff=2 # this is a radius...12nm is a diameter!!

altitude_path=alt_path+'L1_rad_accsol_Radius_of_mode_accsol.nc'
cube=iris.load(altitude_path)
cube=cube[0]
alt_data=cube.coord('altitude').points
alt_data=alt_data[:,1,1]
alt_data=alt_data/1000

def find_nearest_index(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def cat_func_lat(position):
    return asl.coord('latitude').nearest_neighbour_index(position)

def cat_func_lon(position):
    return asl.coord('longitude').nearest_neighbour_index(position)    

def lognormal_cummulative(N,r,rbar,sigma):
    total=(N/2)*(1+sp.special.erf(np.log(r/rbar)/np.sqrt(2)/np.log(sigma)))
    return total

sigma=[1.59,1.59,1.40,2.0,1.59,1.59,2.0]

pref=1.013e5
tref=293.0
zboltz=1.3807e-23
staird=pref/(tref*287.058) 


def get_model_data(indx,alt,num,mpath): #add variable for cutoff and do logcumtor (easy!)

    model_aird = iris.load(mpath+'L1_air_density_Density of air.nc')
    model_aird = model_aird[0]
    #model_aird = iris.load_cube(mpath+'L1_air_density_Density of air.nc') #kgm-3
    
    
    model_acc = iris.load(mpath+'L1_n_accsol_number_fraction_of_total_accumulation_mode_soluble_aerosol_in_air.nc')#particles/m3
    model_nuc = iris.load(mpath+'L1_n_nucsol_number_fraction_of_total_nucleation_mode_soluble_aerosol_in_air.nc')
    model_aitins = iris.load(mpath+'L1_n_aitins_number_fraction_of_total_aitken_mode_insoluble_aerosol_in_air.nc')
    model_ait = iris.load(mpath+'L1_n_aitsol_number_fraction_of_total_aitken_mode_soluble_aerosol_in_air.nc')
    model_cor = iris.load(mpath+'L1_n_corsol_number_fraction_of_total_coarse_mode_soluble_aerosol_in_air.nc')
    model_nucrad = iris.load(mpath+'L1_rad_nucsol_Radius_of_mode_nucsol.nc')
    model_aitrad = iris.load(mpath+'L1_rad_aitsol_Radius_of_mode_aitsol.nc')
    model_aitirad = iris.load(mpath+'L1_rad_aitins_Radius_of_mode_aitins.nc')

    model_acc=model_acc[0]
    model_nuc=model_nuc[0]
    model_aitins=model_aitins[0]
    model_ait=model_ait[0]
    model_cor=model_cor[0]
    model_nucrad=model_nucrad[0]
    model_aitrad=model_aitrad[0]
    model_aitirad=model_aitirad[0]



    model_acc_stp = model_acc*staird/model_aird
    model_ait_stp = model_ait*staird/model_aird
    model_cor_stp = model_cor*staird/model_aird
    model_nuc_stp = model_nuc*staird/model_aird
    model_aitins_stp = model_aitins*staird/model_aird


    model_nuc_thl = model_nuc_stp - model_nuc_stp.copy(lognormal_cummulative(model_nuc_stp.data, cutoff*1.0e-9, model_nucrad.data, sigma[0]))
    model_ait_thl = model_ait_stp - model_ait_stp.copy(lognormal_cummulative(model_ait_stp.data, cutoff*1.0e-9, model_aitrad.data, sigma[1]))
    model_aitins_thl = model_aitins_stp - model_aitins_stp.copy(lognormal_cummulative(model_aitins_stp.data, cutoff*1.0e-9, model_aitirad.data, sigma[4]))
    
    model_n = model_nuc_thl+model_ait_thl+model_aitins_thl+model_acc_stp+model_cor_stp
    #print model_n
    #model_n = model_n.collapsed('time',iris.analysis.MEAN)
    model_n = model_n/1000000
    print model_n
    #model
    model_n.long_name='Particle Number Concentration at STP (cm-3)'
    model_n.units='cm-3'

    slice1=model_n[indx,:,:]
    return slice1

def file_save(slice1,num,alt):
    data=slice1.data
    lon=slice1.coord('longitude').points
    lat=slice1.coord('latitude').points
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
    plt.title('CAT_SCOTT - Number Conc (cm-3) || ALTITUDE = '+str(alt)+'km');

    file_name='file'+str(num)+'.png'
    #plt.show()
    plt.savefig(file_name)
    #return data,lat,new_lon 
    
    
    
    #...........................................................
def file_save2(slice1,num,alt):
    plt.figure()
    qplt.contourf(slice1,25)
    plt.gca().coastlines()
    plot_name='(new-old/old)*100--uax424 (%) || ALT = '+str(alt)+'km'
    print '\n',plot_name
    plt.title(plot_name)
    file_name='file'+str(num)+'.png'
    plt.show()
    #plt.savefig(file_name)
    
    
    #plt.show()
    #return slice1
    #model_n = model_nuc_stp+model_ait_stp+model_aitins_stp+model_acc_stp+model_cor_stp
   # model_n=model_nuc+model_ait+model_aitins+model_acc+model_cor



var1=[]
var2=[]
var3=[]
var4=[]
var5=[]
var6=[]
var7=[]
var8=[]
#f=plt.figure()
indx=[10,20,30,35,40,45,50,55]
alt=[3.4,5.1,7.8,9.8,12.1,14.8,18,21.7]




#for i in range(1):
for i in range(len(alt_data)):
    print '\n File STARTED '
    #if i==0:
    if i%3==0:
        new1=get_model_data(i,alt_data[i],i,mpath1)
 #       old1=get_model_data(i,alt_data[i],i,mpath2)
 #       diff=((new1-old1)/old1)*100
      #  data, lat, lon = file_save(new1,i,alt_data[i])
        file_save(new1,i,alt_data[i])
        """
        data=new1.data
        lon=new1.coord('longitude').points
        lat=new1.coord('latitude').points
        lon=lon-180    #basemap correction 
        fig = plt.figure(num=None, figsize=(12, 8) )
        #m = Basemap(projection='moll',lon_0=0, resolution ='c')
        
        m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,resolution='c')
        x,y=m(*np.meshgrid(lon,lat))
        m.drawcoastlines()
        m.drawmapboundary(fill_color='lightblue')

        m.pcolormesh(x,y,data,norm=colors.LogNorm(vmin=data.min(),vmax=data.max()),cmap=plt.cm.jet)
        m.colorbar(location='right')
        plt.title("Mollweide Projection");
        plt.show()
        """
        print new1       
        


    #qplt.contourf(model_cube)
    #contour = qplt.contour(model_cube)
    #plt.gca().coastlines()
    #plt.clabel(contour,inline=False)
    #plt.show()
#print model_n
