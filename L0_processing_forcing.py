# -*- coding: utf-8 -*-
"""

Code developed by Jesus Vergara Temprado and Kirsty Pringle

eejvt@leeds.ac.uk
K.Pringle@leeds.ac.uk

Aerosol modellers group
Institute for climate and atmospheric science (ICAS)
University of Leeds 2016

"""

import sys
#dir_scripts='/nfs/see-fs-02_users/earhg/UKCA_postproc'#Change this to the downloaded folder
#sys.path.append(dir_scripts)
import UKCA_lib as ukl
import numpy as np
import time
import iris
from glob import glob
import matplotlib.pyplot as plt
import iris.plot as iplt
import iris.quickplot as qplt
import datetime
from scipy.io import netcdf
import os
import getpass
import multiprocessing
#os.chdir(dir_scripts)
username=getpass.getuser()
iris.netcdf_promote = False
iris.netcdf_no_unlimited = False
import variable_dict as vd
reload(vd)
nmonths=12  # this if written wrongly gives an error 

orog_file = '/group_workspaces/jasmin2/gassp/jvergaratemprado/n96_hadgem1_qrparm.orog_new.pp'#jasmin
#orog_file = '/nfs/a107/earkpr/ACID-PRUFF/Masaru/OAT5/teafw/ppfiles/n96_hadgem1_qrparm.orog_new.pp'#leeds foe-linux
#plt.interactive(0)
#files_directory_UKCA='/nfs/a107/earkpr/DataVisualisation/UKCA/'
#files_directory_UKCA='/nfs/a201/'+username+'/UKCA/First_nucleation_runs/'
"""
files_directory_UKCA='/group_workspaces/jasmin2/crescendo/hgordon/'
run='u-ax337/'
"""
files_directory_UKCA='/group_workspaces/jasmin2/asci/eeara/'
files_directory=files_directory_UKCA
pp_files=glob(files_directory+'*pp')
print(pp_files)
dateoffset=9
date=(pp_files[0])[len(files_directory)+dateoffset:-3]
stashcodes=[]


stashcodes = ['m01s50i061','m01s50i063','m01s34i072','m01s34i071','m01s34i081','m01s34i091','m01s34i092','m01s34i073','m01s05i216']
stashcodes = stashcodes + ['m01s50i082'] # lightning diagnostic
stashcodes = stashcodes + ['m01s34i001'] # ozone diagnostic
stashcodes = stashcodes + ['m01s38i525'] # black carbon diagnostic
stashcodes = stashcodes + ['m01s38i439','m01s38i440'] # ozone diagnostic
stashcodes = stashcodes + ['m01s38i371','m01s38i372','m01s38i373','m01s38i374'] # aging diagnostics
stashcodes = stashcodes + ['m01s09i203','m01s00i265','m01s00i254','m01s00i266'] # cloud fraction and liquid water path diagnostics

stashcodes =stashcodes+ ['m01s34i101','m01s34i102','m01s34i103','m01s34i104','m01s34i105','m01s34i106','m01s34i107','m01s34i108','m01s34i109','m01s34i110','m01s34i111','m01s34i112','m01s34i113','m01s34i114','m01s34i115','m01s34i116','m01s34i117','m01s34i118','m01s34i119','m01s34i120','m01s34i121','m01s34i126']
#stashcodes =stashcodes+ ['m01s00i004','m01s00i408','m01s00i033']
stashcodes = stashcodes+['m01s00i004','m01s00i408','m01s00i033']
stashcodes = stashcodes+['m01s30i453'] # height at tropopause level
stashcodes = stashcodes+['m01s34i077','m01s34i078'] # stash codes for CS2 and COS respectively
stashcodes=stashcodes+['m01s38i201','m01s38i202','m01s38i203','m01s38i204','m01s38i205','m01s38i206','m01s38i207']
stashcodes=stashcodes+['m01s38i214','m01s38i215','m01s38i216','m01s38i217','m01s38i218','m01s38i219','m01s38i220','m01s38i221','m01s38i222','m01s38i223']
stashcodes=stashcodes+['m01s38i237','m01s38i238','m01s38i239','m01s38i240','m01s38i241','m01s38i242','m01s38i243','m01s38i244','m01s38i245','m01s38i246']
stashcodes=stashcodes+['m01s38i261','m01s38i262','m01s38i263','m01s38i264','m01s38i265','m01s38i266','m01s38i267','m01s38i268','m01s38i269','m01s38i270','m01s38i271']
stashcodes=stashcodes+['m01s38i284','m01s38i285','m01s38i286','m01s38i287','m01s38i288','m01s38i289','m01s38i290','m01s38i291','m01s38i292','m01s38i293','m01s38i294','m01s38i295','m01s38i296','m01s38i297','m01s38i298']
stashcodes=stashcodes+['m01s38i319','m01s38i320','m01s38i321','m01s38i322','m01s38i323']
stashcodes=stashcodes+['m01s38i338','m01s38i339','m01s38i340','m01s38i341','m01s38i342','m01s38i343']
stashcodes=stashcodes+['m01s38i354','m01s38i356','m01s38i366','m01s38i372','m01s38i380']
stashcodes=stashcodes+['m01s38i401','m01s38i402','m01s38i403','m01s38i404','m01s38i405','m01s38i408','m01s38i409','m01s38i410','m01s38i411']
stashcodes=stashcodes+['m01s38i476','m01s38i477','m01s38i478','m01s38i479']



