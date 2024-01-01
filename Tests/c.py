# importing the required module
import matplotlib.pyplot as plt
  
# x axis values
x = [0.6, 0.8, 1.0, 1.2, 1.4]
# corresponding y axis values
y_salsa = [
0.017923,
0.0119349,
0.00444852,
0.000736314,
5.3334e-05
]

y_cp_64_4_12_2 = [
0.0187086,
0.0119266,
0.00450241,
0.000710628,
5.48616e-05
]
  
# plotting the points 
plt.plot(x, y_cp_64_4_12_2, marker='o')
plt.plot(x, y_salsa, marker='p')

# naming the x axis
plt.xlabel('Zipf skew')
# naming the y axis
plt.ylabel('ARE (Log-scale)')

plt.grid()
plt.yscale("log")
#plt.xscale("log")
  
# giving a title to my graph
plt.title('Heavy Hitters, Memory: 2Mb')
plt.gca().legend(('salsa','counter pools 64_4_12_2'))
# function to show the plot
plt.show()
