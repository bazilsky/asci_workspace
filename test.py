import numpy as np
import matplotlib.pyplot as plt

x1 = [1,2,3]
x2 = [1.4,3.6,3.1]

y = [1,2,6]
plt.plot(x1,y,'b*')
plt.plot(x2,y,'b*')

plt.fill_betweenx(y,x1,x2,color='r',alpha=.2,label = 'observation')
#plt.yticks(np.arange(3),('1','2','3'))
plt.yticks([1,2,3,4,5,6])
plt.show()
