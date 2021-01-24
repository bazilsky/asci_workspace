import iris,glob
import numpy as np
import scipy as sp
import numpy.ma as ma
import matplotlib.pyplot as plt
import iris.coord_systems as cs
from gridded_interpolation import _RegularGridInterpolator
import datetime
import pandas as pd
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import matplotlib.colors as cols
import matplotlib.cm as cmx
import matplotlib._cntr as cntr
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import LogNorm
from matplotlib.collections import LineCollection
import matplotlib
#import error_calc

path='/nfs/a201/earhg/CLOUD/nitrate-nc/'
atom_names = glob.glob(path+'ananth-atom-files/all_points_2016*.nc')
frames = []
points=[]
i=0
for atom_name in atom_names:
    atom_lon=iris.load_cube(atom_name,'longitude')
    atom_lat=iris.load_cube(atom_name,'latitude')
    atom_alt=iris.load_cube(atom_name,'altitude')
    atom_ntot =iris.load_cube(atom_name,'N_tot')
    atom_acc=  iris.load_cube(atom_name,'N_acc')
    atom_time = iris.load_cube(atom_name,'time')
    print atom_name,atom_time.data[0]

    times_of_flight=pd.to_datetime(3600*atom_time.data, unit='s')
    print times_of_flight[0]
    times_of_flight1=3600*atom_time.data
    #print times_of_flight1
    for ipoint in range(0,len(atom_lat.data)):
        #print times_of_flight[ipoint]
        if atom_lon.data[ipoint]>0:
            points.append([times_of_flight1[ipoint],atom_lon.data[ipoint],atom_lat.data[ipoint],atom_alt.data[ipoint]])
        else:
            points.append([times_of_flight1[ipoint],atom_lon.data[ipoint]+360.0,atom_lat.data[ipoint],atom_alt.data[ipoint]])
        d= {'time':pd.Series(times_of_flight), 'latitude':pd.Series(atom_lat.data),'longitude':pd.Series(atom_lon.data),
            'altitude':pd.Series(atom_alt.data),'ntot':pd.Series(atom_ntot.data),'nacc':pd.Series(atom_acc.data)}
    mydf = pd.DataFrame(d)
    frames.append(mydf)
    i=i+1
#print points
df= pd.concat(frames)
print df.head()

tomcat_name = path+'N3_baseline_110617_ATom1_daily.nc'
tomcat_cn = iris.load_cube(tomcat_name,'n3_baseline_pd')

aird_name = path+'air_density_baseline_110617_ATom1_daily.nc'
air_density = iris.load_cube(aird_name,'air_density')



def lognormal_cumulative(N,r,rbar,sigma):
    total=(N/2)*(1+sp.special.erf(np.log(r/rbar)/np.sqrt(2)/np.log(sigma)))
    return total

tomcat_nd_file = path+'mode_number_mass_except_dust_110617_ATom1_daily.nc'
tomcat_nd = iris.load_cube(tomcat_nd_file,'number_mixing')
tomcat_rbar = iris.load_cube(tomcat_nd_file,'rbardry')
print tomcat_nd
tomcat_Ait = tomcat_nd[:,:,:,:,1]
tomcat_acc = tomcat_nd[:,:,:,:,2]
tomcat_rAit = tomcat_rbar[:,:,:,:,1]
tomcat_racc = tomcat_rbar[:,:,:,:,2]
tomcat_acc60 = tomcat_acc+tomcat_Ait-tomcat_Ait.copy(lognormal_cumulative(tomcat_Ait.data,6e-8,tomcat_rAit.data,1.59))

pref=1.013E5
tref=273.0 #ATOM standard T is 0C.
zboltz=1.3807E-23
staird=pref/(tref*zboltz*1.0E6)
tomcat_cn_stp = tomcat_cn*staird/air_density
tomcat_Ait_stp = tomcat_Ait*staird/air_density
tomcat_acc_stp = tomcat_acc*staird/air_density
tomcat_acc60_stp = tomcat_acc60*staird/air_density
#print tomcat_cn.coord('longitude')

tomcat_altitudes= path+'grid_box_volume_for_weighting_110617_ATom1_daily.nc'
tomcat_alts = iris.load_cube(tomcat_altitudes,'atmosphere_hybrid_height_coordinate')
reversed_alts3d= 1e-3*tomcat_alts.data[::-1,::-1,:]
altitude_hybrid = iris.coords.AuxCoord(reversed_alts3d,'altitude', units='km')

