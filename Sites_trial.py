### Written by Hamish Gordon, modified by Claude de Rijke-Thomas

#34/101 nucleation mode number
#
#34/103 Aitken number
#34/107 Accumulation number
#34/113 coarse mode
#34/119 Aitken insoluble
#34/122 Acc insoluble
#34/124 coarse insoluble
#38 401 DRY PARTICLE DIAMETER NUCLEATION-SO
#38 402 DRY PARTICLE DIAMETER AITKEN-SOL   
#38 403 DRY PARTICLE DIAMETER ACCUMULATN-SO
#38 404 DRY PARTICLE DIAMETER COARSE-SOL   
#38 405 DRY PARTICLE DIAMETER AITKEN-INS   
#38 406 DRY PARTICLE DIAMETER ACCUMULATN-IN
#38 407 DRY PARTICLE DIAMETER COARSE-INS 

#Beijing is 39.9075000 N,  116.3972300 E

#N96 longitude grid spacing 1.875 starts at zero
#latitude spacing 1.25 degrees starts at South Pole.

import sys
#dir_scripts=UKCA_postproc'#Change this to the downloaded folder
#sys.path.append(dir_scripts)
import UKCA_lib as ukl
import numpy as np
import numpy.ma as ma
#import scipy.special
import time
import iris
import iris.coord_categorisation
from glob import glob
import scipy.stats as st
from scipy.stats import lognorm
from scipy.special import erf
import matplotlib.pyplot as plt
import iris.plot as iplt
import iris.quickplot as qplt
import datetime
from scipy.io import netcdf
import os
from matplotlib.backends.backend_pdf import PdfPages
import getpass
import multiprocessing
from collections import defaultdict
#os.chdir(dir_scripts)
username=getpass.getuser()
iris.FUTURE.netcdf_promote = False
import variable_dict as vd
reload(vd)
import I_MODE_SETUP_Variables as ims
reload(ims)
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

ukca=1

def find_grid_cells(lat,lon, test, lonpoints,latpoints):
    if ukca==0:
        ysp=2.8
        xsp=2.8
    for i in range(0,len(latpoints)-2):
       lathi =  latpoints[i+1]
       if lathi < lat:
           break
    if test==1:
        print 'lathi',lathi,'latbox',i-1
        #if lathi > lat-0.5*ysp and i > 1:
    lats=[i,i+1,lathi-lat]
    #elif lathi < lat-0.5*ysp and i < 63:
    #    lats=[i+1,i+2,lathi-lat]
    #else:
    #    lats=[i,i]
    if lon>0 or ukca==0:
        for j in range(1,len(lonpoints)-1):
            lonhi = lonpoints[j]
            if lonhi > lon:
                break
    else:
        for j in range(1,len(lonpoints)-1):
            lonhi = lonpoints[j]
            if lonhi > 360+lon:
                break
    if test==1:
        print 'lonhi',lonhi,'lonbox',j-1
    if lonhi > lon+0.5*(lonpoints[j+1]-lonpoints[j]) and j > 1:
        lons = [j-2,j-1,lonhi-lon]
    elif lonhi < lon+0.5*(lonpoints[j+1]-lonpoints[j]) and j < 191:
        lons = [j-1,j, lonhi-lon]
    else:
        lons= [j-1,j-1]
    if lon > 0 or ukca==0:
        gridcoords = [[lats[0],lons[0]],[lats[0],lons[1]],[lats[1],lons[0]],[lats[1],lons[1]],[lathi-lat,lonhi-lon]]
    else:
        gridcoords = [[lats[0],lons[0]],[lats[0],lons[1]],[lats[1],lons[0]],[lats[1],lons[1]],[lathi-lat,lonhi-lon-360]]

    #gridcoords = [[lats[0],lons[0]],[lats[0],lons[1]],[lats[1],lons[0]],[lats[1],lons[1]],[lathi-lat,lonhi-lon]]#ANANTH removed this line in favor of the if and else at the top 
    print gridcoords
    return gridcoords


test=0
hasalt=0
fromScratch=1

