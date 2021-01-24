import iris
import re
import matplotlib.pyplot as plt
import scipy as sp
import iris.quickplot as qplt
import numpy as np
import glob

from mpl_toolkits.basemap import Basemap

path='/group_workspaces/jasmin2/gassp/eeara/CARIBIC/'
mpath='/group_workspaces/jasmin2/gassp/eeara/new_uax424_results/L1/'
files=glob.glob(path+'*.nc')
#files=['/group_workspaces/jasmin2/gassp/eeara/CARIBIC/CPC_CARIBIC2_data_20150114_491_MUC_GRU_10s_V12.nc','/group_workspaces/jasmin2/gassp/eeara/CARIBIC/CPC_CARIBIC2_data_20150115_492_GRU_MUC_10s_V12.nc']

#files=['/group_workspaces/jasmin2/gassp/eeara/CARIBIC/CPC_CARIBIC2_data_20150114_491_MUC_GRU_10s_V12.nc']

#map=Basemap(projection='mill',lat_0=0, lon_0=0)
#map.drawmapboundary(fill_color='white')
#map.fillcontinents(color='coral', lake_color='white')
#map.drawcoastlines()
#map.drawparallels(np.arange(-90.,91.,20.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5')
#map.drawmeridians(np.arange(0., 360., 30.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5')
#plt.figure(figsize=(10,10))
count =1
flag=0
for filename in files:
    #filename=path+'CPC_CARIBIC2_data_20150715_515_MUC_LAX_10s_V06.nc'
    cube=iris.load(filename)
    if re.search('FRA CAN', cube[0].attributes['Environment'])!=None or re.search('CAN FRA',cube[0].attributes['Environment'])!=None:
        r=cube[0].attributes['Time_Coverage_Start'][5:7]
        #print cube[0].attributes['Time_Coverage_Start'] ,'\n'
        if r=='03' or r=='04' or r=='05':
            if r=='03':
                flag=3
            if r=='04':
                flag=4
            if r=='05':
                flag=5
            
            print count,'\n' 
            count = count + 1
    #print cube
            n12=cube[0]
            lat=cube[7]
            lon=cube[8]
            alt=cube[6]
     
            time=n12.coord('time').points
    
    
            n12_data=n12.data
            latitude=lat.data
            longitude=lon.data
            altitude=alt.data
            break
            #plt.plot(time,altitude)
            
            #break
       #plt.plot(time,longitude)
        #plt.plot(time,altitude)
   # map=Basemap(projection='mill',lat_0=0,lon_0=0)
   # map.drawmapboundary(fill_color='aqua')
   # map.fillcontinents(color='coral', lake_color='aqua')
   # map.drawcoastlines()
    #x,y=map(longitude,latitude)
    #plt.title('Caribic_flight_tracks')
    #map.scatter(x,y,marker='o',color='b',s=0.0001)


    #x1=[-180,0]
    #y1=[0,90]
    #x11,y11=map(x1,y1)
    #map.scatter(x11,y11,marker='D',color='b')

#plt.show()

def lognormal_cummulative(N,r,rbar,sigma):
    total=(N/2)*(1+sp.special.erf(np.log(r/rbar)/np.sqrt(2)/np.log(sigma)))
    return total

cutoff=2 # this is the radius

sigma=[1.59,1.59,1.40,2.0,1.59,1.59,2.0]
pref=1.013e5
tref=293.0
zboltz=1.3807e-23
staird=pref/(tref*287.058)

model_aird = iris.load(mpath+'L1_air_density_Density of air.nc')
model_aird = model_aird[0]
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
    

mtime=model_n.coord('time').points    

sample_points=[('time',mtime[flag-1]),('model_level_number',38),('latitude',latitude),('longitude',longitude)]
cube2=model_n.interpolate(sample_points,iris.analysis.Nearest(extrapolation_mode='extrapolate'))

cube3=cube2.data
cube3=cube3/1000000 #conversion from meter to centimeter

for i in range(len(latitude)):
    plt.plot(longitude[i],cube3[i,i],'r.')
    plt.plot(longitude[i],n12_data[i],'b.')

plt.xlabel('longitude')
plt.ylabel('Particle number concentration')
plt.savefig('flight_vs_model_caribic.png')
#plt.legend()
plt.show()
#mlat=model_n.coord('latitude')


                

lon1=longitude[idx_lon]
alt_model=model_n.coord('altitude').points


mlat=model_n.coord('latitude').points
mlon=model_n.coord('longitude').points




mlevel=model_n.coord('model_level_number').points
malt=alt_model[:,130,140]