#diagnostics for shortwave and longwave radiation
stashcodes=stashcodes+['m01s01i205','m01s01i206','m01s01i207','m01s01i208']
stashcodes=stashcodes+['m01s01i217','m01s01i218','m01s01i219','m01s01i220']
stashcodes=stashcodes+['m01s01i517','m01s01i518','m01s01i519','m01s01i520','m01s01i521','m01s01i522']


stashcodes=stashcodes+['m01s02i205','m01s02i206','m01s02i207','m01s02i208']
stashcodes=stashcodes+['m01s02i217','m01s02i218','m01s02i219','m01s02i220']
stashcodes=stashcodes+['m01s02i517','m01s02i518','m01s02i519','m01s02i520','m01s02i521','m01s02i522']

# diagnostics to get cloud liquid fraction and CCN s38i437 is the CN diagnostic
stashcodes=stashcodes+['m01s38i438','m01s38i476','m01s38i437','m01s38i439','m01s38i440']
stashcodes=stashcodes+['m01s38i531']# OM diagnostic]
stashcodes=stashcodes+['m01s38i504','m01s38i505','m01s38i506','m01s38i507','m01s38i508','m01s38i509','m01s38i510']# aerosol mode diagnostics

stashcodes=stashcodes+['m01s00i133','m01s50i214']# DMS OCEAN FUX nanf surface emission  diagnostic

print(stashcodes)


stashcodes=stashcodes+['m01s38i201','m01s38i295','m01s38i215','m01s38i238','m01s38i290','m01s38i284','m01s38i287','m01s38i262']

stashcodes=stashcodes+['m01s38i202','m01s38i296','m01s38i216','m01s38i239','m01s38i285','m01s38i288','m01s38i263','m01s38i203','m01s38i297','m01s38i217','m01s38i240','m01s38i286','m01s38i289']

stashcodes=stashcodes+['m01s38i206','m01s38i220','m01s38i221','m01s38i222','m01s38i223','m01s38i243','m01s38i244','m01s38i245','m01s38i246','m01s38i372','m01s38i342','m01s38i366']

stashcodes=stashcodes+['m01s38i204','m01s38i205','m01s38i218','m01s38i241','m01s38i292','m01s38i380']

#nucleation diagnostics
stashcodes=stashcodes+['m01s38i574','m01s38i575','m01s38i576']

stashcodes=stashcodes+['m01s38i319']
"""
"""
stashcodes=stashcodes+['m01s50i140','m01s50i141','m01s50i142','m01s50i144','m01s50i150','m01s50i151','m01s50i152','m01s50i153','m01s50i154','m01s50i155','m01s50i215','m01s50i216','m01s50i217']
stashcodes= stashcodes+['m01s00i266']

stashcodes = stashcodes+['m01s38i301','m01s38i302','m01s38i303','m01s38i304','m01s38i305','m01s38i306','m01s38i307','m01s38i308','m01s38i309','m01s38i310','m01s38i311','m01s38i312','m01s38i313','m01s38i314','m01s50i147','m01s50i148','m01s50i149','m01s38i286','m01s34i126','m01s34i121','m01s34i110','m01s34i116','m01s34i106']

stashcodes = stashcodes+['m01s34i968','m01s34i076']

def stashInList(cell):   
    return cell in stashcodes
stashconstr = iris.AttributeConstraint(STASH=stashInList)

print date
year=date[:4]
print year
print pp_files


def from_pp_to_nc_single_var(step_file):
    print step_file
    '''define things and create folders for nc (NETCDF) files'''
    #date='20160801'
    date=step_file[len(files_directory)+dateoffset:-3]
    print date
    folder_NETCDF=files_directory+date