if test==0:
#    sitelist=['Jungfraujoch','Hyytiala','Pallas','Finokalia','MaceHead','Hohenpeissenberg','PuydeDome','Nepal','Melpitz','Bondville','SouthernGreatPlains','TrinidadHead','CapeGrim','SableIsland','Tomsk','Listvyanka','Harwell','Weybourne','Botsalano','IndiaHimalaya','Aspvreten','Uto','Varrio','PicoEspejo','ThompsonFarm','MountWashington','CastleSprings','TaunusObs.','PoValley','MountWaliguan','MaunaLoa','Neumayer','SouthPole','PointBarrow','Samoa','Zugspitze','EastTroutLake']
    sitelist=[]
    latitudes=[]
    longitudes=[]
    altitudes_sl=[]
    sitesize=[]
    allsites = iris.load('gassp_sites_daily_means.nc')
    #ANANTH made sitecubes smaller testing
    sitecubes=iris.cube.CubeList([allsites[0],allsites[1],allsites[2]])
   # sitecubes=iris.load('gassp_sites_daily_means.nc')# ANANTH testing for all cubes not just 2 cubes
    for cube in sitecubes:
        sitelist.append(cube.name())
        
        latitudes.append(float(cube.attributes['latitude']))
        longitudes.append(float(cube.attributes['longitude']))
        altitudes_sl.append(float(cube.attributes['altitude']))
        sitesize.append(float(cube.attributes['cutoff_in_nm']))

    
    modelist = ['nucl_mode_sol', 'Aitken_mode_sol', 'accu_mode_sol', 'coarse_mode_sol', 'Aitken_mode_insol']
else:
    sitelist=['Jungfraujoch','Hyytiala','Pallas','Finokalia']

#longitudes=[7.98,24.3,24.1,25.7,350.1,11.0,3.0,86.82,12.9,271.6,262.5,235.85,144.69,300.0,85.1,104.9,359.0,1.10,25.75,79.6,17.4,21.4,29.6,288.95,289.1,282.7,288.7,8.4,11.6,100.9,204.42,351.75,335.2,203.39,189.44,10.98,249.83]
#latitudes=[46.56,61.9,68.0,35.3,53.3,47.8,45.75,27.95,51.5,40.1,36.6,41.05,-40.62,43.90,56.5,51.9,51.0,53.0,-25.53,29.4,58.8,59.8,67.8,8.52,43.1,44.27,43.7,50.2,44.7,36.28,19.54,-70.65,-89.9,71.32,-14.23,47.40,54.25]
print 'sitelist:', sitelist
print 'longitudes:', longitudes
print 'latitudes:', latitudes
nloc = len(sitelist)
#height above surface
if ukca==0:
    g3d = iris.load_cube('/nfs/a201/earhg/CLOUD/GLOMAP-nc/old-arc3/Hamish-nitrate-10p1/g3d.nc','Monthly mean altitude')
#height of surface (mean over grid-box, not height of mountain top where stations often are)
    geopotential=(1/9.81)*iris.load_cube('/nfs/a201/earhg/CLOUD/GLOMAP-nc/old-arc3/Hamish-nitrate-10p2/gld305_diag_t042_2006021100.nc', 'Surface geopotential')
    geopotential.units='m'
#print 'gepotential:', geopotential




path='/nfs/a201/earhg/CLOUD/GLOMAP-nc/ARCHER/Apr2018-clouds/L1/'
#path2='/nfs/a201/earhg/CLOUD/GLOMAP-nc/Hamish-v6-CMOR-PD/L1/'
path='/group_workspaces/jasmin2/crescendo/hgordon/u-ax337/L1_kappa0p88/'
path='/group_workspaces/jasmin2/gassp/eeara/RESULTS2/uax424_results/L1/'#ANANTH
path2=path
#leglabels=['CN (new TOMCAT)','CN (v6 Jan2016)']
leglabels=['','']
#paths=[path,path2]
paths=[path]