def format_cube(cube, alt_hybrid):
    reversed_cn_data = cube.data[:, ::-1,::-1,:]
    reversed_alt = tomcat_cn.coord('alt').points[::-1]
    new_alts = iris.coords.DimCoord(reversed_alt,long_name='alt',units='km')
    #print reversed_alts
    glomap_cn = tomcat_cn.copy(reversed_cn_data)
    reversed_lats = tomcat_cn.coord('latitude').points[::-1]
    new_lats = iris.coords.DimCoord(reversed_lats,'latitude')
    glomap_cn.remove_coord('latitude')
    glomap_cn.add_dim_coord(new_lats, 2)
    glomap_cn.remove_coord('alt')
    glomap_cn.add_dim_coord(new_alts, 1)
    #new_altitude = iris.coords.DimCoord(1e3*tomcat_cn.coord('alt').points,long_name='level_height',units='m')
    #tomcat_cn.remove_coord('alt')
    #tomcat_cn.add_dim_coord(new_altitude,1)
    #print tomcat_cn
    #factory = iris.aux_factory.HybridHeightFactory(delta=tomcat_cn.coord('level_height'),orography=iris.coords.AuxCoord(tomcat_hasl.data,'surface_altitude',units='m'))
    #print factory.name()
    #factory.rename('atmosphere_hybrid_height_coordinate')
    #tomcat_cn.add_aux_factory(factory)

    glomap_cn.add_aux_coord(alt_hybrid, (1,2,3))
    #print glomap_cn
    return glomap_cn



def do_interpolation(cube, cubelist, points):
    cubedimcoords=[]
    cubedatasets=[]
    tomcat_times1 = glomap_cn.coord('month').points #[cell.point for cell in tomcat_cn.coord('month').cells()]
    months=[7,7,7,7]
    [months.append(8) for i in range(0,24)]
    days = [28,29,30,31]
    [days.append(i) for i in range(1,25)]
    hours = [12 for i in range(0,28)]
    minutes= [0 for i in range(0,28)]

    cube_times = pd.to_datetime({'year':[2016 for i in tomcat_times1],'month':months,'day':days, 'hour':hours,'minute':minutes}, unit='s').astype(int)/1e9
    cube_times1 = [ cube_times[i] for i in range(0,len(cube_times))]
    print cube_times
    if cube.ndim==4:
        cubedimcoords.append(cube_times)
        for cube_to_interp in cubelist:
            cubedatasets.append(np.transpose(cube_to_interp.data,(0,3,2,1)))
            print cube_to_interp
    else:
        for cube_to_interp in cubelist:
            cubedatasets.append(cube_to_interp.data.T)
    cubedimcoords.append(cube.coord('longitude').points)
    cubedimcoords.append(cube.coord('latitude').points)
    cubedimcoords.append(cube.coord('alt').points)
    print cube.coord('alt').points
    print 'interpolator hybrid_dim args',cube.coord_dims(cube.coord('altitude'))
    # complicated version of interpolator that handles topography. Credit to Duncan Watson-Parris (cis) and scitools                   
    interpolator=_RegularGridInterpolator(cubedimcoords,np.asarray(points).T, hybrid_coord =cube.coord('altitude').points.T,hybrid_dims=cube.coord_dims(cube.coord('altitude')),method='nn')
    interp_results=[]
    for dataset_to_interp in cubedatasets:
        interp_results.append(np.asarray(interpolator(dataset_to_interp, fill_value=None)))
    return interp_results

def add_times_to_plot(df):
    for itime in range(0,len(df.altitude)):
        hours = df.index.hour
        minutes= df.index.minute
        seconds = df.index.second
        if minutes[itime]==0 and seconds[itime]==0:
            plt.plot(df.longitude[itime],df.latitude[itime],marker='|',markersize=3,color='black')
            if hours[itime] < 10:
                timestring = '0'+str(hours[itime])+':00'
            else:
                timestring = str(hours[itime])+':00'

            plt.text(df.longitude[itime],df.latitude[itime],timestring, fontsize=12)

def add_flight_track_to_latlon(ax,norm,cmap,variable,dataframe):
    points = np.array([dataframe.longitude, dataframe.latitude]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap,norm=norm)
    lc.set_array(np.asarray(variable))
    lc.set_linewidth(2)
    ax.add_collection(lc)
    add_times_to_plot(dataframe)
def horizontalplot(ax, cube,minv,maxv,norm):
    if norm !=None:
        pl =  iplt.pcolormesh(cube,vmin=minv,vmax=maxv,norm=norm)
    else:
        pl =  iplt.pcolormesh(cube,vmin=minv,vmax=maxv)
    pl.cmap.set_under('k')
    plt.gca().stock_img()
    plt.gca().coastlines(resolution='50m')
    ax.set_xlim(lonmin,lonmax)
    ax.set_ylim(latmin,latmax)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), linestyle='-',draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter(LONGITUDE_FORMATTER)
    gl.yformatter(LATITUDE_FORMATTER)

