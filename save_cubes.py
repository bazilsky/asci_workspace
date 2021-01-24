import iris
import numpy as np


cube1=iris.load('bk947a.pm2017jan.pp')

print cube1[241] 
print cube1[242] 
print cube1[243] 
print cube1[244] 
print cube1[245]
print cube1[246] 

iris.save(cube1[241],"japp_lehtinen_2017.nc")
iris.save(cube1[242],"jveh_lehtinen_2017.nc")
iris.save(cube1[243],"coag3nm_lehtinen_2017.nc")
iris.save(cube1[244],"coag1nm_lehtinen_2017.nc")
iris.save(cube1[245],"m_leh_lehtinen_2017.nc")
iris.save(cube1[246],"rc_2017.nc")


cube2=iris.load('bk848a.pm2017jan.pp')

print cube2[241] 
print cube2[242] 
print cube2[243] 
print cube2[244] 
print cube2[245]
print cube2[246] 

iris.save(cube2[241],"japp_default2017.nc")
iris.save(cube2[242],"jveh_default_2017.nc")
iris.save(cube2[243],"cond_sink_2017.nc")




"""
cube2=iris.load('bk340a.pm2014jan.pp')

iris.save(cube2[241],"japp_default_new.nc")
iris.save(cube2[242],"jveh_default_new.nc")
iris.save(cube2[243],"condsink_default_new.nc")
"""
