import multiprocessing as mp
import iris
def f(slice1):

    #slice1 =data.data
    print slice1


path='/group_workspaces/jasmin2/gassp/eeara/model_runs/u-bc046/L1/L1_rad_accsol_Radius_of_mode_accsol.nc'
cube=iris.load(path)
cube=cube[0]
data=cube.data
p=mp.Process(target=f,args=(data,))
p.start()

