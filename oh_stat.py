
import numpy as np 
import matplotlib.pyplot as plt
import glob as glb
import matplotlib.backends.backend_pdf as mb


home_path='/group_workspaces/jasmin2/gassp/eeara/'
path='/group_workspaces/jasmin2/gassp/eeara/oh_data/'

#filename='PEM-Tropics-A_DC8_so2_Tahiti.stat'

title=['ialt','N','min','max','mean','stddev','5%','25%','median','75%','95%']

check='mean'
pdf=mb.PdfPages(home_path+'oh_data.pdf')
n_plot=5 ##number of plots per page
grid_size=(n_plot,1)

def study(filename):
    indx=0
    for i in range(len(title)):
        if title[i]==check:
            indx=i
            break
    #load all data into a numpy array from a file
    data = np.loadtxt(filename)
    altitude=data[:,0]
    attribute=data[:,indx]
    return altitude, attribute,filename
    
files=glb.glob(path+'*_oh_*')
list_length=len(files)
nc=321
flag=0
for i in range(list_length):
    if i%n_plot==0:
        fig=plt.figure(figsize=(8.27,11.69),dpi=100)
    print 'Value of i = ', i, '\n'
    print files[i],'\n'
    alt,mean,filename=study(files[i])
    temp=plt.subplot2grid(grid_size,(i%n_plot,0))
    plt.plot(alt,mean,'b*')
    #plt.ticklabel_format(axis='x', style='sci')
    temp.set_title(filename[46:])
    plt.grid()
    if mean[0]>1:
        plt.ylabel('Conc(molecules/cm3)')
        #plt.ticklabel_format(axis='y', style='sci',scilimits=(0,0))
    else:
        plt.ylabel('Conc(pptv)')
    if (i+1)%n_plot==0:
        plt.xlabel('altitude(km)')
        pdf.savefig(fig)

pdf.close()
print '\nPROGRAM ENDED\n' 