##make plots                                                                                                                                
def plot_comparison(df,xvalue,obs_col,lam_col,glm_col,ylabel,var_min,var_max,is_log,norm_array,plot_another_line):
    #plt.figure()
    #plt.subplot(212)
    df['ratio'] = df[lam_col]/df[obs_col]
    all_ratios = df['ratio'].as_matrix()
    print 'number of simulated points below 50% of obs',np.count_nonzero(all_ratios < 0.5),'out of',np.count_nonzero(all_ratios)
    print 'number of simulated points above 100% of obs',np.count_nonzero(all_ratios > 2.0),'out of',np.count_nonzero(all_ratios)
    print 'number of simulated points below 20% of obs',np.count_nonzero(all_ratios < 0.2),'out of',np.count_nonzero(all_ratios)
    print 'number of simulated points above 500% of obs',np.count_nonzero(all_ratios > 5.0),'out of',np.count_nonzero(all_ratios)
    print 'NMBF',1-np.sum(df[obs_col].as_matrix())/np.sum(df[lam_col].as_matrix()),'the other NMBF',np.sum(df[lam_col].as_matrix())/np.sum(df[obs_col].as_matrix())-1
    print 'mean model',np.mean(df[lam_col].as_matrix()),'mean obs',np.mean(df[obs_col].as_matrix())
    ax = df.plot(kind='scatter',x=xvalue,y=obs_col,c=df['altitude'],logy=is_log,ylim=(var_min,var_max),label='Obs.',style='o',colormap='coolwarm',colorbar=True)
    ax2 = df.plot(kind='scatter',x=xvalue,y=obs_col,c=df['ratio'], logy=is_log,ylim=(var_min,var_max),label='Model',style='o',norm=LogNorm(),colormap='coolwarm',colorbar=True,vmin=0.1,vmax=10)
    if plot_another_line==1:
        df.plot(kind='scatter',x=xvalue,y=glm_col,logy=is_log,ylim=(var_min,var_max),label='Acc60',ax=ax,style='o')
    ax2.set_ylabel(ylabel)
    ax2 = df.plot(kind='scatter',x=xvalue,y=lam_col,c=df['ratio'], logy=is_log,ylim=(var_min,var_max),label='Model',style='o',norm=LogNorm(),colormap='coolwarm',colorbar=True,vmin=0.1,vmax=10)
    
    #plt.scatter(df[xvalue].as_matrix(),df[lam_col].as_matrix(),c=df['ratio'].as_matrix(),norm=LogNorm())
    #ax3 = df.plot(kind='scatter',x=xvalue,y='altitude',secondary_y=True,label='Altitude',ax=ax,style='o')
    #ax3.set_ylabel('Altitude (m)')

    #h2,l2 = ax2.get_legend_handles_labels()
    #h3,l3 = ax3.get_legend_handles_labels()
    #plt.legend(h2+h3,l2+l3)#,bbox_to_anchor=(1.0, 1.4))
def nmbf(model_data,obs_data):
    bias = []
    denom = []
    numerator = []
    flag = np.mean(model_data)>=np.mean(obs_data)
    if flag == True:
        bias = (model_data - obs_data)/obs_data
    else:
        bias = (model_data - obs_data)/model_data
    return bias 

