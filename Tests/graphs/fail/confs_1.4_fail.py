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
    

y_pools_To_Counters= [1.26367e-05, 4.57896e-06, 1.71804e-06, 6.42591e-07, 2.42667e-07, 9.04029e-08, 3.35388e-08, 1.2429e-08, 4.46932e-09, 1.5691e-09, 5.49043e-10, 1.8595e-10]
	
salsa = [5.87099e-05, 1.83125e-05, 5.78177e-06, 1.8676e-06, 5.82481e-07, 1.76376e-07, 5.45509e-08, 1.57345e-08, 5.15509e-09, 1.69441e-09, 5.73413e-10, 1.93779e-10]



aee  = [
    0.000579566,
    0.000577879,
    0.000389121,
    0.000373825,
    0.000361214,
    0.000368744,
    0.000314074,
    0.000429833,
    0.000429833,
    0.000429833,
    0.000429833,
    0.000429833
]



baseline = [
    0.000547431,
    0.000184605,
    8.85128e-05,
    2.78643e-05,
    1.25477e-05,
    4.15955e-06,
    1.3435e-06,
    6.37249e-07,
    2.1033e-07,
    8.33539e-08,
    2.82807e-08,
    1.01069e-08
]

#abc = [
#    0.109209,
#    0.109209,
#    0.109209,
#    0.109209,
#    0.109209,
#    0.109209,
#    0.109209,
#    0.109209,
#    0.109209,
#    0.109209,
#    0.109209,
#    0.109209
#]



abc = [0.109209, 0.09607468, 0.08354656, 0.07252348, 0.0628958, 0.05464934, 0.04766725, 0.0419252, 0.03733867, 0.03359977, 0.0304227, 0.02771516]

pyramid = [0.00867413, 0.00410959, 0.000598773, 0.000202865, 3.65565e-05, 9.61479e-06, 1.30601e-06, 3.96419e-07, 1.55049e-07, 3.33584e-08, 3.33584e-08, 3.33584e-08]


optimal = [1.23491e-05, 4.5727e-06, 1.71633e-06, 6.42591e-07, 2.42667e-07, 9.04029e-08, 3.35388e-08, 1.2429e-08, 4.46932e-09, 1.5691e-09, 5.49043e-10, 1.8595e-10]
optimal_x = [4.5, 9.0, 18.0, 40.0, 80.0, 160.0, 320.0, 373.33333333333337, 1280.0, 1493.3333333333335, 2986.666666666667, 5973.333333333334]


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

plt.gca().legend(( "salsa", "Counter Pools","abc", "pyramid"))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot

plt.legend('',frameon=False)
plt.savefig("fail_comp_1.4.pdf", format="pdf", bbox_inches="tight")
plt.show()