#step_file[len(files_directory)+len(run)+dateoffset:-6]+'/'
    ukl.create_folder(folder_NETCDF)

    '''loading cubes from pp files and saving them in their correspondent folder'''
    #cubes=iris.load(step_file)#long and heavy bit Time: around 15 minutes
    cubes=iris.load(step_file,iris.AttributeConstraint(STASH=stashInList))#long and heavy bit. Time: around 15 minutes
    print cubes
    for cube in cubes:
       #capturing stash code from pp file
        stash_code=ukl.get_stash(cube)
        if stash_code in vd.variable_reference_stash:
            if not isinstance(cube.long_name,str):
                cube.long_name=vd.variable_reference_stash[stash_code].long_name
                print 'added long_name',cube.long_name, 'to', stash_code
            if not isinstance(cube._var_name,str):
                if not vd.variable_reference_stash[stash_code].short_name=='':
                    cube._var_name=vd.variable_reference_stash[stash_code].short_name
                print 'added short_name as cube._var_name',cube._var_name, 'to', stash_code
            #if not isinstance(cube.units,str):
                #cube.units=vd.variable_reference_stash[stash_code].units
                print 'added units',cube.units, 'to', stash_code
        #check that long name exists
        if cube.long_name:
            saving_name=folder_NETCDF+'/'+date+'_'+stash_code+'_'+cube.long_name+'.nc'
        elif cube._var_name:
            saving_name=folder_NETCDF+'/'+date+'_'+stash_code+'_'+cube._var_name+'.nc'
        else:
            saving_name=folder_NETCDF+'/'+date+'_'+stash_code+'.nc'
        print'\nSAVING NAME\n\n', saving_name, '\n\n'
        iris.save(cube,saving_name, netcdf_format="NETCDF4")
        #cube=iris.load(saving_name)


jobs=[]
start=time.time()
for step_file in pp_files:
    p = multiprocessing.Process(target=from_pp_to_nc_single_var, args=(step_file,))
    jobs.append(p)
    p.start()

for job in jobs:
    job.join()

end=time.time()

print(end-start)
#sys.exit()

#file_variable_name='2008apr_m01s00i101_mass_fraction_of_sulfur_dioxide_expressed_as_sulfur_in_air.nc'
def join_variables(list_variables):
    for file_variable_name in list_variables:
        names=[]
        #print(file_variable_name, '\n')
        for imon in range(nmonths):
            print(files_directory)
            name=files_directory+year+ukl.months_str[imon]+'/'+file_variable_name[:4]+ukl.months_str[imon]+file_variable_name[7:]
            print(name, '\n')
            names.append(name)
        cube_list=[]
        cube_list=iris.load(names)
        try:
            print(cube_list[0].long_name)
        except:
            jfskjsf=1
        if 'm01s00i033' in file_variable_name:
            print('orography skipped')
            continue
        indx=0
        if len(cube_list)>1:
            if cube_list[0]==cube_list[1]:
                indx=-1
        cube_list_concatenated=cube_list[indx]
        stash_code=ukl.get_stash(cube_list_concatenated)
        if cube_list_concatenated.long_name:
            saving_name=folder_all_months+'All_months_'+stash_code+'_'+cube_list_concatenated.long_name+'.nc'
        elif cube_list_concatenated._var_name:
            saving_name=folder_all_months+'All_months_'+stash_code+'_'+cube_list_concatenated._var_name+'.nc'
        else:
            saving_name=folder_all_months+'All_months_'+stash_code+'.nc'

        iris.save(cube_list_concatenated,saving_name, netcdf_format="NETCDF4")

        cube_annual_mean=cube_list_concatenated.collapsed(['time'],iris.analysis.MEAN)

        stash_code=ukl.get_stash(cube_annual_mean)
        if cube_annual_mean.long_name:
            saving_name=folder_annual_mean+'Annual_mean_'+stash_code+'_'+cube_annual_mean.long_name+'.nc'
        elif cube_annual_mean._var_name:
            saving_name=folder_annual_mean+'Annual_mean_'+stash_code+'_'+cube_annual_mean._var_name+'.nc'
        else:
            saving_name=folder_annual_mean+'Annual_mean_'+stash_code+'.nc'
        iris.save(cube_annual_mean,saving_name, netcdf_format="NETCDF4")


folder_annual_mean=files_directory+'Annual_mean/'

folder_all_months=files_directory+'All_months/'
ukl.create_folder(folder_annual_mean)
ukl.create_folder(folder_all_months)
print(year)
#year=str(2017)
sample_month_folder=year+'jan/'
print p
list_variable_names=glob(files_directory+sample_month_folder+'*.nc')
#cut variable names
for i in range(len(list_variable_names)):
    list_variable_names[i]=list_variable_names[i][len(files_directory+sample_month_folder):]
    #print list_variable_names,'\n'
#Loop over all variables and save in annual_mean folder

processes=1
list_of_chunks=np.array_split(list_variable_names,processes)
jobs=[]
start=time.time()
for chunk in list_of_chunks:
    p = multiprocessing.Process(target=join_variables, args=(chunk.tolist(),))
    jobs.append(p)
    p.start()

for job in jobs:
    job.join()
end=time.time()
print(end-start)