model_number_lists = []
model_radius_lists = []
#for path in paths:
#listofnumbers = iris.cube.CubeList()
###############################################ANANTH CHANGED STRUCTURE OF FOR LOOP
"""
    if ukca==0:
        listofnumbers.append(iris.load_cube(path+'L1_n_nucsol_m01s34i101_nbr_nucsol.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_aitsol_m01s34i103_nbr_aitsol.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_accsol_m01s34i107_nbr_accsol.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_corsol_m01s34i113_nbr_corsol.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_aitins_m01s34i119_nbr_aitins.nc'))
    #ANANTH CHANGE EVERYTHING TO NUMBER FRACTION
listofnumbers.append(iris.load_cube(path+'L1_n_nucsol_number_fraction_of_total_nucleation_mode_soluble_aerosol_in_air.nc'))
listofnumbers.append(iris.load_cube(path+'L1_n_aitsol_number_fraction_of_total_aitken_mode_soluble_aerosol_in_air.nc'))
listofnumbers.append(iris.load_cube(path+'L1_n_accsol_number_fraction_of_total_accumulation_mode_soluble_aerosol_in_air.nc'))
listofnumbers.append(iris.load_cube(path+'L1_n_corsol_number_fraction_of_total_coarse_mode_soluble_aerosol_in_air.nc'))
listofnumbers.append(iris.load_cube(path+'L1_n_aitins_number_fraction_of_total_aitken_mode_insoluble_aerosol_in_air.nc'))
model_number_lists.append(listofnumbers)
listofradii = iris.cube.CubeList()
listofradii.append(iris.load_cube(path+'L1_rad_nucsol_Radius_of_mode_nucsol.nc'))
listofradii.append(iris.load_cube(path+'L1_rad_aitsol_Radius_of_mode_aitsol.nc'))
listofradii.append(iris.load_cube(path+'L1_rad_accsol_Radius_of_mode_accsol.nc'))
listofradii.append(iris.load_cube(path+'L1_rad_corsol_Radius_of_mode_corsol.nc'))
listofradii.append(iris.load_cube(path+'L1_rad_aitins_Radius_of_mode_aitins.nc'))
model_radius_lists.append(listofradii)
       
#print '\n\n BATMAN \n\n'
"""
######################################################################################

for path in paths:
    listofnumbers = iris.cube.CubeList()
    if ukca==0:
        listofnumbers.append(iris.load_cube(path+'L1_n_nucsol_m01s34i101_nbr_nucsol.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_aitsol_m01s34i103_nbr_aitsol.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_accsol_m01s34i107_nbr_accsol.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_corsol_m01s34i113_nbr_corsol.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_aitins_m01s34i119_nbr_aitins.nc'))
    #ANANTH CHANGE EVERYTHING TO NUMBER FRACTION
    else:
        listofnumbers.append(iris.load_cube(path+'L1_n_nucsol_number_fraction_of_total_nucleation_mode_soluble_aerosol_in_air.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_aitsol_number_fraction_of_total_aitken_mode_soluble_aerosol_in_air.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_accsol_number_fraction_of_total_accumulation_mode_soluble_aerosol_in_air.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_corsol_number_fraction_of_total_coarse_mode_soluble_aerosol_in_air.nc'))
        listofnumbers.append(iris.load_cube(path+'L1_n_aitins_number_fraction_of_total_aitken_mode_insoluble_aerosol_in_air.nc'))
    model_number_lists.append(listofnumbers)
    listofradii = iris.cube.CubeList()
    listofradii.append(iris.load_cube(path+'L1_rad_nucsol_Radius_of_mode_nucsol.nc'))
    listofradii.append(iris.load_cube(path+'L1_rad_aitsol_Radius_of_mode_aitsol.nc'))
    listofradii.append(iris.load_cube(path+'L1_rad_accsol_Radius_of_mode_accsol.nc'))
    listofradii.append(iris.load_cube(path+'L1_rad_corsol_Radius_of_mode_corsol.nc'))
    listofradii.append(iris.load_cube(path+'L1_rad_aitins_Radius_of_mode_aitins.nc'))
    model_radius_lists.append(listofradii)

