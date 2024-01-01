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
	
salsa_Memory = [width*Height*4/(1024.0) for width in widths_array]	
    

y_pools_To_Counters = [0.000309993, 9.20383e-05, 3.86331e-05, 1.67125e-05, 7.06666e-06, 2.90274e-06, 1.15965e-06, 4.54846e-07, 1.77719e-07, 6.93781e-08, 2.64618e-08, 9.63825e-09]

salsa = [0.000801392, 0.000333619, 0.000112839, 4.0162e-05, 1.67082e-05, 6.87269e-06, 2.69426e-06, 9.50758e-07, 2.93215e-07, 9.32026e-08, 3.14904e-08, 1.06849e-08]


aee  = [
	0.000700732,
	0.000324344,
	0.000296561,
	0.000242684,
	0.000268945,
	0.000267613,
	0.000213475,
	0.000255634,
	0.000266499,
	0.000263655,
	0.000209228,
	0.000205005
]



baseline = [
	0.00375835,
	0.00168246,
	0.000589909,
	0.000236784,
	0.00010965,
	5.84073e-05,
	2.24943e-05,
	1.03645e-05,
	3.12042e-06,
	1.55365e-06,
	6.02101e-07,
	1.64246e-07
]

#abc = [
#	0.0372001,
#	0.0371715,
#	0.0371715,
#	0.0372001,
#	0.0371715,
#	0.0371715,
#	0.0371715,
#	0.0372,
#	0.0371715,
#	0.0371715,
#	0.0371715,
#	0.0371715
#]

abc = [0.0372001, 0.03348009, 0.02999447, 0.02674296, 0.02372523, 0.02093223, 0.01836443, 0.0160227, 0.01390747, 0.01202001, 0.01035332, 0.00885129]



pyramid = [0.0215729, 0.0105906, 0.00264525, 0.000806389, 0.000293804, 0.000128343, 4.35585e-05, 7.31634e-06, 1.19817e-06, 3.57822e-07, 3.57822e-07, 3.57822e-07]


optimal = [0.000246599, 9.00193e-05, 3.86331e-05, 1.67125e-05, 7.06666e-06, 2.90274e-06, 1.15965e-06, 4.54846e-07, 1.77719e-07, 6.93781e-08, 2.64618e-08, 9.63825e-09]
optimal_x = [4.5, 9.0, 20.0, 40.0, 80.0, 160.0, 320.0, 640.0, 1280.0, 2560.0, 5120.0, 5973.333333333334]


markers=['o', '.', ',', 'v', 'o', '<', '>']
line_styles = ['-', '--', '-.', ':', 'dotted', 'dashed', '-.', ':']
i=0
  



# plotting the points 

# i+=1
# plt.plot(d[(64,4,0,1)] , y_cp_64_4_0_1_0, marker = markers[i%(len(markers))])
# i+=1
# plt.plot( [y + 4*1/1024.0 for y in d[(64,4,0,1)]], y_cp_64_4_0_1_1, marker = markers[i%(len(markers))])
# i+=1
# plt.plot( [y + 4*4/1024.0 for y in d[(64,4,0,1)]], y_cp_64_4_0_1_4, marker = markers[i%(len(markers))])
# i+=1
# plt.plot([y + 4*16/1024.0 for y in d[(64,4,0,1)]], y_cp_64_4_0_1_16, marker = markers[i%(len(markers))])
# i+=1
# plt.plot([y + 4*64/1024.0 for y in d[(64,4,0,1)]], y_cp_64_4_0_1_64, marker = markers[i%(len(markers))])
# i+=1
# plt.plot([y + 4*256/1024.0 for y in d[(64,4,0,1)]], y_cp_64_4_0_1_256, marker = markers[i%(len(markers))])


i+=1
plt.plot(salsa_Memory, abc, marker = markers[i%(len(markers))], markersize=12, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(salsa_Memory, pyramid, marker = markers[(i+4)%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(salsa_Memory, salsa, marker = markers[i%(len(markers))], color='gray', markersize=16, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(d[(64,4,0,1)]  , y_pools_To_Counters, marker = markers[(i)%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(optimal_x, optimal, marker = markers[i%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
plt.plot(salsa_Memory, baseline, marker = 'X', markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1


plt.yticks(fontsize=25)
plt.xticks(fontsize=25)

#plt.ylim([0.0000000001,10])
# naming the x axis
plt.xlabel('Memory[KB]',fontsize=30)
# naming the y axis
plt.ylabel('On-Arrival NRMSE',fontsize=30)

plt.grid()
plt.yscale("log")
plt.xscale("log")
plt.tight_layout()
  
# giving a title to my graph
#plt.title('OnArrival')

plt.gca().legend(("salsa","Counter Pools", "abc", "pyramid"))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot

plt.legend('',frameon=False)
plt.savefig("fail_comp_NYC.pdf", format="pdf", bbox_inches="tight")
plt.show()