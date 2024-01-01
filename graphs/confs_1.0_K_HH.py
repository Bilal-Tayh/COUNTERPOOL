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

for c in confs:
    print(m[c])




y_cp_64_4_0_1_0 = [0.00593063, 0.0033163, 0.00185245, 0.00105642, 0.00061048, 0.000352755, 0.000224128, 0.000114475, 6.61751e-05]

y_cp_64_4_0_1_4 = [0.00593058, 0.00331622, 0.00185232, 0.00105619, 0.000610072, 0.000352014, 0.000222811, 0.000112103, 6.14316e-05]

y_cp_64_4_0_1_16 = [0.00593058, 0.00331622, 0.00185232, 0.00105619, 0.000610072, 0.000352014, 0.000222811, 0.000112103, 6.14316e-05]


y_cp_64_4_0_1_64 = [0.00593058, 0.00331622, 0.00185232, 0.00105619, 0.000610072, 0.000352014, 0.000222811, 0.000112103, 6.14316e-05]


y_cp_64_4_0_1_256 = [0.00516689, 0.00294531, 0.0016602, 0.000966076, 0.000531776, 0.000294812, 0.000160352, 9.26018e-05, 4.16113e-05]
  	

markers=['o', 'v', '<', '>','.','P']
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


# plotting the points 

i+=1
plt.plot(Thresholds, y_cp_64_4_0_1_0, marker = markers[i%(len(markers))],markersize=16)
i+=1
plt.plot(Thresholds, y_cp_64_4_0_1_4, marker = markers[i%(len(markers))],markersize=14)
i+=1
plt.plot(Thresholds, y_cp_64_4_0_1_16, marker = markers[i%(len(markers))],markersize=12)
i+=1
plt.plot(Thresholds, y_cp_64_4_0_1_64, marker = markers[i%(len(markers))],markersize=10)
i+=1
plt.plot(Thresholds, y_cp_64_4_0_1_256, marker = markers[i%(len(markers))],markersize=8)
i+=1

# naming the x axis
#plt.xlabel('ThreshHold')
# naming the y axis
plt.ylabel('ARE')

plt.grid()
plt.yscale("log")
plt.xscale("log")

plt.ylim([0, 1])
  
# giving a title to my graph
#plt.title('HeavyHitters')

plt.gca().legend(( "K=0"  , "K=4" , "K=16", "K=64" ,"K=256"))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot
plt.show()