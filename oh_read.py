
import numpy as np 
import matplotlib.pyplot as plt
import glob as glb
import matplotlib.backends.backend_pdf as mb
import iris


home_path='/group_workspaces/jasmin2/gassp/eeara/'


# so2_path 
#path='/group_workspaces/jasmin2/gassp/eeara/so2_data/'

# oh path 
path='/group_workspaces/jasmin2/gassp/eeara/oh_data/'

#model_path and file 
mpath='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-ax424/All_time_steps/'

#filename='PEM-Tropics-A_DC8_so2_Tahiti.stat'
#model_file='All_time_steps_m01s34i072_mass_fraction_of_sulfur_dioxide_in_air.nc'
model_file='All_time_steps_m01s34i081_mass_fraction_of_hydroxyl_radical_in_air.nc'

mpath=mpath+model_file

title=['ialt','N','min','max','mean','stddev','5%','25%','median','75%','95%']
check='mean'
pdf=mb.PdfPages(home_path+'oh_compare.pdf')
n_plot=5
grid_size=(n_plot,1)

temp=0
#f=open(path+filename,'r')
#data=f.read()
def get_latlon(filename):
    with open(filename) as f:
        content =f.readlines()
    #print content[3]   # line number 3 has the lattitude-longitude data
    a = content[3]
    
    #a=np.fromstring(content[3], dtype = int)
    #print a[2:5]
    lat1= a[8:10]
    lat2= a[13:15]
    lon1= a[23:26]
    lon2= a[29:32]
    
    lat1=int(lat1)
    lon1=int(lon1)
    return lat1,lon1


def create_cube(cube):
    altitude=cube.coord('altitude').points
    coord1=cube.coord('model_level_number').points
    coord2=cube.coord('latitude').points
    coord3=cube.coord('longitude').points
    dim1=iris.coords.DimCoord(coord1,standard_name='model_level_number')
    dim2=iris.coords.DimCoord(coord2,standard_name='latitude')
    dim3=iris.coords.DimCoord(coord3,standard_name='longitude')
    newcube=iris.cube.Cube(altitude,dim_coords_and_dims=[(dim1,0),(dim2,1),(dim3,2)])
    return newcube

def find_alt(alt,sample):

    alt=alt.collapsed('latitude',iris.analysis.MEAN)
    alt=alt.collapsed('longitude',iris.analysis.MEAN)
    data=alt.data
    data=data/1000
    #print data
    temp2=[]
    model_level=alt.coord('model_level_number').points
    print model_level,'\n'
    
    for j in range(len(data)):
        error=abs(data[j]-sample)
        temp2=np.append(temp2,error)
    
    print temp2,'\n'
    indx=np.argmin(temp2)
    print 'altitude nearest',data[indx],'\n'
    return model_level[indx]

def get_model_data(cube,level_fit,lat,lon):
    cube=cube.collapsed('time',iris.analysis.MEAN)
    data_points=[('model_level_number',level_fit),('latitude',lat),('longitude',lon)]
    cube2=cube.interpolate(data_points,iris.analysis.Nearest(extrapolation_mode='extrapolate'))
    return cube2

"""
def get_p(cube,level_fit,lat,lon):
    cube=cube.collapsed('time',iris.analysis.MEAN)
    data_points=[('model_level_number',level_fit),('latitude',lat),('longitude',lon)]
    cube2=cube.interpolate(data_points,iris.analysis.Nearest(extrapolation_mode='extrapolate'))
    return cube2
"""


def study(filename):
    indx=0
    for i in range(len(title)):
        if title[i]==check:
            indx=i
            break
    #load all data into a numpy array from a file
    data = np.loadtxt(filename)
    altitude=data[:,0]
    attribute=data[:,indx]
    return altitude, attribute,filename
    

files=glb.glob(path+'*oh*')
#files=[path+filename]
length=len(files)
temp2=np.array([])
n_plot=5
pressure_file='All_time_steps_m01s00i407_air_pressure.nc'
p_path='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-ax424/All_time_steps/'
p_cube=iris.load(p_path+pressure_file)
p_cube=p_cube[0]
p_cube=p_cube.collapsed('time',iris.analysis.MEAN)
p_cube=p_cube.collapsed('latitude',iris.analysis.MEAN)
p_cube=p_cube.collapsed('longitude',iris.analysis.MEAN)
p_data=p_cube.data
R=0.0821 #L atm mol-1


