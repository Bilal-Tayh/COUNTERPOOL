# importing the required module
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import pylab
from matplotlib.legend_handler import HandlerErrorbar
from matplotlib import container
import copy



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
    







y_cp_64_4_0_1 = [0.00129271, 0.000506265, 0.000191465, 9.4541e-05, 4.65121e-05, 2.2763e-05, 1.7625e-05, 1.51714e-06]

y_cp_64_4_7_4 = [0.000844309, 0.000414316, 0.000200616, 9.4541e-05, 4.65121e-05, 2.2763e-05, 1.57952e-05, 1.35089e-06]


y_cp_64_4_12_2 = [0.00129271, 0.000506265, 0.000191465, 9.4541e-05, 4.65121e-05, 2.2763e-05, 1.57952e-05, 1.35089e-06]


y_cp_64_5_8_1 = [0.00165375, 0.000810488, 0.000385148, 0.000173498, 6.7321e-05, 2.27793e-05, 1.39747e-05, 1.18525e-06]



y_cp_64_6_0_1 = [0.00232381, 0.00115103, 0.000567536, 0.000274487, 0.000128749, 5.61252e-05, 2.51939e-05, 1.07612e-06]




y_cp_64_6_4_2 = [0.0023207, 0.00114976, 0.000564001, 0.000270126, 0.000123353, 4.98829e-05, 1.43113e-05, 9.67168e-07]



y_cp_62_6_7_4 = [0.00232339, 0.00115232, 0.000566784, 0.000273605, 0.000127689, 5.18829e-05,1.55646e-05, 8.32406e-07]


all_y = [y_cp_64_4_0_1, y_cp_64_4_7_4, y_cp_64_4_12_2, y_cp_64_5_8_1, y_cp_64_6_0_1, y_cp_64_6_4_2, y_cp_62_6_7_4]
all_x = [d[(64,4,0,1)], d[(64,4,7,4)], d[(64,4,12,2)], d[(64,5,8,1)], d[(64,6,0,1)], d[(64,6,4,2)], d[(62,6,7,4)]]


y_optimal = y_cp_64_4_0_1
x_optimal = d[(64,4,0,1)]

print(x_optimal)


for i in range(len(y_cp_64_6_4_2)):
    min = 1;
    for j in range(len(all_y)):
        if(all_y[j][i]<min):
            y_optimal[i] = all_y[j][i]
            x_optimal[i] = all_x[j][i]
            min = all_y[j][i]







y_pools_To_Counters = [0.00129271, 0.000506265, 0.000191465, 9.4541e-05, 4.65121e-05, 2.2763e-05, 1.10673e-05, 5.32958e-06, 2.5355e-06, 1.18525e-06, 5.41782e-07, 2.39878e-07]


salsa =  [0.00287239, 0.00129587, 0.000509684, 0.00019047, 9.35622e-05, 4.55432e-05, 2.18152e-05, 1.01375e-05, 4.42744e-06, 1.66772e-06, 5.59345e-07, 2.4129e-07]


aee  = [
    0.00110343,
    0.000548157,
    0.000271558,
    0.000134143,
    6.59958e-05,
    3.22957e-05,
    1.569e-05,
    7.55154e-06,
    3.58895e-06,
    1.67632e-06,
    7.64785e-07,
    3.37562e-07
]



baseline = [
    0.00445002,
    0.00218519,
    0.000956001,
    0.000271786,
    0.000134112,
    6.59749e-05,
    3.22801e-05,
    1.56568e-05,
    7.41085e-06,
    2.97203e-06,
    8.45456e-07,
    3.65223e-07
]

abc = [
    0.00100343,
    0.000508157,
    0.000201558,
    0.000104143,
    5.6401e-05,
    4.65815e-05,
    2.6054e-05,
    1.38925e-05,
    8.61078e-06,
    6.74647e-06,
    6.19339e-06,
    6.07695e-06
]

pyramid = [0.0660412, 0.0393924, 0.00855066, 0.0021069, 0.000526573, 0.000130808, 3.05867e-05, 7.55708e-06, 1.97106e-06, 8.44839e-07, 5.44839e-07, 5.44839e-07]

optimal = [0.000844309, 0.000414316, 0.000191465, 9.4541e-05, 4.65121e-05, 2.2763e-05, 1.10673e-05, 5.32958e-06, 2.5355e-06, 1.18525e-06, 5.41782e-07, 2.39878e-07]
optimal_x = [4.5, 9.0, 20.0, 40.0, 80.0, 160.0, 250.0, 360.0, 1280.0, 2560.0, 5120.0, 5973.333333333334]



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



# xlabel = 'Memory[KB]'
# ylabel = 'OnArrival NRMSE'
# fig, ax1 = plt.subplots(1,1)
# ax1.set_ylabel(ylabel, fontsize=20)
# ax1.set_xlabel(r'Memory[KB]', fontsize=20)



# i+=1
# ax1.errorbar(salsa_Memory, abc,label ='Abc', marker = markers[i%(len(markers))], markersize=12, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# ax1.errorbar(salsa_Memory, pyramid,label ='Pyramid', marker = markers[(i+4)%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])

# ax1.errorbar(salsa_Memory, baseline,label ='BaseLine', marker = 'X', markersize=10, linewidth=2.0, linestyle =line_styles[i-1], color = 'purple')
# i+=1
# ax1.errorbar(salsa_Memory, salsa,label ='Salsa', marker = markers[i%(len(markers))], color='gray', markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# ax1.errorbar(d[(64,4,0,1)]  , y_pools_To_Counters,label ='Counter Pools (64,4,0,1)', marker = markers[(i)%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1
# ax1.errorbar(optimal_x, optimal,label ='Optimal Counter Pools', marker = markers[i%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
# i+=1








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

plt.gca().legend(( "salsa","Counter Pools", "abc", "pyramid"))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot

plt.legend('',frameon=False)
plt.savefig("fail_comp_0.6.pdf", format="pdf", bbox_inches="tight")
plt.show()




# handles, labels = ax1.get_legend_handles_labels()
# handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]

# figlegend=pylab.figure()
# pylab.figlegend(*(handles,labels), fontsize=10, loc = 'upper left', ncol=3)
# figlegend.savefig("legend2.pdf",format = 'pdf', bbox_inches='tight')
