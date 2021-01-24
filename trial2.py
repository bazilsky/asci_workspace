import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt
import numpy as np


cube1=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uaz660-mt_results/All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')
print 'WTFFF'
cube2=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uax337_results/All_time_steps/All_time_steps_m01s01i208_toa_outgoing_shortwave_flux.nc')
#note that cube 2 directory is somewhat different

cube3=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uaz660-mt_results/All_time_steps/All_time_steps_m01s01i517_CLEAN-AIR_UPWARD_SW_FLUX_ON_LEVELS__.nc')
cube4=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uax337_results/All_time_steps/All_time_steps_m01s01i517_CLEAN-AIR_UPWARD_SW_FLUX_ON_LEVELS__.nc')
        #note that cube 2 directory is somewhat different

