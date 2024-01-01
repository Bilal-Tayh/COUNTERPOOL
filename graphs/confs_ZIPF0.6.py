#import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
from math import log, ceil
import numpy as np
import sys
import itertools
import math
from matplotlib.legend_handler import HandlerErrorbar
from matplotlib import container
import copy
import pylab



###############################################################################
############################################################################### 

def numeric_binomial(n,k):
   c = 1
   for i in range(1,k+1):
       c *= n-(k-i)
       c /= i
   return c
   
def nSAB(x,y):
   return numeric_binomial(x+y-1,y-1)

###############################################################################
############################################################################### 

confs = [
	#8b overhead
	(64,4,12,2),
	(64,4,9,3),
	(64,4,7,4),
	(61,5,5,6), #210*3B = 630B lookup (encode the starting positions of counter 2-5)
	(64,5,8,4), #210*3B = 630B lookup (encode the starting positions of counter 2-5)
	(62,6,7,4), #252*4B = 1KB lookup (encode the starting positions of counter 2-6)
	#16b overhead
	(64,5,0,2), #One lookup for (size,offset) computation # 58905*3B=175KB lookup (encode the starting positions of counter 2-5)
	(64,6,4,2), #One lookup for (size,offset) computation # 210*4B=175KB lookup (encode the starting positions of counter 2-6)
	(64,6,0,3), #One lookup for (size,offset) computation #(if counters are restricted to 40 bits or so), 210*4B=175KB lookup (encode the starting positions of counter 2-6)
	(64,7,0,4), #One lookup for (size,offset) computation #(if counters are restricted to 32 bits or so), 53592*5B=260KB lookup (encode the starting positions of counter 2-6)
	(64,5,7,1), #One lookup for (size,offset) computation #per pool & 40920*3B = 120KB lookup (encode the starting positions of counter 2-5)
	(64,5,8,1), #Magic Division + One lookup for (size,offset) computation #per pool & 2925*3B = 9KB lookup (encode 22 size options for counter 1 (8-29) bits multiplied by SAB(24,4)) OR 20475*3B=60KB lookup table for SAB(24,5)
	(64,6,8,2), #One lookup for (size,offset) computation #per pool & 20349*4B = 80KB lookup (encode the starting positions of counter 2-6)
	(64,4,0,1), #
	#20b overhead
	(64,5,0,1),
	#24b overhead
	(64,6,0,1),
]


Height = 4
widths_array = [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]

d = {}

for pool_config in confs:
        
        (pool_bit_size, counters_per_pool, initial_counter_size, counter_bit_increase) = pool_config

           
        factor = (float(pool_bit_size/8.0)/counters_per_pool)
        
        (ps, n, s, j) = pool_config
        
        cs0 = nSAB(np.ceil((ps-n*s)/j),n) 
        
        overhead_per_pool = float(np.ceil(np.log2(cs0)/8))
        
        if (64, 7, 0, 4) == pool_config:
            overhead_per_pool = 2.0
        
        #print(pool_config, overhead_per_pool)
                       
        memory_array = [width*Height*(factor+overhead_per_pool/counters_per_pool)/1024.0 for width in widths_array]
        
        d[pool_config] = memory_array
salsa_Memory = [width*Height*9/(8*1024.0) for width in widths_array]
	
	
	
    



y_cp_64_4_0_1 = [0.00129271, 0.000506265, 0.000191465, 9.4541e-05, 4.65121e-05, 2.2763e-05, 1.10673e-05, 5.32958e-06, 2.5355e-06, 1.18525e-06, 5.41782e-07, 2.39878e-07]

y_cp_64_4_7_4 = [0.000844309, 0.000414316, 0.000200616, 9.4541e-05, 4.65121e-05, 2.2763e-05, 1.10673e-05, 5.32958e-06, 2.5355e-06, 1.18525e-06, 5.41782e-07, 2.39878e-07]


y_cp_64_4_12_2 = [0.000844309, 0.000414316, 0.000200616, 9.4541e-05, 4.65121e-05, 2.2763e-05, 1.10673e-05, 5.32958e-06, 2.5355e-06, 1.18525e-06, 5.41782e-07, 2.39878e-07]


y_cp_64_5_8_1 = [
    0.00165375,
    0.000810488,
    0.000385148,
    0.000173498,
    6.7321e-05,
    2.27793e-05,
    1.10673e-05,
    5.32958e-06,
    2.5355e-06,
    1.18525e-06,
    5.41782e-07,
    2.39878e-07
]


y_cp_64_6_0_1 = [
    0.00232381,
    0.00115103,
    0.000567536,
    0.000274487,
    0.000128749,
    5.61252e-05,
    1.99084e-05,
    5.50397e-06,
    2.53551e-06,
    1.18525e-06,
    5.41782e-07,
    2.39878e-07
]