def plot_vertical_profile(df, xvalue_obs,xvalue_model):

    lat1=[0.0   ,25.0  ,65.0     ]
    lat2=[25.0  ,65.0  ,90.0     ]
    lat3=[-25.0 ,-65.0 ,-90.0    ]
    lat4=[0.0   ,-25.0 ,-65.0    ]
    plot_name = ['Tropics','Midlatitudes','Highlatitudes']
    plot_indx=[231,232,233]
    plot_indx2=[234,235,236]
    plt.figure(figsize=(12,10))
    matplotlib.style.use('ggplot')
    
    
    all_obs = df[xvalue_obs].as_matrix()
    all_model = df[xvalue_model].as_matrix()
    print 'this is the length'
    print len(all_obs),len(all_model)
    all_latitudes  = df['latitude'].as_matrix()
    all_altitudes = df['altitude'].as_matrix()
     
    for r in range(len(lat1)):
        #model_highlat = all_model[np.logical_or(all_latitudes > 60,all_latitudes < -60)]
        lat_pos= np.where(np.logical_or(np.logical_and(all_latitudes > lat1[r],all_latitudes < lat2[r]),np.logical_and(all_latitudes>=lat3[r],all_latitudes<=lat4[r])))
        model_arr = all_model[lat_pos].copy()
        obs_arr = all_obs[lat_pos].copy()
        alt_arr = all_altitudes[lat_pos].copy()
        lat_arr = all_latitudes[lat_pos].copy()

        bin_size = 1.0
        lim1 = 0.0
        lim2 = lim1+bin_size

        alt_val = []
        model_25=[]
        model_50=[]
        model_75=[]
        obs_25=[]
        obs_50=[]
        obs_75=[]
        bias_25=[]
        bias_50=[]
        bias_75=[]
        bias_slice=[]

        while (lim2<14.0): # maximum altitude 14km
            pos=np.where(np.logical_and(alt_arr>=lim1, alt_arr<=lim2))
            model_slice = model_arr[pos].copy()
            obs_slice = obs_arr[pos].copy()
            lat_slice = lat_arr[pos].copy()
            alt_slice = alt_arr[pos].copy()
            bias_slice = nmbf(model_slice,obs_slice)
            if len(alt_slice)!=0:
                alt_val = np.append(alt_val,np.mean(alt_slice))
                
                obs_25 = np.append(obs_25,np.percentile(obs_slice,25))
                obs_75 = np.append(obs_75,np.percentile(obs_slice,75)) 
                obs_50 = np.append(obs_50,np.percentile(obs_slice,50))
                model_25 = np.append(model_25,np.percentile(model_slice,25))
                model_75 = np.append(model_75,np.percentile(model_slice,75)) 
                model_50 = np.append(model_50,np.percentile(model_slice,50))
                bias_25 = np.append(bias_25,np.percentile(bias_slice,25))
                bias_75 = np.append(bias_75,np.percentile(bias_slice,75))
                bias_50 = np.append(bias_50,np.percentile(bias_slice,50))
            lim1 = lim1+bin_size
            lim2 = lim2+bin_size
        plt.subplot(plot_indx[r])
        plt.grid(True)
        #plt.fill_betweenx(alt_val,obs_25,obs_mean,color='b',alpha=.2,)
        
        plt.fill_betweenx(alt_val,obs_25,obs_75,color='k',alpha=.2,)
        plt.fill_betweenx(alt_val,model_25,model_75,color='g',alpha=.2,)
        
        
        plt.plot(obs_50,alt_val,'k',linewidth=1.0)
        plt.plot(model_50,alt_val,'g',linewidth=1.0)
        #plt.plot(new_50_3,alt_val,'b',linewidth=1.0)
        
        #plt.fill_betweenx(alt_val,bias1_25,bias1_75,color='y',alpha=.2,)
        #plt.plot(bias1_50,alt_val,'y',linewidth=1.0)
        #plt.plot(old_75,alt_val,'r-.')
        # this code is to shrink the plot ###################### 
        ax = plt.gca() # this gets the axis of the current data 
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height*0.09,box.width, box.height*0.99])
        
        
        label = ax.set_xlabel('N_total(cm-3)',fontsize = 10)
        if r==0:
            plt.ylabel('Altitude (km)')
            #plt.xlabel('Ntot (cm-3)',loc='center')
        plt.title(plot_name[r])
       # plt.xlim([10,2e5]) 
        plt.xscale('log') 
        plt.subplot(plot_indx2[r]) 
        plt.title(plot_name[r])
        plt.fill_betweenx(alt_val,bias_25,bias_75,color='g',alpha=.2,)
        plt.plot(bias_50,alt_val,'g',linewidth=1.0)
        #if r<3:
        #    plt.xlim([-11,15])
        #plt.xlim([-5,10])
        ax = plt.gca() # this gets the axis of the current data 
        box = ax.get_position()
        #ax.set_position([box.x0, box.y0 + box.height*0.05,box.width, box.height*0.95])
        
        
        label = ax.set_xlabel('Normalised mean Bias Factor',fontsize = 10)
        if r==0:
            plt.ylabel('Altitude (km)')
        #plt.title(plot_name[r])
glomap_cn = format_cube(tomcat_cn_stp, altitude_hybrid)
glomap_ait= format_cube(tomcat_Ait_stp, altitude_hybrid)
glomap_acc = format_cube(tomcat_acc_stp, altitude_hybrid)
glomap_acc60 =format_cube(tomcat_acc60_stp, altitude_hybrid)
[df['model_ntot'],df['model_acc'],df['model_acc60']] = do_interpolation(glomap_cn,iris.cube.CubeList([glomap_cn,glomap_acc,glomap_acc60]), points)
#print df
norm_array_c10h16=[200,500,1000,2000,5000,10000,20000]
plot_comparison(df,'latitude','ntot','model_ntot','model_ntot','Num/cc', 100,10000.0, True,norm_array_c10h16,0)
plot_vertical_profile(df,'ntot','model_ntot')

plot_comparison(df,'latitude','nacc','model_acc60','model_acc60','Num/cc', 50,4000.0, True,norm_array_c10h16,0)

plt.show()