p_path='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-ax424/All_time_steps/'


for i in range(length):
    lat,lon=get_latlon(files[i])
    cube=iris.load(mpath)
    cube=cube[0]
    alt=create_cube(cube)
    temp_alt=np.array([])
    temp_mean=np.array([])

    """
    sample=4 # find model level number at altitude 10km
    level_fit=find_alt(alt,sample)
    model_mass_fraction=get_model_data(cube,level_fit,lat,lon)
    pptv=pow(10,-12)
    model_mole_fraction=(model_mass_fraction*29/64)/pptv
    model_mole_fraction=model_mole_fraction.data
    """
    if i%n_plot==0:
        fig=plt.figure(figsize=(8.27,11.69),dpi=100)
    print 'Value of i = ',i,'\n' 
    alt2,mean,filename=study(files[i])
    
    
    for j in range(len(alt2)):
        sample=alt2[j] # find model level number at altitude 
        level_fit=find_alt(alt,sample)
        model_mass_fraction=get_model_data(cube,level_fit,lat,lon)
        pptv=pow(10,-12)
        ppbv=pow(10,-9)
        ppmv=pow(10,-6)
        if mean[0]<1:
            model_mole_fraction=(model_mass_fraction*29/17)/pptv
            model_mole_fraction=model_mole_fraction.data
            temp_mean=np.append(temp_mean,model_mole_fraction)
        else:
            model_mole_fraction=(model_mass_fraction*29/17)/ppmv
            model_mole_fraction=model_mole_fraction.data
            #convert to molecules/cm3
            air_n=(1/ppmv)/(6.023*pow(10,23))
            p_model=p_data[level_fit]/(101325)
            V=(air_n*R*(15+273)/(p_model))*1000
            molec_pcm3=model_mole_fraction/V
            temp_mean=np.append(temp_mean,molec_pcm3)


       # temp_mean=np.append(temp_mean,model_mole_fraction)

        

    temp3=plt.subplot2grid(grid_size,(i%n_plot,0))
    plt.plot(alt2,mean,'b*',alt2,temp_mean,'r*')
    temp3.set_title(filename[47:])
    plt.grid()
    if mean[0]>1:
        plt.ylabel('Molecules/cm3')
    else:
        plt.ylabel('Conc(pptv)')

    if (i+1)%n_plot==0:
        plt.xlabel('altitude(km)')
        pdf.savefig(fig)

pdf.close()
    
    

    #alt=alt.collapsed(sdasdasdasdasd'latitude',iris.analysis.MEAN)
    #alt=alt.collapsed('longitude',iris.analysis.MEAN)
    #print 'rcube::::::::::::::::::::::::::',level_fit,'\n'
    #print '\n',cube,'\n'
    #print model_mole_fraction.data






#content = [x.strip for x in content]

"""
for i in range(len(data)):
    if data[i]=='L'

"""

"""
title=['ialt','N','min','max','mean','stddev','5%','25%','median','75%','95%']

check='mean'
pdf=mb.PdfPages(home_path+'so2_data.pdf')
n_plot=5 ##number of plots per page
grid_size=(n_plot,1)

def study(filename):
    indx=0
    for i in range(len(title)):
        if title[i]==check:
            indx=i
            break
    #load all data into a numpy array from a file
    data = np.loadtxt(filename)
    altitude=data[:,0]
    attribute=data[:,indx]
    return altitude, attribute,filename
    
files=glb.glob(path+'*so2*')
list_length=len(files)
nc=321
flag=0
for i in range(list_length):
    if i%n_plot==0:
        fig=plt.figure(figsize=(8.27,11.69),dpi=100)
    print 'Value of i = ', i, '\n'
    alt,mean,filename=study(files[i])
    temp=plt.subplot2grid(grid_size,(i%n_plot,0))
    plt.plot(alt,mean,'b*')
    temp.set_title(filename[47:])
    plt.grid()
    if mean[0]>1:
        plt.ylabel('Concentration (pptv)')
    else:
        plt.ylabel('Vol_mixing_ratio(ppbv)')

    if (i+1)%n_plot==0:
        plt.xlabel('altitude(km)')
        pdf.savefig(fig)

pdf.close()
"""

print '\nPROGRAM ENDED\n' 
