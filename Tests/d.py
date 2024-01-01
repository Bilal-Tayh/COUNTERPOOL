# importing the required module
import matplotlib.pyplot as plt
  
# x axis values
x = [0.6, 0.8, 1.0, 1.2, 1.4]
# corresponding y axis values
y_salsa = [
5.59248e-07,
3.8701e-07,
1.27451e-07,
1.23998e-08,
5.73413e-10
]

y_cp_64_4_12_2 = [
1.18525e-06,
8.34359e-07,
2.89947e-07,
3.07674e-08,
1.5691e-09
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
plt.title('On Arraival, Memory: 2Mb')
plt.gca().legend(('salsa','counter pools 64_4_12_2'))
# function to show the plot
plt.show()
