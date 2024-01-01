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
    

	
    



y_cp_64_4_0_1 = [
0.000580879,
0.000178267,
7.98499e-05,
3.67532e-05,
1.6862e-05,
7.66855e-06,
3.45567e-06,
1.53856e-06,
6.74863e-07,
2.89947e-07,
1.21486e-07,
4.91766e-08
]

y_cp_64_4_7_4 =[
0.000476966,
0.00020673,
7.97858e-05,
3.6751e-05,
1.68625e-05,
7.66855e-06,
3.45567e-06,
1.53856e-06,
6.74863e-07,
2.89947e-07,
1.21486e-07,
4.91766e-08
]

y_cp_64_4_12_2 = [
0.000575821,
0.00017436,
7.99778e-05,
3.67522e-05,
1.68625e-05,
7.66855e-06,
3.45567e-06,
1.53856e-06,
6.74863e-07,
2.89947e-07,
1.21486e-07,
4.91766e-08
]


y_cp_64_5_8_1 =[
0.000910046,
0.000418341,
0.000180828,
6.84678e-05,
1.83041e-05,
7.6855e-06,
3.45594e-06,
1.53856e-06,
6.74863e-07,
2.89947e-07,
1.21486e-07,
4.91766e-08
]


y_cp_64_6_0_1 = [
0.00120167,
0.000561878,
0.000258189,
0.000115091,
4.80183e-05,
1.65561e-05,
3.75444e-06,
1.5413e-06,
6.74892e-07,
2.89948e-07,
1.21486e-07,
4.91766e-08
]



y_cp_64_6_4_2 = [
0.00120068,
0.000562053,
0.00025704,
0.000113837,
4.63104e-05,
1.36981e-05,
3.90896e-06,
1.54292e-06,
6.74904e-07,
2.89948e-07,
1.21486e-07,
4.91766e-08
]


y_cp_62_6_7_4 = [
0.0012011,
0.000562661,
0.000257582,
0.000114446,
4.73056e-05,
1.57222e-05,
3.66175e-06,
1.5719e-06,
6.81047e-07,
2.89963e-07,
1.21486e-07,
4.91766e-08
]

salsa = [0.00148765, 0.00060866, 0.000198767, 8.08026e-05, 3.64538e-05, 1.62741e-05, 7.06301e-06, 2.85884e-06, 9.77707e-07, 3.2628e-07, 1.27447e-07, 5.05156e-08]




  
  	

markers=['o', '.', ',', 'v', 'P', '<', '>']
line_styles = ['-', '--', '-.', ':', 'dotted', 'dashed', '-.', ':']
i=0
  


y_cp_64_4_0_1 = [ y*1.53 for y in y_cp_64_4_0_1]



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

plt.gca().legend(("(64,4,0,1)"  , "(64_4_7_4)" , "(64_4_12_2)", "(64_5_8_1)" ,"(64_6_0_1)" , "(64_6_4_2)" , "(62_6_7_4)"))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot

plt.legend('',frameon=False)
plt.savefig("confs_1.0.pdf", format="pdf", bbox_inches="tight")
plt.show()