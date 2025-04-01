import math
import cmath
import numpy as np
from numpy.polynomial.hermite import Hermite
from scipy.sparse import csr_matrix, coo_matrix,  bmat, diags, identity, issparse, vstack, hstack
from scipy.sparse.linalg import eigsh,eigs
import matplotlib.pyplot as plt
import sys
import random
from matplotlib.ticker import MaxNLocator


#from ast import Del
#from numpy.linalg import eigvals, eigvalsh
#from scipy.linalg import eigh
#import scipy as SCI
#import scipy.sparse as Spar
#from tempfile import TemporaryFile

#np.set_printoptions(linewidth = 500)
np.set_printoptions(threshold=sys.maxsize)


###defining constants##

hbar = 1.055*10**(-34);   #in J-s
ee = 1.602*10**(-19);     #in C
hbar_mev = hbar/ee*1000   # in meV-s
me = 9.11*10**(-31);      #in kg
hbm = hbar**2*1000/2/me/ee/(1e-18) #in meV (nm)**2

ep0 = 8.85 *1E-24 ### epsilon knot in C/mV/nm

k0 = 1/4/math.pi/ep0 ### in mV nm /C

k0_e = k0 * ee ### in meV nm  ##### if you dont want to multiply by charge in code then use this 