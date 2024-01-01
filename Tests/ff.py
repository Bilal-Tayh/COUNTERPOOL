# importing the required module
import matplotlib.pyplot as plt
  
# x axis values
x = [100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115]
x = [100.0/x1 for x1 in x ]



# corresponding y axis values
y_cuckooCP16 = [
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
100,
100,
100
]


y_cuckoo16 = [
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
100,
100,
100,
100,
100
]

y_cuckooCP18 = [
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
100,
100,
100,
100
]


y_cuckoo18 = [
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
100,
100,
100,
100,
100
]




y_cuckooCP_univ = [
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
100,
100,
100,
100
]


y_cuckoo_univ = [
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
100,
100,
100,
100,
100
]


  
# plotting the points 
plt.plot(x, y_cuckooCP16, marker='+')
plt.plot(x, y_cuckooCP18, marker='v')
plt.plot(x, y_cuckooCP_univ,  marker='p')
plt.plot(x, y_cuckoo16,  marker='o')
plt.plot(x, y_cuckoo18,  marker='s')
plt.plot(x, y_cuckoo_univ,  marker='.')

# naming the x axis
plt.xlabel('Load Factor')
# naming the y axis
plt.ylabel('Sucsess Rate')

plt.grid()
#plt.yscale("log")
#plt.xscale("log")
  
# giving a title to my graph
#plt.title('Heavy Hitters, Memory: 2Mb')
plt.gca().legend(('cuckooCP_16','cuckooCP_18', 'cuckooCP_univ', 'cuckoo_16','cuckoo_18', 'cuckoo_univ'))
# function to show the plot
plt.show()






