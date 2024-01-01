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
	
	
	
    



y_cp_64_4_0_1 = [
    5.14795e-06,
    4.69744e-06,
    4.40688e-06,
    4.18932e-06,
    4.01426e-06,
    3.8681e-06,
    3.74054e-06,
    3.62862e-06,
    3.52891e-06,
    3.39539e-06
]

y_cp_64_4_7_4 = [
    5.14795e-06, 4.69744e-06, 4.40688e-06, 4.18932e-06, 4.01426e-06,
    3.8681e-06, 3.74054e-06, 3.62862e-06, 3.52891e-06, 3.39539e-06
]

y_cp_64_4_12_2 = [
    5.14795e-06, 4.69744e-06, 4.40688e-06, 4.18932e-06, 4.01426e-06,
    3.8681e-06, 3.74054e-06, 3.62862e-06, 3.52891e-06, 3.39539e-06
]


y_cp_64_5_8_1 = [
    5.14795e-06, 4.69744e-06, 4.40688e-06, 4.18937e-06, 4.01432e-06,
    3.86824e-06, 3.74085e-06, 3.62914e-06, 0.00125147, 0.00185497
]


y_cp_64_6_0_1 = [
    5.14795e-06, 4.69793e-06, 0.0130584, 0.025104, 0.0740163,
    0.226941, 0.633759, 1.42506, 2.37343, 2.83259
]



y_cp_64_6_4_2 =  [
    5.14801e-06, 0.0169636, 0.0682182, 0.131915, 0.359958,
    1.00101, 2.21678, 3.30095, 3.59052, 3.30303
]


y_cp_62_6_7_4 = [
    0.320326, 22.8425, 14.3073, 10.1914, 7.80846,
    6.26725, 5.19407, 4.40796, 3.80962, 3.3318
]



  
  	

markers=['o', '.', ',', 'v', 'o', '<', '>']
i=0
  


N = [10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000, 80000000, 90000000, 100000000]



# plotting the points 

i+=1
plt.plot(N, y_cp_64_4_0_1, marker = markers[i%(len(markers))])
i+=1
plt.plot(N, y_cp_64_4_7_4, marker = markers[i%(len(markers))])
i+=1
plt.plot(N, y_cp_64_4_12_2, marker = markers[i%(len(markers))])
i+=1
plt.plot(N, y_cp_64_5_8_1, marker = markers[i%(len(markers))])
i+=1
plt.plot(N, y_cp_64_6_0_1, marker = markers[i%(len(markers))])
i+=1
plt.plot(N, y_cp_64_6_4_2, marker = markers[i%(len(markers))])
i+=1
plt.plot(N, y_cp_62_6_7_4, marker = markers[i%(len(markers))])
i+=1

# naming the x axis
plt.xlabel('Trace Size')
# naming the y axis
plt.ylabel('NRMSE')

plt.grid()
plt.yscale("log")
plt.xscale("log")
  
# giving a title to my graph
plt.title('OnArrival')

plt.gca().legend(( "y_cp_64_4_0_1"  , "y_cp_64_4_7_4" , "y_cp_64_4_12_2", "y_cp_64_5_8_1" ,"y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4"))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot
plt.show()