######################################################################################


def getdataAtSites(model_version_index):
    si=0
    radoutputData=[]
    outputData = []
    for site in sitelist: #for each site
        outputnumberatsites = []
        radoutputnumberatsites = []
        imode=0
        print site
        numberlist = model_number_lists[model_version_index]
        radiuslist = model_radius_lists[model_version_index]
        latlon = find_grid_cells(latitudes[si],longitudes[si], test,numberlist[0].coord('longitude').points,numberlist[0].coord('latitude').points)
        for cube in numberlist: #for particle numbers of each mode
            
            cubelist = iris.cube.CubeList()      #making a list of cubes for particle number concentrations

            cubelist.append(cube[:,:,(latlon[0])[0],(latlon[0])[1]])
            cubelist.append(cube[:,:,(latlon[1])[0],(latlon[1])[1]])
            cubelist.append(cube[:,:,(latlon[2])[0],(latlon[2])[1]])
            cubelist.append(cube[:,:,(latlon[3])[0],(latlon[3])[1]])
            radcubelist =iris.cube.CubeList()   # making a list of cubes for particle mode-radii
            radcubelist.append((radiuslist[imode])[:,:,(latlon[0])[0],(latlon[0])[1]])
            radcubelist.append((radiuslist[imode])[:,:,(latlon[1])[0],(latlon[1])[1]])
            radcubelist.append((radiuslist[imode])[:,:,(latlon[2])[0],(latlon[2])[1]])
            radcubelist.append((radiuslist[imode])[:,:,(latlon[3])[0],(latlon[3])[1]])
            if si ==0:
                #print 'site coordinates',latitudes[si],longitudes[si]
                print 'box 1',(latlon[0])[0],(latlon[0])[1]
                print 'box 2',(latlon[1])[0],(latlon[1])[1]
                print 'box 3',(latlon[2])[0],(latlon[2])[1]
                print 'box 4',(latlon[3])[0],(latlon[3])[1]
            if ukca==1:
                hf = -1*((latlon[4])[1])/(numberlist[0].coord('longitude').points[1]-numberlist[0].coord('longitude').points[0])
            else:
                hf = -1*((latlon[4])[1])/2.8
            if hf < 0.5:
                horizontal_scale = 0.5-hf
            else:
                horizontal_scale = 1.5-hf
            vf = ((latlon[4])[0])/(numberlist[0].coord('latitude').points[1]-numberlist[0].coord('latitude').points[0])
            if vf < 0.5:
                vertical_scale = 0.5-vf
            else:
                vertical_scale = 1.5-vf
            if si==0:
                print 'vf,hf',vf,hf
                print 'v, h', vertical_scale, horizontal_scale
            cubelistH1 = cubelist[0].data*(1-horizontal_scale) + cubelist[1].data*horizontal_scale
            cubelistH2 = cubelist[2].data*(1-horizontal_scale) + cubelist[3].data*horizontal_scale
            cubeCol = cubelist[0].copy(cubelistH1*vertical_scale+cubelistH2*(1-vertical_scale))
            radcubelistH1 = radcubelist[0].data*(1-horizontal_scale) + radcubelist[1].data*horizontal_scale
            radcubelistH2 = radcubelist[2].data*(1-horizontal_scale) + radcubelist[3].data*horizontal_scale
            radcubeCol = radcubelist[0].copy(radcubelistH1*vertical_scale+radcubelistH2*(1-vertical_scale))
            cubeCol.long_name = sitelist[si] + modelist[imode]
            radcubeCol.long_name = sitelist[si] + modelist[imode]
            outputnumberatsites.append(cubeCol)
            radoutputnumberatsites.append(radcubeCol)
            print cubeCol.data[0][30]
            if imode ==0:
                totalcube = cubeCol
            else: 
                totalcube = totalcube + cubeCol
            imode=imode+1
        
        radoutputData.append(radoutputnumberatsites)
        outputData.append(outputnumberatsites)
        si=si+1
    print 'len(radoutputData)', len(radoutputData)
    print outputData
    #iris.save(outputData,'/nfs/a201/earhg/CLOUD/GLOMAP-nc/Hamish-nitrate-11/L1/n3_at_surface_sites__mod.nc')
    #iris.save(radoutputData,'/nfs/a201/earhg/CLOUD/GLOMAP-nc/Hamish-nitrate-11/L1//radconcdata_at_surface_sites__mod.nc')
    return radoutputData, outputData

