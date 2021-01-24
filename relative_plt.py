

import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt

cube1=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uax428-mt_results/L1/L1_ccn0.4_Cloud_condensation_nuclei_at_a_supersaturation_of_0.4000.nc')
cube2=iris.load('/group_workspaces/jasmin2/gassp/eeara/new_uax424_results/L1/L1_ccn0.4_Cloud_condensation_nuclei_at_a_supersaturation_of_0.4000.nc')

c1=cube1[0].collapsed(['time'],iris.analysis.MEAN)
c2=cube2[0].collapsed(['time'],iris.analysis.MEAN)


c1=c1.collapsed(['model_level_number'],iris.analysis.MEAN)
c2=c2.collapsed(['model_level_number'],iris.analysis.MEAN)

newcube=((c2-c1)/c1)*100
qplt.contourf(newcube,85)
plt.title('Percentage change in CCN concentration at SS = 0.4')
plt.gca().coastlines()
plt.savefig('fig2.pdf')
plt.show()
