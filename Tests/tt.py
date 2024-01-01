
# importing matplotlib
import matplotlib.pyplot as plt



# making a simple plot
a = [ 1 , 2, 4, 5, 7, 8]
b = [(113+112+117+110)/4, (111+111+115+109)/4, (114+110+118+109)/4, (112+110+118+109)/4, (112+112+115+110)/4, (111+111+115+108)/4]

b = [100/b1 for b1 in b]

# Plot scatter here
plt.bar(a, b)
  
c = [0.7, 0.6, 0.5, 0.4 , 0.6,0.73]
c = [c1*0.04 for c1 in c]
  
plt.errorbar(a, b, yerr=c, fmt="o", color="r")

plt.ylabel('Load Factor')

ax = plt.gca()
ax.set_ylim([0.8, 1.01])
my_xticks = ['CuckooCP 18','Cuckoo 18','CuckooCP 16','Cuckoo 16','CuckooCP univ', 'Cuckoo univ']
plt.xticks(a, my_xticks)
  
plt.show()




