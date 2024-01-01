#!/usr/bin/env python3

#import os
import multiprocessing
import subprocess

'''
    // command line arguments
	cout << "Received input arguments:" << endl;
	cout << "argv[1]: int N = " << N << endl;
	cout << "argv[2]: int Seed = " << Seed << endl;
	cout << "argv[3]: int Alg = " << Alg << endl;
	cout << "argv[4]: bool weighted_experiment = " << weighted_experiment << endl;
	cout << "argv[5]: String Trace = \"" << Trace << "\"" << endl;
	cout << "argv[6]: Counters in row = \"" << RowCounterNum << "\"" << endl;
	cout << "argv[7]: Number of rows = \"" << RowsNum << "\"" << endl;
	cout << endl;   

	if (argc > 8)
	{
		argv[8] : pool_bit_size
		argv[9] : counters_per_pool
		argv[10]: initial_counter_size
		argv[11]: counter_bit_increase
	}
'''

# trace length

# trace path
Traces = ["zipf0.6", "zipf1.0", "zipf1.4", "NYC18"]
Traces = ["NYC18"]
#Traces = ["NYC18"]
#Traces = [  "zipf0.6"]
#Traces = ["zipf1.0"]
# number of rows
RowsNum = 4

# seeds
seeds = [40, 39, 38]
seeds = [40]
def error_worker_cp(N, counters, seed, trace, pool_config, k=0):
    
    (pool_bit_size, counters_per_pool, initial_counter_size, counter_bit_increase) = pool_config











    
    print("started run. counters: {}, seed: {}".format(counters, seed))
    subprocess.call(['../cp', 
                     str(N), 
                     str(seed), 
                     str(0), 
                     str(0), 
                     trace, 
                     str(counters), 
                     str(RowsNum), 
                     str(pool_bit_size), 
                     str(counters_per_pool), 
                     str(initial_counter_size), 
                     str(counter_bit_increase),
                     str(k)
                     ])
    
    return




def error_worker_salsa(N, counters, seed, trace):
    
    
    print("started run. counters: {}, seed: {}".format(counters, seed))
    subprocess.call(['../salsa', 
                     str(N), 
                     str(seed), 
                     str(0), 
                     str(0), 
                     trace, 
                     str(counters), 
                     str(RowsNum)])
    
    return

'''
def speed_worker(counters, seed, trace):
    print("started run. counter: {}, seed: {}".format(counters, seed))
    subprocess.call(['Salsa.exe', str(N), str(seed), str(5), str(0), trace, str(counters), str(RowsNum)])
    return 'finished: {} {} {}'.format(counters, seed, trace)
'''

if __name__ == '__main__':
    
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

    confs = [
            (64,4,12,2),
    ]

    confs = [
            #8b overhead
            (64,4,12,2),
            # (64,4,9,3),
            # (64,4,7,4),
            # (61,5,5,6), #210*3B = 630B lookup (encode the starting positions of counter 2-5)
            # (64,5,8,4), #210*3B = 630B lookup (encode the starting positions of counter 2-5)
            # (62,6,7,4), #252*4B = 1KB lookup (encode the starting positions of counter 2-6)
            # #16b overhead
            # (64,5,0,2), #One lookup for (size,offset) computation # 58905*3B=175KB lookup (encode the starting positions of counter 2-5)
            # (64,6,4,2), #One lookup for (size,offset) computation # 210*4B=175KB lookup (encode the starting positions of counter 2-6)
            # (64,6,0,3), #One lookup for (size,offset) computation #(if counters are restricted to 40 bits or so), 210*4B=175KB lookup (encode the starting positions of counter 2-6)
            # (64,7,0,4), #One lookup for (size,offset) computation #(if counters are restricted to 32 bits or so), 53592*5B=260KB lookup (encode the starting positions of counter 2-6)
            # (64,5,7,1), #One lookup for (size,offset) computation #per pool & 40920*3B = 120KB lookup (encode the starting positions of counter 2-5)
            # (64,5,8,1), #Magic Division + One lookup for (size,offset) computation #per pool & 2925*3B = 9KB lookup (encode 22 size options for counter 1 (8-29) bits multiplied by SAB(24,4)) OR 20475*3B=60KB lookup table for SAB(24,5)
            # (64,6,8,2), #One lookup for (size,offset) computation #per pool & 20349*4B = 80KB lookup (encode the starting positions of counter 2-6)
            # (64,4,0,1), #
            # #20b overhead
            # (64,5,0,1),
            # #24b overhead
            # (64,6,0,1),
    ]


    N = 98000000
    N = 10000000

    confs = [
    (64,4,0,1),
    (64,4,12,2),
    (64,4,7,4),
    (64,5,8,1),
    (64,6,0,1),
    (64,6,4,2),
    (62,6,7,4)
    ]


    confs = [
  (64,4,0,1),
      ]


    Dict = {  
    (64, 5, 0, 1): 238313,
    (64, 6, 0, 1): 285976,
    (64, 4, 12, 2):233017,
    (64, 4, 9, 3):209716,
    (64, 4, 7, 4):233017,
    (61, 5, 5, 6):303936,
    (64, 5, 8, 4):291272,
    (62, 6, 7, 4):359512,
    (64, 5, 0, 2):262144,
    (64, 6, 4, 2):314573,
    (64, 6, 0, 3):285976,
    (64, 7, 0, 4):367002,
    (64, 5, 7, 1):262144,
    (64, 5, 8, 1):262144,
    (64, 6, 8, 2):314573,
    (64, 4, 0, 1):209716,
    'salsa' : 466034
    }

 

    


    isCounterPool = False
    isSalsa= True
    # error (parallel)
    for trace in Traces:
        RowCounters = [2**i for i in range(9,21)]
        RowCounters = [2**19]


####################
        #r = 32768

        #N2 = [10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000, 80000000, 90000000, 100000000]
        #for N in N2:
####################
        for r in RowCounters:
            for seed in seeds:
                if(isSalsa):
                    error_worker_salsa(N, r, seed, trace);
                for pool_config in confs:
                    # p = []
                    if(isCounterPool):

                        #error_worker_cp(N, Dict[pool_config]/10, seed, trace, pool_config,0);  
                        #error_worker_cp(N, Dict[pool_config], seed, trace, pool_config,0);                    
                        # error_worker_cp(N, Dict[pool_config]/10, seed, trace, pool_config,16);  
                        # error_worker_cp(N, Dict[pool_config]/10, seed, trace, pool_config,64); 
                        # error_worker_cp(N, Dict[pool_config]/10, seed, trace, pool_config,256); 
                        #error_worker_cp(N,r, seed, trace, pool_config,16);
                        #error_worker_cp(N,r, seed, trace, pool_config,64);
                        error_worker_cp(N,r, seed, trace, pool_config,0);
                        #p.append(multiprocessing.Process(target=error_worker, args=(r, seed, trace, pool_config,)))
                        
                    # for proc in p:
                    #     proc.start()  
                
                    # for proc in p:
                    #     proc.join()    
                    
                    # p = []
                

                
                
    '''
    
    # speed (serial)
    for trace in Traces:
        
        RowCounters = [2**i for i in range(9,21)]
            
        for r in RowCounters:
            
            for seed in seeds:  
                
                print(speed_worker(r, seed, trace))
                
    '''
                












           
