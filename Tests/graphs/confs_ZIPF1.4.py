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
	
salsa_Memory = [width*Height*9/(8*1024.0) for width in widths_array]
	
    



y_cp_64_4_0_1 =  [
    1.26367e-05,
    4.57896e-06,
    1.71804e-06,
    6.42591e-07,
    2.42667e-07,
    9.04029e-08,
    3.35388e-08,
    1.2429e-08,
    4.46932e-09,
    1.5691e-09,
    5.49043e-10,
    1.8595e-10
]

y_cp_64_4_7_4 = [1.23491e-05, 4.59313e-06, 1.71633e-06, 6.42605e-07, 2.42667e-07, 9.04029e-08, 3.35388e-08, 1.2429e-08, 4.46932e-09, 1.5691e-09, 5.49043e-10, 1.8595e-10]


y_cp_64_4_12_2 = [1.24767e-05, 4.5727e-06, 1.71635e-06, 6.42591e-07, 2.42667e-07, 9.04029e-08, 3.35388e-08, 1.2429e-08, 4.46932e-09, 1.5691e-09, 5.49043e-10, 1.8595e-10]



y_cp_64_5_8_1 = [3.64534e-05, 9.24471e-06, 1.98996e-06, 6.48853e-07, 2.4279e-07, 9.04029e-08, 3.35388e-08, 1.2429e-08, 4.46932e-09, 1.5691e-09, 5.49043e-10, 1.8595e-10]




y_cp_64_6_0_1 = [5.33591e-05, 1.91602e-05, 5.56117e-06, 1.00485e-06, 2.51826e-07, 9.06209e-08, 3.35412e-08, 1.2429e-08, 4.46932e-09, 1.5691e-09, 5.49043e-10, 1.8595e-10]




y_cp_64_6_4_2 =[5.31915e-05, 1.89794e-05, 5.35833e-06, 9.37317e-07, 2.53122e-07, 9.05752e-08, 3.35395e-08, 1.2429e-08, 4.46932e-09, 1.5691e-09, 5.49043e-10, 1.8595e-10]



y_cp_62_6_7_4 = [
    5.33773e-05,
    1.92227e-05,
    5.07376e-06,
    9.49054e-07,
    2.73983e-07,
    9.11599e-08,
    3.35591e-08,
    1.2429e-08,
    4.46933e-09,
    1.5691e-09,
    5.49043e-10,
    1.8595e-10
]


salsa = [5.87099e-05, 1.83125e-05, 5.78177e-06, 1.8676e-06, 5.82481e-07, 1.76376e-07, 5.45509e-08, 1.57345e-08, 5.15509e-09, 1.69441e-09, 5.73413e-10, 1.93779e-10]





  
  	

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

plt.gca().legend(( "(64,4,0,1)"  , "(64_4_7_4)" , "(64_4_12_2)", "(64_5_8_1)" ,"(64_6_0_1)" , "(64_6_4_2)" , "(62_6_7_4)"))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot

plt.legend('',frameon=False)

plt.savefig("confs_1.4.pdf", format="pdf", bbox_inches="tight")
plt.show()