


import iris
import numpy as np
import matplotlib.pyplot as plt 
import glob
import time

dir_files='/group_workspaces/jasmin2/gassp/eeara/2008/'
#pp_files=glob.glob(dir_files+'*.pp')
obs_files_dir='/group_workspaces/jasmin2/gassp/eeara/ARCTAS/'

model_files=glob.glob(dir_files+'*Number*.nc')
obs_files=glob.glob(obs_files_dir+'*.nc')

##### this file was used to find altitude as altitude is a derived coordinate..we can get altitude as a function of model level number
path2='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-ax424/All_time_steps/'
model_file2='All_time_steps_m01s34i072_mass_fraction_of_sulfur_dioxide_in_air.nc'
alt_file=path2+model_file2

#####
org_file='2007sepm01s38i504Number_nuc_mode_m3.nc'

org_cube=iris.load(dir_files+org_file)
org_cube=org_cube[0]
t_model=org_cube.coord('time').points
t_model_ref=t_model[0]

months_array=['sep','oct','nov','dec','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
days_array=[31,29,31,30,31,30,31,31,30,31,30,31]

init_days=30+31+30+31 # sum of days in 2007 the previous year of model run 
#for i in range(len(model_files)):
#    print '\nFile Number: ',i,' .. Filename: ',model_files[i],'\n'
#print netcdf_files
ref_hr=0


#this function is used to convert obs data grid to the corresponding model dimensions time is expressed in hours from the start point of the model sep1st 2007 00:00
def norm(month,day,hour,t_obs):
    t_init=t_model_ref
    #add months in 2007
    indx=month
    tot_days=init_days+sum(days_array[0:indx-1])+day
    
    tot_hours=tot_days*24+hour
    
    t_new=t_init+tot_hours
    #print '\n\n TOTAL_DAYS : ', tot_days
    #
    t_obs=t_obs/3600
    t_obs=t_obs-t_obs[0]
    t_norm=t_obs+t_new

    return t_norm


cube2=iris.load(alt_file)
cube2=cube2[0]
m_alt=cube2.coord('altitude').points
mlevel=cube2.coord('model_level_number').points
m_alt=m_alt[:,10,10]/1000

#cube2=cube2.collapsed('latitude',iris.analysis.MEAN)
#cube2=cube2.collapsed('longitude',iris.analysis.MEAN)
temp3=[]
level_norm=[]

def find_level(alt_data):
    level_norm=[]
    for q in alt_data:
        error=abs(m_alt-q)
        pos=np.argmin(error)
        level_norm=np.append(level_norm,mlevel[pos])

        #temp3=np.append(temp3,error)
         
    return level_norm


def get_model_data(t_norm,level_norm,lat_norm,lon_norm):
    temp4=['mar','dec']
    interp_data=[]
    err1=[]
    err2=[]
    err3=[]
    err4=[]
    indx1=[]
    indx2=[]
    indx3=[]
    indx4=[]
    interp_data=[]
    counter=0
    if file_number<15:
        file1='2008marm01s38i504Number_nuc_mode_m3.nc' 
        file2='2008march_pi_505.nc'
    else:
        file1='2008junm01s38i504Number_nuc_mode_m3.nc'
        file2='2008june_pi_505.nc'
    mcube=iris.load(dir_files+file1)
    mcube=mcube[0]
    mdata=mcube.data/1000000
    
    """
    mcube2=iris.load(dir_files+file2)
    mcube2=mcube2[0]
    mdata2=mcube2.data/1000000
    """
    #data_points=[('time',t_norm),('model_level_number',level_norm),('latitude',lat_norm),('longitude',lon_norm)]
#new_cube
    mtime=mcube.coord('time').points
    mlevel=mcube.coord('model_level_number').points
    mlat=mcube.coord('latitude').points
    mlon=mcube.coord('longitude').points
    model_aird=iris.load(aird_path+aird_file)
    model_aird=model_aird[0]
    model_aird_data=model_aird.data

    for iter1 in range(len(t_norm)):
        print '\n\n counter :',counter
        err1=abs(mtime-t_norm[iter1])
        err2=abs(mlevel-level_norm[iter1])
        err3=abs(mlat-lat_norm[iter1])
        err4=abs(mlon-lon_norm[iter1])
        indx1=np.argmin(err1)
        indx2=np.argmin(err2)
        indx3=np.argmin(err3)
        indx4=np.argmin(err4)
        val=(mdata[indx1,indx2,indx3,indx4])*staird/model_aird_data[indx2,indx3,indx4]
        interp_data=np.append(interp_data,val)
        #interp_data=np.append(interp_data,val)
        counter =counter+1

    return interp_data
    

#model
file_number=0

aird_path='/group_workspaces/jasmin2/gassp/eeara/2008/L1/'
aird_file='L1_air_density_Density of air.nc'

pref=1.013e5
tref=293.0
#M_air=29
staird=pref/(tref*287.058)


#obs_files=obs_files[0]
length=len(obs_files)
for j in range(length):
    cube=iris.load(obs_files[j])
    n10=cube[0]
    alt=cube[3]
    lon=cube[4]
    lat=cube[8]
    t_obs=cube[0].coord('TIME').points
    t1=n10.attributes['Time_Coverage_Start']
    t2=n10.attributes['Time_Coverage_End']
    print '\nSTART= ',t1,'||','END= ',t2 
    month_str=t1[5:7]
    day_str=t1[8:10]
    time_str=t1[11:13]
    month=int(month_str)
    day=int(day_str)
    hour=int(time_str)

    t_norm=norm(month,day,hour,t_obs)
    lat_norm=lat.data
    lon_norm=lon.data+180
    
    #find new alt_array
    alt_data=alt.data
    level_norm=find_level(alt_data)
   # model_alt=    
    new_cube=get_model_data(t_norm,level_norm,lat_norm,lon_norm) 

    #file_number+=1
    plt.figure()
    plt.plot(new_cube,alt_data,'r*',n10.data,alt_data,'b.')
    #plt.show()
    plt.title('Altitude vs Number_concentration(cm-3)')
    plt.xlabel('Number Concentration(cm-3)')
    plt.ylabel('Altitude (km)')
    pic_num=str(file_number)
    plt.savefig('File'+pic_num+'.png')

    file_number+=1


print new_cube

#c[0].attributes['Time_Coverage_End']

