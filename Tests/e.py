# importing the required module
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import pylab

  
# x axis values
xi = [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536,131072,262144,524288,1048576]
x1 = [i/(9*1024) for i in xi]
x2 = [i/(18*1024) for i in xi]
# corresponding y axis values
y_1 = [
48,
62,
79,
91,
105,
116,
121,
127
]










y_2 = [
60,
92,
110,
121,
129,
139,
138,
137
]


x = [110, 115 , 120, 125 , 130, 135, 140, 145]


 

#y_cp_64_4_12_2_nf_4 = [
#0.000551504,
#9.63527e-05,
#3.87986e-05,
#1.67128e-05,
#7.06666e-06,
#2.90274e-06,
#1.15965e-06,
#4.54846e-07,
#1.77719e-07,
#6.93781e-08,
#2.64618e-08,
#9.63825e-09
#]






x = [x1*200*100000 for x1 in ([0.1, 0.2, 0.3, 0.4, 0.5, 1, 1.5, 2, 3, 4])]



x_pools = [  11274289152/(i*32) for i in x]
x_cuckoo = [  11274289152/(i*32) for i in x]

y_1 = [20.5, 45.25, 52.0, 63.75, 65.5, 70.0, 74.5, 79.0, 90.0, 91.0]
y_2 = [30.5, 40.25, 52.6, 66.5, 70.4, 79.0, 84.0, 89.0, 98.0, 100.0]


y_pools = y_2

	
y_cuckoo = y_1

y_fast = [59.5, 52.95, 53.85, 57.0, 60.15, 64.5, 68.1, 71.85, 79.05, 83.3]
y_set = [41.9, 24.5, 28.3, 32.9, 37.5, 49.5, 54.0, 60.0, 74.0, 83.25]

y_set = [i/1.2 for i in y_set]

x = [i/50 for i in x_pools]
print(x)

# plotting the points 
plt.plot(x, y_1)
plt.plot(x, y_2)
plt.plot(x, y_fast)
plt.plot(x, y_set)



# naming the x axis
plt.xlabel('Size/Flows')
# naming the y axis
plt.ylabel('throuput [1M/Sec]')
  
# giving a title to my graph

plt.gca().legend(('Cuckoo', 'Cuckoo_cp', 'Robin Hood map', 'unordered map'))


plt.xlim([0,1])

plt.grid()

# function to show the plot
plt.show()
plt.savefig("cuckoo.pdf", format="pdf", bbox_inches="tight")
