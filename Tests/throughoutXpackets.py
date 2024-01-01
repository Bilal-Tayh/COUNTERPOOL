# importing the required module
import matplotlib.pyplot as plt
 
'''  
# x axis values
xi = [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536,131072,262144,524288,1048576]
x1 = [i/(9*1024) for i in xi]
x2 = [i/(18*1024) for i in xi]
# corresponding y axis values
'''

y_1 = [
143,
145,
144,
140,
132,
110,
85,
67,
60,
55
]



y_2 = [
143,
145,
144,
142,
135,
124,
103,
85,
75,
70
]


x = [2,2.5,3,3.5,4,4.5,5,5.5,6,6.5]


 





x_cuckoo = x
x_cuckooCp = x




# plotting the points 
plt.plot(x_cuckoo, y_2)
plt.plot(x_cuckooCp, y_1)



#x3 = [x+(64*4096/(1024*1024)) for x in x2]
#plt.plot(x3, y_cp_64_4_12_2_nf_4096)




# naming the x axis
plt.xlabel('packets[M]')
# naming the y axis
plt.ylabel('throughput [M/Sec]')
  
# giving a title to my graph

plt.gca().legend(('Cuckoo', 'Cuckoo_cp'))



plt.grid()

# function to show the plot
plt.show()
