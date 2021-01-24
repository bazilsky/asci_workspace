import iris
import numpy as np
import multiprocessing as nproc
import time 

"""
dir_files='/group_workspaces/jasmin2/gassp/eeara/'

file1='ax424a.pm2014apr.pp'
file2='ax424a.pm2014mar.pp'
file3='ax424a.pm2014may.pp'

file_list=[file1,file2,file3]

d=iris.cube.CubeList()
#start=time.time()
"""



def f_trial(filename):
    cube2=iris.load(filename)
    d=np.append(d,cube2[0])

#processes=20
#chunck_list=np.array_split(file_list,len(file_list)/processes+1)

if __name__ == '__main__':
    
    
    dir_files='/group_workspaces/jasmin2/gassp/eeara/'

    file1='ax424a.pm2014apr.pp'
    file2='ax424a.pm2014mar.pp'
    file3='ax424a.pm2014may.pp'

    file_list=[file1,file2,file3]

    d=iris.cube.CubeList()
    
    
    start=time.time()
    p=nproc.Pool(5)
    p.map(f_trial,[file1,file2,file3])
    end=time.time()

    print '\ntotal_time = ', end-start
    
    """
    dir_files='/group_workspaces/jasmin2/gassp/eeara/'

    file1='ax424a.pm2014apr.pp'
    file2='ax424a.pm2014mar.pp'
    file3='ax424a.pm2014may.pp'

    file_list=[file1,file2,file3]

    d=iris.cube.CubeList()

    """
"""
for chunck in chunck_list:
    jobs=[]
    for j in file_list:
        print '\n\nLooping' 
        p=nproc.Process(target=f_trial,args=(j,))
        jobs.append(p)        
        p.start()
        for job in jobs:
            job.join()

end=time.time()
print '\nFull Time = ', end-start

"""

"""

c=iris.cube.CubeList()

start=time.time()
for i in file_list:
    print '\nloop1'
    cube=iris.load(i)
    c=np.append(c,cube)

end=time.time()
print '\nTotal time --- ', end-start

"""