model_numbers=[]
model_radii=[]
if fromScratch==1:
    print 'getting data at sites'    
    for i in range(0,len(model_number_lists)):
        radoutputData, outputData = getdataAtSites(i)
        model_numbers.append(outputData)
        model_radii.append(radoutputData)
else:
    for path in paths:
        outputData = iris.load(path+'n3_at_surface_sites__mod.nc') 
        radoutputData  = iris.load(path+'radconcdata_at_surface_sites__mod.nc')
        model_numbers.append(outputData)
        model_radii.append(radoutputData)


altData = iris.cube.CubeList()

#print '\n\n BATMAN \n\n'



def getAltitudesAtSites(): #ALTITUDES
     
    si=0
    for site in sitelist:            
        latlon = find_grid_cells(latitudes[si],longitudes[si], test,listofnumbers[0].coord('longitude').points,listofnumbers[0].coord('latitude').points)
        if ukca==0:
            geo1=float(geopotential.data[0,(latlon[0])[0],(latlon[0])[1]])
            geo2=float(geopotential.data[0,(latlon[1])[0],(latlon[1])[1]])
            geo3=float(geopotential.data[0,(latlon[2])[0],(latlon[2])[1]])
            geo4=float(geopotential.data[0,(latlon[3])[0],(latlon[3])[1]])
            altCol1 =g3d[:,(latlon[0])[0],(latlon[0])[1]]+geo1
            altCol2 =g3d[:,(latlon[1])[0],(latlon[1])[1]]+geo2
            altCol3 =g3d[:,(latlon[2])[0],(latlon[2])[1]]+geo3
            altCol4 =g3d[:,(latlon[3])[0],(latlon[3])[1]]+geo4
        else:
            altCol1 = listofnumbers[0].coord('altitude').points[:,(latlon[0])[0],(latlon[0])[1]]
            altCol2 = listofnumbers[0].coord('altitude').points[:,(latlon[1])[0],(latlon[1])[1]]
            altCol3 = listofnumbers[0].coord('altitude').points[:,(latlon[2])[0],(latlon[2])[1]]
            altCol4 = listofnumbers[0].coord('altitude').points[:,(latlon[3])[0],(latlon[3])[1]]
       
        print '\n\n JOKER \n\n', type(altCol1)
        altCol1=np.ascontiguousarray(altCol1)
        altCol2=np.ascontiguousarray(altCol2)
        altCol3=np.ascontiguousarray(altCol3)
        altCol4=np.ascontiguousarray(altCol4)
       # print '\n\n JOKER \n\n',type(altCol1)
        #print '\n\n RIDDLER \n\n', altCol5.flags
        
        if test ==1:
            print 'site coordinates ',latitudes[si],longitudes[si]
            print 'box 1',(latlon[0])[0],(latlon[0])[1]
            print 'box 2',(latlon[1])[0],(latlon[1])[1]
            print 'box 3',(latlon[2])[0],(latlon[2])[1]
            print 'box 4',(latlon[3])[0],(latlon[3])[1]
        hf = -1*((latlon[4])[1])/2.8
        if hf < 0.5:
            horizontal_scale = 0.5-hf
        else:
            horizontal_scale = 1.5-hf
        vf = ((latlon[4])[0])/2.8
        if vf < 0.5:
            vertical_scale = 0.5-vf
        else:
            vertical_scale = 1.5-vf
        print 'vf,hf',vf,hf
        print 'v, h', vertical_scale, horizontal_scale
        print '\n\n BATMAN \n\n'
        #print 1-horizontal_scale
        #trial=[q*(1-horizontal_scale) for q in altCol1]
     #   print '\n\n ROBIN \n\n',trial,'\n\n'
        #ANANTH changing the structure of altColH1 and others
        #altColH1 = [q*(1-horizontal_scale)+p*horizontal_scale for q,p in zip(altCol1.data,altCol2.data)]
        altColH1 = altCol1*(1-horizontal_scale)+altCol2*horizontal_scale
        #altColH1 = altCol1.data*(1-horizontal_scale) + altCol2.data*horizontal_scale
        #print '\n\n ROBIN0 \n\n', altColH1
        
        #altColH2 = [l*(1-horizontal_scale)+k*horizontal_scale for l,k in zip(altCol3,altCol4)]
        altColH2 = altCol3*(1-horizontal_scale)+altCol4*horizontal_scale
        #print altCol1.data
        #altColH2 = altCol3.data*(1-horizontal_scale) + altCol4.data*horizontal_scale
       # print '\n\n ROBIN \n\n',altColH1
        #temp=[n*vertical_scale+m*(1-vertical_scale) for n,m in zip(altColH1,altColH2)]
       # altCol = temp.copy([n*vertical_scale+m*(1-vertical_scale) for n,m in zip(altColH1,altColH2)])
        #altCol = altCol1.copy([n*vertical_scale+m*(1-vertical_scale) for n,m in zip(altColH1,altColH2)])
       # print 'ROBIN2',altCol
        
        #altCol = altCol1.copy(altColH1*vertical_scale+altColH2*(1-vertical_scale))
        altCol=iris.cube
        altCol.data=altColH1*vertical_scale+altColH2*(1-vertical_scale)
       # print '\n\nROBIN1\n',tempa,'\nROBIN2\n',type(tempa)
        altCol.long_name=sitelist[si]
        #print altData,'\nROBIN2\n' 
        altData.append(altCol)
        print '\nROBIN3',type(altData)
        si=si+1
   #ANANTH testing output 
    for flag3 in range(3):
        print 'NEXT ',flag3,'\n',altData[flag3].data,'\n'
    #print altData[0].data,'\n\n',altData[1].data      
    return altData
   # iris.save(altData,path+'height_at_surface_sites__mod.nc')
