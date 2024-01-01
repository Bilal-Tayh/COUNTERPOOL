#!/usr/bin/env python3

import sys
sys.path.append("../")

#from defs import *

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import pylab

from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf')

plt.rcParams["font.family"] = "Verdana"
plt.rcParams["font.sans-serif"] = "Verdana"

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True  

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
        #
        #16b overhead
        (128,10,7,6), #48620 entries lookup
        #32b overhead
        (128,10,0,3), #no immediate lookup
        (128,10,4,2), #if counters are restricted to 80 bits or so, no immediate lookup
        (128,10,9,1), #no immediate lookup
        (128,11,0,4), #no immediate lookup
        (128,11,2,3), #no immediate lookup
        (128,12,3,3), #no immediate lookup
        (128,13,2,4), #no immediate lookup
        (128,9,8,2),  #Three lookups + one summation for (size,offset) computation #35960*4B = 140KB lookup (encode SAB(128,5)x2, starting positions for 2-5).
        (128,11,8,2), #Three lookups + one summation for (size,offset) computation #53130*5B = 265KB lookup (encode SAB(128,6)x2, starting positions for 2-6).
        (128,13,8,2), #Three lookups + one summation for (size,offset) computation #18564*8B = 150KB lookup (encode SAB(128,7)x2, starting positions for 2-7).
        #40b overhead, or 48 bit using two separate SAB encodings
        (128,11,6,1),
        #48b overhead
        (128,11,1,1),
        #
        #32 overhead bits
        (256,20,7,7),
        #64 overhead bits
        (256,20,2,3),
        (256,24,9,1), #57 overhead per pool
        (256,26,3,4), #62 overhead per pool
        #
        #64b overhead
        (510,36,7,8),
        (511,48,7,7),
        #128b overhead per pool
        (512,64,6,2), #123b
        (512,48,7,2), #123b
        (512,38,6,2),
        #256b overhead
        (512,63,2,1),
        ]

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

#datasets = ["CH16", "Univ2", "youtube", "zipf0.6", "zipf0.8", "zipf1.0", "zipf1.2", "zipf1.4", "NY18"]
datasets = ["zipf0.8"]

seeds = [40, 39, 38]    

for dataset in datasets:
        
    dsn = "\\{}\\".format(dataset)
    
    fn = {}
    
    for conf in confs:
    
        fn[conf] = [os.getcwd() + dsn + "sim_test_cms_error_on_arrival_pools_seed_" + str(i) + "_" + "_".join(tuple(map(str,conf))) + ".txt" for i in seeds]
         
    countersVSerror = {}
    
    for f in fn:
        
        countersVSerror[f] = {}
        
        countersVSerror[f]['L(1)'] = {}
        countersVSerror[f]['L(2)'] = {}
        countersVSerror[f]['L(inf)'] = {}
        
        for file in fn[f]:
                    
            lines = open(file).readlines()
            
            N = float(lines[0].split()[1])
            Height= float(lines[0].split()[5])
            
            for line in lines:
                
                Width = float(line.split()[3])
                
                countersVSerror[f]['L(1)'][Width] = countersVSerror[f]['L(1)'].get(Width, []) + [float(line.split()[8])/N]
                countersVSerror[f]['L(2)'][Width] = countersVSerror[f]['L(2)'].get(Width, []) + [float(line.split()[11])/N]
                countersVSerror[f]['L(inf)'][Width] = countersVSerror[f]['L(inf)'].get(Width, []) + [float(line.split()[14])]
                
    ###############################################################################
    ###############################################################################
    
    from itertools import cycle
    lines = ["-","--","-.",":"]
    linecycler = cycle(lines)
    
    bad_configs = [(61,5,5,6), (64,5,0,2), (64,6,0,3), (64,6,8,2), (64,6,4,2), (64, 7, 0, 4)]
        
    fig, ax = plt.subplots(figsize=(8,4))
    
    for pool_config in countersVSerror:
            
        widths_array = sorted(countersVSerror[pool_config]['L(2)'])
        
        (pool_bit_size, counters_per_pool, initial_counter_size, counter_bit_increase) = pool_config
        
        if pool_config in bad_configs:
            continue
        
        if pool_bit_size > 64:
            continue
           
        factor = (float(pool_bit_size/8.0)/counters_per_pool)
        
        (ps, n, s, j) = pool_config
        
        cs0 = nSAB(np.ceil((ps-n*s)/j),n) 
        
        overhead_per_pool = float(np.ceil(np.log2(cs0)/8))
        
        if (64, 7, 0, 4) == pool_config:
            overhead_per_pool = 2.0
        
        #overhead = 
        
        print(pool_config, overhead_per_pool)
                       
        memory_array = [width*Height*(factor+overhead_per_pool/counters_per_pool)/1024.0 for width in widths_array]
        
        ax.errorbar(memory_array ,
                    [np.mean(countersVSerror[pool_config]['L(2)'][width]) for width in widths_array], 
                    [np.std(countersVSerror[pool_config]['L(2)'][width], ddof=1) for width in widths_array], 
                    label=pool_config,#renamer.get(f, pool_config), 
                    #alpha=alphas[renamer.get(f, f)], 
                    linewidth=2, 
                    linestyle=next(linecycler),#lineStyles[renamer.get(f, f)], 
                    #marker=markers[renamer.get(f, f)],
                    #color=colors[renamer.get(f, f)], 
                    #markersize=markersizes[renamer.get(f, f)], 
                    capsize=12, 
                    elinewidth=4, 
                    capthick=1.5, 
                    #ecolor=colors[renamer.get(f, f)]
                    )
    
    ax.set_xscale('log', basex=10)
    ax.set_yscale('log', basey=10)
        
    plt.xlabel("Memory", fontsize=28)
    plt.ylabel("Error", fontsize=28)
    plt.legend(loc='best',prop={'size':12}, ncol=3) 
    #plt.xlim([2e0, 5e3])
    #plt.ylim([10**-9, 10**-3])
    plt.grid(linestyle='dashed')
    plt.xticks(fontsize = 28)
    plt.yticks(fontsize = 28)   
    plt.tight_layout()
    #plt.savefig('cus_rmse_' + dataset  + '.pdf')
    plt.show()
    
### create legend
figLegend = pylab.figure()

# produce a legend for the objects in the other figure
pylab.figlegend(*ax.get_legend_handles_labels(), fontsize=22, loc = 'upper center', ncol=6)
pylab.subplots_adjust(right=1.0, left=0.0, top=1.0, bottom=0.0)

# save the two figures to files
#figLegend.savefig("cus_legend.pdf", bbox_inches='tight')
    
    
