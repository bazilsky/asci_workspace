



import numpy as np 
import iris


file1 = '/group_workspaces/jasmin2/gassp/eeara/2008/bb295a.pm2008apr.pp'
file2 = '/group_workspaces/jasmin2/gassp/eeara/ba471a.p42014apr.pp'
name1=[]
name2=[]
print 'start'
cube1=iris.load(file1)
print '\ncube1 completed\n'
cube2=iris.load(file2)
print 'completed'

for i in cube1:
    name1=np.append(name1,i.name())


for j in cube2:
    name2=np.append(name2,j.name())