if fromScratch==1:
    #getAltitudesAtSites()
    temp1=getAltitudesAtSites()#ANANTH NEW VARIABLE DEFINED 
    
else:
    altData = iris.load('/nfs/a201/earhg/CLOUD/GLOMAP-nc/Hamish-nitrate-11/height_at_surface_sites__mod.nc')

#global gld
#gld=iris.cube
#ANANTH uncommentted altitudes_sl
#altitudes_sl=[3580.0,180.0,340.0,250.0,5.0,995.0,1465.0,5079.0,86.0,213.0,320.0,107.0,94.0,5.0,170.0,750.0,60.0,0.0,1424.0,2180.0,25.0,8.0,400.0,4775.0,75.0,1910.0,406.0,810.0,11.0,3816.0,3397.0,42.0,2841.0,11.0,77.0,2650.0,492.0]  
def find_altitude_glomap(siteIndex):
   
    g1d=temp1[siteIndex]#ANANTH
    print g1d,'\n\n',type(g1d),'\n\n'
   # temp45=gld.data[30]
   # g1d=iris.load_cube(path+'height_at_surface_sites__mod.nc',sitelist[siteIndex])
    altbox=0
    site_alt=altitudes_sl[siteIndex]
    #print g1d.data
    for i in range(0,31):
        #temp2=gld
        altbound = g1d.data[i]
        #altbound = g1d.data[i]
        if site_alt < altbound:
            altbox=i
    if site_alt < g1d.data[30]:
        altbox=30
    print altbox
    return altbox

#gld=iris.cube
altitudeboxes = []
for i in range(0, nloc, 1):
    altitudeboxes.append(find_altitude_glomap(i))
print '\n\n FINAL \n\n', altitudeboxes


