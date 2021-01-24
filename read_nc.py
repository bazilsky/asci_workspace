import iris
import numpy as np 
import matplotlib.pyplot as plt

file_1 = '/group_workspaces/jasmin2/asci/eeara/atom/bk947a.pi2013sep'

rc = iris.load(file_1)[0][6,0:55,:,:]

l = rc.coord('model_level_number').points
lat = rc.coord('latitude').points
rc = rc[:,0,96]
print lat[0]
plt.plot(rc.data,l,'r')
plt.title('critical radius - vertical profile')
plt.xlabel('Rc (nm)')
plt.ylabel('Model level number')
plt.grid(True)
plt.show()

