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
        
        width = 512
        memory =  width*Height*(factor+overhead_per_pool/counters_per_pool)/1024.0
        while(memory < 2*1024):
             width+=1
             memory = width*Height*(factor+overhead_per_pool/counters_per_pool)/1024.0    
		
        print(pool_config)
        print(" ")
        print(width)
        print("\n")
        
        d[pool_config] = memory_array
salsa_Memory = [width*Height*9/(8*1024.0) for width in widths_array]
	

		
  



y_cp_64_4_0_1 = [0.000309993, 9.20383e-05, 3.86331e-05, 1.67125e-05, 7.06666e-06, 2.90274e-06, 1.15965e-06, 4.54846e-07, 1.77719e-07, 6.93781e-08, 2.64618e-08, 9.63825e-09]


y_cp_64_4_7_4 = [0.000246599, 0.000107492, 3.87447e-05, 1.67125e-05, 7.06721e-06, 2.90274e-06, 1.15965e-06, 4.54846e-07, 1.77719e-07, 6.93781e-08, 2.64618e-08, 9.63825e-09]


y_cp_64_4_12_2 = [0.00030862, 9.00193e-05, 3.86828e-05, 1.67125e-05, 7.06666e-06, 2.90274e-06, 1.15965e-06, 4.54846e-07, 1.77719e-07, 6.93781e-08, 2.64618e-08, 9.63825e-09]



y_cp_64_5_8_1 = [0.000478999, 0.000222472, 9.37285e-05, 3.23086e-05, 7.83474e-06, 2.91247e-06, 1.15975e-06, 4.54846e-07, 1.77719e-07, 6.93781e-08, 2.64618e-08, 9.63825e-09]



y_cp_64_6_0_1 = [0.000638548, 0.000297049, 0.00013364, 5.67935e-05, 2.15978e-05, 5.95071e-06, 1.26311e-06, 4.56029e-07, 1.77727e-07, 6.93781e-08, 2.64618e-08, 9.63825e-09]




y_cp_64_6_4_2 = [0.000637949, 0.000297258, 0.000133078, 5.60988e-05, 2.06367e-05, 5.4407e-06, 1.26369e-06, 4.57193e-07, 1.77736e-07, 6.93783e-08, 2.64618e-08, 9.63825e-09]


y_cp_62_6_7_4 = [0.000638626, 0.000297688, 0.000133252, 5.6354e-05, 2.14544e-05, 5.01963e-06, 1.3204e-06, 4.77874e-07, 1.78099e-07, 6.93784e-08, 2.64619e-08, 9.63825e-09]


salsa = [0.000801392, 0.000333619, 0.000112839, 4.0162e-05, 1.67082e-05, 6.87269e-06, 2.69426e-06, 9.50758e-07, 2.93215e-07, 9.32026e-08, 3.14904e-08, 1.06849e-08]



  
  	

markers=['o', '.', ',', 'v', 'P', '<', '>']
line_styles = ['-', '--', '-.', ':', 'dotted', 'dashed', '-.', ':']
i=0
  






# plotting the points 

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

plt.gca().legend(( "(64,4,0,1)"  , "(64_4_7_4)" , "(64_4_12_2)", "(64_5_8_1)" ,"(64_6_0_1)" , "(64_6_4_2)" , "(62_6_7_4)", salsa))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot

plt.legend('',frameon=False)

plt.savefig("confs_NYC.pdf", format="pdf", bbox_inches="tight")
plt.show()