def readSiteDataFileGASSP():
    allmonthlydata=[]
    
    for cube in sitecubes:
        monthdata=np.zeros(12)
        iris.coord_categorisation.add_month_number(cube,cube.coord('time'))
        monthly_means = cube.aggregated_by(['month_number'],iris.analysis.MEAN)
        print monthly_means
        print monthly_means.coord('month_number').points
        print monthly_means.data
        for i in range(0,12):
            for j in range(0, len(monthly_means.data)):
                if monthly_means.coord('month_number').points[j]==i+1:
                    monthdata[i] = monthly_means.data[j]
        monthdata1 = ma.masked_where(monthdata <=0, monthdata)
        monthdata2 = ma.masked_invalid(monthdata1)
        allmonthlydata.append(monthdata2)
        print monthdata1
    return allmonthlydata
        
def readSiteDataFile():
    #restore data arrays of observations from Dom's code (these were saved after running read_spracklen2010_cn_obs.pro) - alternatively could just copy the code to read that file in here
    nloc=37
    file='spracklen2010_cn_obs_changeOrder.txt'
    print 'reading in sites'
    allmonthlydata = []
    with open(file) as myfile:
        head = [next(myfile) for x in xrange(15)]
        # print head
        for i in xrange(nloc):
            sitename = next(myfile)
            size = next(myfile)
            lonlatlev = next(myfile)
            monthlydata = next(myfile)
            monthlydata = monthlydata.strip('\n')       
            montharrst = monthlydata.split()
            montharr = [float(x) for x in montharrst]
            #print montharr
            allmonthlydata.append(montharr)
    return allmonthlydata

def lognormal_cumulative_to_r(N,r,rbar,sigma):
     return (N/2.0)*(1.0+erf(np.log(r/rbar)/np.sqrt(2.0)/np.log(sigma)))

sigma = [1.59,1.59,1.4,2.0,1.59] #s.d of all modes smallest to largest respectively
#sitesize = the lower cutoff diameter that the each site from (has been accounted for in all further model observations)
#sitesize = [10,3,10,10,10,3,10,3,3,14,10,14,3,10,3,3,10,10,10,10,3,7,8,10,7,10,7,10,3,13,14,14,14,14,14,12,3]
model_results=[]
#for k in range(0,len(path)):#ANANTH REMOVED paths variable only running one model 
    
for k in range(0,len(paths)):
    print '\nNUMBER OF MODELS \n',k,'\n'
    outputData = model_numbers[k]
    model_number_results=[]
    nuclN = []
    AitkenN = []
    accN = []
    coarseN = []
    AiInN = []
   # for i in range(3):#ANANTH
   # nloc=37
    nloc=3#since we have only 3 sites
    for i in range(0, nloc, 1):
        for j in range(0, 12, 1):
            nuclN.append(1e-6*(outputData[i])[0].data[j][altitudeboxes[i]])
            AitkenN.append(1e-6*(outputData[i])[1].data[j][altitudeboxes[i]])
            accN.append(1e-6*(outputData[i])[2].data[j][altitudeboxes[i]])
            coarseN.append(1e-6*(outputData[i])[3].data[j][altitudeboxes[i]])
            AiInN.append(1e-6*(outputData[i])[4].data[j][altitudeboxes[i]])    
    print 'particle numbers per cm3 for each site in Aitken mode with correct altitude for each month:', len(AitkenN)
    radoutputData = model_radii[k]
    
    radnuclN = []
    radAitkenN = []
    radaccN = []
    radcoarseN = []
    radAiInN = []
    for i in range(0, nloc, 1):
        for j in range(0, 12, 1):
            radnuclN.append((radoutputData[i])[0].data[j][altitudeboxes[i]])
            radAitkenN.append((radoutputData[i])[1].data[j][altitudeboxes[i]])
            radaccN.append((radoutputData[i])[2].data[j][altitudeboxes[i]])
            radcoarseN.append((radoutputData[i])[3].data[j][altitudeboxes[i]])
            radAiInN.append((radoutputData[i])[4].data[j][altitudeboxes[i]])
    print 'the length of radAitkenN:', len(radAitkenN)
   
    Aitkenarray = []
    nuclarray = []
    accarray = []
    coarsearray = []
    AiInarray = []
    #calculations compensating for the lower instrument cutoff
    for j in range(0, 12*nloc, 1):
        Aitkencalc = AitkenN[j] -lognormal_cumulative_to_r(AitkenN[j], (sitesize[((j/12)%12)]*0.5), (radAitkenN[j]*1e+9), sigma[1])
        Aitkenarray.append(Aitkencalc)
        NuclCalc = nuclN[j] -lognormal_cumulative_to_r(nuclN[j], (sitesize[((j/12)%12)]*0.5), (radnuclN[j]*1e+9), sigma[0])
        nuclarray.append(NuclCalc)
        AccCalc = accN[j] -lognormal_cumulative_to_r(accN[j], (sitesize[((j/12)%12)]*0.5), (radaccN[j]*1e+9), sigma[2])
        accarray.append(AccCalc)
        coarsecalc = coarseN[j] -lognormal_cumulative_to_r(coarseN[j], (sitesize[((j/12)%12)]*0.5), (radcoarseN[j]*1e+9), sigma[3])
        coarsearray.append(coarsecalc)
        AiIncalc = AiInN[j] -lognormal_cumulative_to_r(AiInN[j], (sitesize[((j/12)%12)]*0.5), (radAiInN[j]*1e+9), sigma[4])
        AiInarray.append(AiIncalc)
    the_amendment = []
    for i in range(0, 12*nloc, 1):
       #ANANTH REMOVING COARSE 
       # the_amendment.append(Aitkenarray[i]+ nuclarray[i]+ accarray[i]+ coarsearray[i]+ AiInarray[i])
        
        the_amendment.append(Aitkenarray[i]+ nuclarray[i]+ accarray[i]+ AiInarray[i])
    print len(the_amendment)
    model_results.append(the_amendment)
