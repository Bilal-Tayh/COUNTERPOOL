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
	
salsa_Memory = [width*Height*(9/8)/(1024.0) for width in widths_array]	
    







y_cp_64_4_0_1 = [19000882, 20003805, 20660662, 20016254, 19794698, 20714335, 19813054, 20578895, 20952584, 21738370, 22335715, 25862049]



salsa =  [11588144, 11927410, 11862038, 11669910, 12168523, 12603539, 11792745, 13318288, 14633287, 15534313, 15385227, 16549074]


aee  = [5599574, 7447070, 8486773, 9862028, 10493040, 10902028, 11267109, 12014663, 15621431, 16734698, 15098147, 15078189]




baseline =[16156449, 16987745, 16736227, 17243550, 17430039, 18000195, 17648755, 19285021, 21875778, 22782008, 23494868, 25572737]


abc = [19676672, 21600902, 19930669, 22053909, 22966258, 23017769, 22783711, 23690151, 24793409, 22962013, 23515412, 25611388]


pyramid = [5831103, 6135202, 6871922, 6053651, 6083062, 6457739, 6740562, 7531815, 9037514, 6988977, 6948580, 7399269]





pyramid = [(x/1000000)/98 for x in pyramid]
baseline = [(x/1000000)/98 for x in baseline]
aee = [(x/1000000)/98 for x in aee]
abc = [(x/1000000)/98 for x in abc]
salsa = [(x/1000000)/98 for x in salsa]
y_cp_64_4_0_1 = [(x/1000000)/98 for x in y_cp_64_4_0_1]


for x in range(len(abc)):
    print(abc[x]/y_cp_64_4_0_1[x]);

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
plt.plot(d[(64,4,0,1)]  , y_cp_64_4_0_1, marker = markers[(i)%(len(markers))], markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
i+=1
i+=1
plt.plot(salsa_Memory, baseline, marker = 'X',color='purple', markersize=10, linewidth=2.0, linestyle =line_styles[i-1])
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
plt.ylabel('Throughput [M/sec]',fontsize=30)

plt.grid()
#plt.yscale("log")
plt.xscale("log")
plt.tight_layout()
  
# giving a title to my graph
#plt.title('OnArrival')

plt.gca().legend(( "salsa","Counter Pools", "abc", "pyramid"))


#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot

plt.legend('',frameon=False)
plt.savefig("speed_0.6.pdf", format="pdf", bbox_inches="tight")
plt.show()




# handles, labels = ax1.get_legend_handles_labels()
# handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]

# figlegend=pylab.figure()
# pylab.figlegend(*(handles,labels), fontsize=10, loc = 'upper left', ncol=3)
# figlegend.savefig("legend2.pdf",format = 'pdf', bbox_inches='tight')
