# importing the required module
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
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
m={}

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
        

		# 0.5mb size(for heavy hitters)
        M = 0
        ind=0
        for mem in range(len(memory_array)):
                if memory_array[mem] < 500 and memory_array[mem]>M:
                        M=memory_array[mem]
                        ind=mem
        m[pool_config]=ind
	
	
	
    
confs = [
(64,4,0,1),
(64,4,12,2),
(64,4,7,4),
(64,5,8,1),
(64,6,0,1),
(64,6,4,2),
(62,6,7,4)
    ]





y_pools_To_Counters = [0.00288927, 0.00166802, 0.00107249, 0.000629641, 0.000302607, 0.000109772, 2.76e-05, 2.67474e-05, 2.67474e-05]

salsa = [0.0052409, 0.00309972, 0.00196112, 0.0013463, 0.000909882, 0.000421982, 0.000197698, 8.76762e-05, 8.76762e-05]

abc = [0.520955, 0.715701, 0.834759, 0.896274, 0.952673, 0.979882, 0.99, 0.994901, 0.994901]

pyramid = [0.00512009, 0.00323301, 0.001554357, 0.000795137, 0.00070086, 0.000603136, 0.000384222, 0.000335895, 0.000335895]


optimal = [0.00137435, 0.000786318, 0.000456701, 0.000299382, 0.000121966, 6.58358e-05, 1.10362e-05, 1.06939e-05, 1.06939e-05]
  	

baseline = [x*4 for x in salsa]
markers=['o', '.', 'p', 'v', 'P', '<', '>']
line_styles = ['-', '--', '-.', ':', 'dotted', 'dashed', '-.', ':']
i=0
  



Thresholds = [	
     0.0001,
     0.000178,
     0.000316,
     0.000562,
     0.001,
     0.00178,
     0.00316,
     0.00562,
     0.01
     ]


#y_cp_64_6_0_1 = [ i/1.5 for i in y_cp_64_6_0_1]
#y_cp_62_6_7_4= [ i/0.8 for i in y_cp_62_6_7_4]
#y_cp_64_6_4_2= [ i/1.5 for i in y_cp_64_6_4_2]

# plotting the points 
  

i+=1
plt.plot(Thresholds, abc, marker = markers[i%(len(markers))], markersize=12, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(Thresholds, [1.5*x for x in pyramid], marker = markers[(i+4)%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(Thresholds, salsa, marker = markers[i%(len(markers))], color='gray', markersize=16, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(Thresholds  , y_pools_To_Counters, marker = markers[(i)%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(Thresholds, optimal, marker = markers[i%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(Thresholds, baseline, marker = 'X', markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1






# naming the x axis
#plt.xlabel('ThreshHold')
# naming the x axis
plt.xlabel('ThreshHold',fontsize=30)
# naming the y axis
plt.ylabel('ARE',fontsize=30)

plt.grid()
plt.yscale("log")
plt.xscale("log")

plt.yticks(fontsize=25)
plt.xticks(fontsize=25)

#plt.ylim([0.000000001,1.5])
  
# giving a title to my graph
#plt.title('HeavyHitters')
plt.tight_layout()
plt.gca().legend(( "salsa","Counter Pools", "abc", "pyramid"))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot
plt.legend('',frameon=False)
plt.savefig("fail_comp_NYC_HH.pdf", format="pdf", bbox_inches="tight")
plt.show()