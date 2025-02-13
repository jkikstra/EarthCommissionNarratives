from scipy.integrate import odeint
import numpy as np
from pyDOE import * #function name >>> lhs

#Tipping limits, see Armstrong McKay et al. 2022:
limits_gis  = [0.8, 3.0]  #0.8-3.0 (central: 1.5)
limits_thc  = [1.4, 8.0]  #1.4-8.0 (central: 4.0)
limits_wais = [1.0, 3.0]  #1.0-3.0 (central: 1.5)
limits_amaz = [2.0, 6.0]  #2.0-6.0 (central: 3.5)
limits_reef = [1.0, 2.0]  #1.0-2.0 (central: 1.5)



###################################################
#Time scale of tipping for the tipping elements (taken from the literature review of D. Armstrong McKay 2021)
tau_gis  = [1000, 15000]         #1000-15000(central: 10.000)      old values: [1000, 15000] 
tau_thc  = [15, 300]             #15-120 (central: 50)             old values: [15, 300]     
tau_wais = [500, 13000]          #500-13000 (central: 2000)        old values: [1000, 13000] 
tau_amaz = [50, 200]             #50-200 (central: 100)            old values: [50, 200]     
tau_reef = [9.9, 10.1]           #~-~ (central: 10)

"""
Latin hypercube sampling
Note: These points need a rescaling according to the uncertainty ranges
This can be done by: x_new = lower_lim + (upper_lim - lower_lim) * u[0;1), where u[0;1) = Latin-HC
"""

# sample size
N = 100

points = np.array(lhs(10, samples=N)) #give dimensions and sample size, here shown for a Latin hypercube; (unfortunately not space filling and not orthogonal)

#rescaling function from latin hypercube
def latin_function(limits, rand):
    resc_rand = limits[0] + (limits[1] - limits[0]) * rand
    return resc_rand
    
    
#MAIN

array_limits = []
sh_file = []
for i in range(0, len(points)):

    #TIPPING RANGES
    rand_gis = latin_function(limits_gis, points[i][0])
    rand_thc = latin_function(limits_thc, points[i][1])
    rand_wais = latin_function(limits_wais, points[i][2])
    rand_amaz = latin_function(limits_amaz, points[i][3])
    rand_reef = latin_function(limits_reef, points[i][4])
        
    #FEEDBACKS
    rand_tau_gis = latin_function(tau_gis, points[i][5])
    rand_tau_thc = latin_function(tau_thc, points[i][6])
    rand_tau_wais = latin_function(tau_wais, points[i][7])
    rand_tau_amaz = latin_function(tau_amaz, points[i][8])
    rand_tau_reef = latin_function(tau_reef, points[i][9])


    array_limits.append([rand_gis, rand_thc, rand_wais, rand_amaz, rand_reef,
                         rand_tau_gis, rand_tau_thc, rand_tau_wais, rand_tau_amaz, rand_tau_reef])


	# write out
    sh_file.append(["{} {} {} {} {} {} {} {} {} {}".format(
                             #insert path
                             rand_gis, rand_thc, rand_wais, rand_amaz, rand_reef,
                             rand_tau_gis, rand_tau_thc, rand_tau_wais, rand_tau_amaz, rand_tau_reef,
                             str(i).zfill(4) )]) #zfill necessary to construct enough folders for monte carlo runs


#Create .sh file to run on the cluster
sh_file = np.array(sh_file)
np.savetxt("latin_sh_file_with_reef.txt", sh_file, delimiter=" ", fmt="%s")