# print len(Aitkenarray)
# print len(nuclarray)
# print len(accarray)
# print len(coarsearray)
# print len(AiInarray)



def plotSurfaceCN2(path,obsData, siteIndex, model_results): #can pass in cubes2 as arg later
    altbox = find_altitude_glomap(siteIndex)
    print altbox
    sp = plt.subplot(8,5,siteIndex+1)
    plt.tight_layout(h_pad=0.5, rect = [0.032,0.032,1,1])
    print 'sitelist[siteIndex], altbox:', sitelist[siteIndex], altbox
    print obsData
    #avoid iris plotting since it tries to interpret time as UTC and fails
    for imod in range(0,len(paths)):
        model_data =model_results[imod]
        plt.plot(np.arange(0, 12, 1), model_data[siteIndex*12:(siteIndex+1)*12], label=leglabels[imod])
    plt.plot(np.arange(0,12,1),obsData, 'b',label='Observations',marker='o',ms=6)
   
    plt.gca().set_yscale('log')
    plt.gca().set_ylim(ymin=50,ymax=1.5e4)
    labels=['J', '', '', '', 'M', '', '', '', 'S', '', '', 'D']
    plt.xticks(np.arange(0, 12, 1), labels, fontsize=10)
    plt.text(0.1, 0.08, sitelist[siteIndex], fontsize=10,transform=plt.gca().transAxes)
    if siteIndex ==nloc-1:
        plt.legend(bbox_to_anchor=(0.55, 0.05),bbox_transform=plt.gcf().transFigure, loc='lower left') 
    from matplotlib.backends.backend_pdf import PdfPages
#from pdb import set_trace as st
#main
#ukl.create_folder(saving_folder)
allmonthlySiteData = readSiteDataFileGASSP()

with PdfPages('surface_sites_GASSP.pdf') as pdf:
    plt.figure(figsize=(8.27,11.69))
   # plt.figure()
    for i in range(0,len(sitelist)):
        i1 = int(i/5)
        i2 = i%5
        print i1,i2
        
        obsData = allmonthlySiteData[i]
        plotSurfaceCN2(path,obsData,i, model_results) 
    print 'saving pdf'
    pdf.savefig()
    plt.close()
    print 'saved'





