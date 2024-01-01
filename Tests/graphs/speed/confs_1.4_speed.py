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
	
salsa_Memory = [width*Height*(9/8)/(1024.0) for width in widths_array]	

y_cp_64_4_0_1= [20192659, 19790218, 20017041, 20338902, 18678828, 19351647, 19335830, 19625842, 19212585, 19364277, 20217105, 20450946]

salsa = [14116714, 12166795, 13773383, 12517518, 12053259, 12368846, 12554130, 12344344, 12293176, 12242042, 13646581, 13688257]



aee  = [763375, 553679, 606809, 574821, 539247, 591824, 646797, 528570, 537605, 579225, 572417, 559604]



baseline = [19796827, 16876392, 19720911, 17915580, 17126072, 16582982, 18223375, 16752897, 16197109, 17231239, 18064260, 17221984]


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



abc = [17942831, 18378913, 17181484, 18251920, 18324565, 17065290, 18432501, 17857947, 18118227, 18112197, 18283542, 17787883]

pyramid = [6312646, 5870671, 6233528, 6052709, 6029210, 5852133, 6080414, 6006806, 6050072, 5959327, 6267574, 6065557]



pyramid = [98/(x/1000000) for x in pyramid]
baseline = [98/(x/1000000) for x in baseline]
aee = [98/(x/1000000) for x in aee]
abc = [98/(x/1000000) for x in abc]
salsa = [98/(x/1000000) for x in salsa]
y_cp_64_4_0_1 = [98/(x/1000000) for x in y_cp_64_4_0_1]





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

plt.gca().legend(( "salsa", "Counter Pools","abc", "pyramid"))

#plt.gca().legend(("y_cp_64_5_7_1", "y_cp_64_4_0_1" , "y_cp_64_4_12_2" , "y_cp_64_5_8_1" , "y_cp_64_5_8_4" , "y_cp_64_6_0_1" , "y_cp_64_6_4_2" , "y_cp_62_6_7_4" ))
# function to show the plot

plt.legend('',frameon=False)
plt.savefig("speed_1.4.pdf", format="pdf", bbox_inches="tight")
plt.show()