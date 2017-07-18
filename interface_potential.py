import numpy as np
import pandas as pd
import os.path
from scipy import integrate

n = int(input("Number of umbrella's: "))
path = os.getcwd()

kB = 1.38064852e-23

filename = ["" for k in range(n)]
for j in range(0,n):
    filename[j] = os.path.join(path,'pos_force'+str(j)+'.dat')
    
# Reading the spring positions of different umbrellas and writing to a single file.
with open(os.path.join(path,'pos_force.dat'), 'w') as outfile:
    for fname in filename:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
            outfile.write("\n")

t,z,f = np.loadtxt(os.path.join(path, 'pos_force.dat'), unpack=True)
zmax = np.amax(z)
zmin = np.amin(z)
print(zmin,zmax) # gives approximate range of z for binning

# Getting coexistence conditions 
startz = float(input("Initial Z: "))
endz = float(input("Final Z: "))
delz = float(input("Bin Width: "))
pres = float(input("Saturation Pressure: "))
area = float(input("Area: "))
T = float(input("Temperature: "))

# Dividing into bins 
bin_count = (endz - startz)/delz + 1
bins = np.linspace(startz, endz, bin_count)
hist, edges = np.histogram(z, bins)
average = np.zeros(bin_count)
counts = np.zeros(bin_count)
for i, item in enumerate(z):
    if (item >= startz and item <= endz): 
        bin = np.amin(np.where(np.abs(item - edges) < delz ))
        average[bin] += f[i]
        counts[bin] += 1
average /= counts
average = average - pres * area # histogram reweigthing
df = pd.DataFrame({'bin': edges, 'average': average})
df.to_csv(os.path.join(path,'histogram.dat'), sep=' ', columns=('bin', 'average'), header=False, index=False)

# Cumulative integration for getting free energy
x,y = np.genfromtxt(os.path.join(path, 'histogram.dat'), skip_footer=1, unpack=True)
y_int = integrate.cumtrapz(y,x,initial=0)
y_int = -y_int/(kB*T)
df = pd.DataFrame({'Z': x, 'potential': y_int})
df.to_csv(os.path.join(path,'lnpi.dat'), sep=' ', columns=('Z', 'potential'), header=False, index=False)
