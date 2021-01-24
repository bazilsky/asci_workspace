import numpy as np
import iris
import matplotlib.pyplot as plt

cube1 = iris.load('japp_default_new.nc')[0]
cube2 = iris.load('japp_lehtinen_rc.nc')[0]

level_num = cube1.coord('model_level_number').points
plt.figure()
plt.xlabel('Japp')
plt.ylabel('Model_level_number')
plt.plot((cube1[:,72,96].data),level_num,'b*-',(cube2[:,72,96].data),level_num,'r*-')
plt.title('Japp_both_at (0,0)')
plt.legend(('default','lehtinen'))
plt.grid(True)
#plt.show()
#plt.show()

plt.figure()
plt.xlabel('Japp_default')
plt.ylabel('Model_level_number')
plt.plot((cube1[:,72,96].data),level_num,'b*-')
plt.title('Japp_default_at (0,0)')
#plt.show()

plt.figure()
plt.xlabel('Japp_lehtinen')
plt.ylabel('Model_level_number')
plt.plot((cube2[:,72,96].data),level_num,'b*-')
plt.title('Japp_lehtinen_at (0,0)')

###############################################33
# plots of Jveh
################################################33333
cube3 = iris.load('jveh_default_new.nc')[0]
cube4 = iris.load('jveh_lehtinen_rc.nc')[0]
plt.figure()
plt.xlabel('Jveh')
plt.ylabel('Model_level_number')
level_num_all = np.arange(1,86,1)
plt.plot((cube3[:,72,96].data),level_num_all,'b*-',(cube4[:,72,96].data),level_num_all,'r*-')
plt.title('Jveh_both_at (0,0)')
plt.legend(('default','lehtinen'))
plt.grid(True)

##########################################3333333
#plot of the condensation sink in the default model
cube5 = iris.load('condsink_default_new.nc')[0]
plt.figure()
plt.xlabel('condensation sink (s-1)')
plt.ylabel('Model_level_number')
level_num_all = np.arange(1,86,1)
plt.plot((cube5[:,72,96].data),level_num_all,'b*-')
plt.title('Condensation sink at (0,0)')
plt.grid(True)

# plot of coagulation sink

cube6 = iris.load('coag3nm_lehtinen_rc.nc')[0]
cube7 = iris.load('coag1nm_lehtinen_rc.nc')[0]
plt.figure()
plt.xlabel('coagulation sink (s-1)')
plt.ylabel('Model_level_number')
level_num_all = np.arange(1,86,1)
plt.plot((cube6[:,72,96].data),level_num_all,'b*-',(cube7[:,72,96].data),level_num_all,'r*-')
plt.title('Coagulation sink at (0,0)')
plt.legend(('3nm coagsink','rc coagsink'))
plt.grid(True)


# plot of coefficient/power m

cube8 = iris.load('m_leh_lehtinen_new.nc')[0]
print cube8.data
#cube8 = np.log((cube6/cube7).data)/np.log(3.0)

plt.figure()
plt.xlabel('m (factor)')
plt.ylabel('Model_level_number')
level_num_all = np.arange(1,86,1)
plt.plot((cube8.data[:,72,96]),level_num_all,'b*-')
#plt.plot((cube8[:,72,96]),level_num_all,'b*-')
plt.title('Factor m  at (0,0)')
plt.grid(True)


"""
cube9 = iris.load('h2so4_default.nc')[0]
cube10 = iris.load('h2so4_lehtinen.nc')[0]
ppbv=pow(10,-9)
cube9_ppb  = (cube9*29/98)*ppbv 
cube10_ppb = (cube10*29/98)*ppbv

plt.figure()
plt.xlabel('h2so4 concentration(ppb)')
plt.ylabel('Model_level_number')
level_num_all = np.arange(1,86,1)
plt.plot((cube9[:,72,96].data),level_num_all,'b*-',(cube10[:,72,96].data),level_num_all,'r*-')
#plt.plot((cube9_ppb[:,72,96].data),level_num_all,'b*-',(cube10_ppb[:,72,96].data),level_num_all,'r*-')
plt.title('H2SO4 at (0,0)')
plt.grid(True)
"""

plt.show()