y_cp_64_6_4_2 = [
    0.0023207,
    0.00114976,
    0.000564001,
    0.000270126,
    0.000123353,
    4.98829e-05,
    1.36732e-05,
    6.22088e-06,
    2.53551e-06,
    1.18525e-06,
    5.41782e-07,
    2.39878e-07
]


y_cp_62_6_7_4 = [0.00232339, 0.00115232, 0.000566784, 0.000273605, 0.000127689, 5.49607e-05, 1.87556e-05, 5.34113e-06, 2.53663e-06, 1.18551e-06, 5.41796e-07, 2.39878e-07]


salsa =  [0.00287239, 0.00129587, 0.000509684, 0.00019047, 9.35622e-05, 4.55432e-05, 2.18152e-05, 1.01375e-05, 4.42744e-06, 1.66772e-06, 5.59345e-07, 2.4129e-07]

  	

markers=['o', '.', 'p', 'v', 'P', '<', '>']
line_styles = ['-', '--', '-.', ':', 'dotted', 'dashed', '-.', ':']

i=0
  

xlabel = 'Memory[KB]'
ylabel = 'OnArrival NRMSE'
fig, ax1 = plt.subplots(1,1)
ax1.set_ylabel(ylabel, fontsize=20)
ax1.set_xlabel(r'Memory[KB]', fontsize=20)



i+=1
plt.plot(d[(64,4,0,1)], y_cp_64_4_0_1, marker = markers[i%(len(markers))],markersize=18, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(d[(64,4,7,4)], y_cp_64_4_7_4, marker = markers[i%(len(markers))],markersize=14, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(d[(64,4,12,2)], y_cp_64_4_12_2, marker = markers[i%(len(markers))],markersize=12, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(d[(64,5,8,1)], y_cp_64_5_8_1, marker = markers[i%(len(markers))],markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(d[(64,6,0,1)], y_cp_64_6_0_1, marker = markers[i%(len(markers))],markersize=8, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(d[(64,6,4,2)], y_cp_64_6_4_2, marker = markers[i%(len(markers))],markersize=8, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(d[(62,6,7,4)], y_cp_62_6_7_4, marker = markers[i%(len(markers))],markersize=4, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
#plt.plot(salsa_Memory, salsa, marker = markers[i%(len(markers))],markersize=10)
i+=1



# i+=1
# ax1.errorbar(d[(64,4,0,1)], y_cp_64_4_0_1,label ='64_4_0_1' ,marker = markers[i%(len(markers))],markersize=18, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# ax1.errorbar(d[(64,4,7,4)], y_cp_64_4_7_4,label ='64_4_7_4', marker = markers[i%(len(markers))],markersize=14, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# ax1.errorbar(d[(64,4,12,2)], y_cp_64_4_12_2,label ='64_4_12_2', marker = markers[i%(len(markers))],markersize=12, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# ax1.errorbar(d[(64,5,8,1)], y_cp_64_5_8_1,label ='64_5_8_1', marker = markers[i%(len(markers))],markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# ax1.errorbar(d[(64,6,0,1)], y_cp_64_6_0_1,label ='64_6_0_1', marker = markers[i%(len(markers))],markersize=8, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# ax1.errorbar(d[(64,6,4,2)], y_cp_64_6_4_2,label ='64_6_4_2', marker = markers[i%(len(markers))],markersize=8, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# ax1.errorbar(d[(62,6,7,4)], y_cp_62_6_7_4,label ='62_6_7_4', marker = markers[i%(len(markers))],markersize=4, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# #plt.plot(salsa_Memory, salsa, marker = markers[i%(len(markers))],markersize=10)
# i+=1







plt.yticks(fontsize=25)
plt.xticks(fontsize=25)

#plt.ylim([0.0000000001,10])
# naming the x axis
plt.xlabel('Memory[KB]',fontsize=30)
# naming the y axis
plt.ylabel('OnArrival NRMSE',fontsize=30)

plt.grid()
plt.yscale("log")
plt.xscale("log")
plt.tight_layout()
# giving a title to my graph
#plt.title('OnArrival')

#plt.gca().legend(( "(64,4,0,1)"  , "(64_4_7_4)" , "(64_4_12_2)", "(64_5_8_1)" ,"(64_6_0_1)" , "(64_6_4_2)" , "(62_6_7_4)"))

plt.gca().legend(( "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot

plt.legend('',frameon=False)
plt.savefig("confs_0.6.pdf", format="pdf", bbox_inches="tight")








# handles, labels = ax1.get_legend_handles_labels()
# handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]

# figlegend=pylab.figure()
# pylab.figlegend(*(handles,labels), fontsize=10, loc = 'upper left', ncol=4)
# figlegend.savefig("legend.pdf",format = 'pdf', bbox_inches='tight')
