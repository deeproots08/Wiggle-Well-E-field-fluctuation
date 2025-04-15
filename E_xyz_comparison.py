from config import *
from Image_charge_3d import *


def main():

    ###file to compare Ex,y,x with each other
    ###Then to compare EXYZ with different dielectric and then a single dielectric with sige dielectric constant

    ### consider charge trap at a distance R_CT

    R_CT = np.linspace(-100,100,201)

    E_med1_a = np.empty((R_CT.shape[0],3))
    E_med1_b = np.empty((R_CT.shape[0],3))

    T_OX = 5 ### IN NM
    T_SIGE = 60 ### IN NM
    T_QW = 9   ### IN NM  ##irrelevantc:\Users\avani\OneDrive\Desktop\Spin_Splitting_Ge_ABS\sheet_of_charge_v3.ipynb