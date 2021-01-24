import numpy as np
from netCDF4 import Dataset

data = Dataset('m01s38i401_20130904.nc')

time    = np.asarray(data['time'])
dry_dia = np.asarray(data['model_data'])

print dry_dia
print data
