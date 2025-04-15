### File to calculate variation due to dipole electric field 

from config import *

from Image_charge_3d import *

class dipole_Efield:

    def __init__(self, q, z_ct, y_ct, x_ct, z, x, y, ep ):

        self.q = q #charge on dipole
        self.ep = ep # dielectric
        self.x_ct = x_ct # x coordinate of charge trap
        self.y_ct = y_ct # y coordinate of charge trap
        self.z_ct = z_ct # z coordinate of charge trap
        self.z = z # z coordinate of obs pt in nm
        self.x = x # x coordinate of obs pt in nm
        self.y = y # y coordinate of obs pt in nm

    def E_Field(self):

        Rct = np.array([self.z_ct, self.y_ct, self.x_ct], dtype=np.float64)

        Rmct = np.array([-self.z_ct, self.y_ct, self.x_ct], dtype=np.float64)

        R = np.array([self.z,  self.y, self.x], dtype=np.float64) 

        R1 = R - Rct

        R2 = R - Rmct

        R1_mag = np.linalg.norm(R1)

        R2_mag = np.linalg.norm(R2) 

        Ef = k0/self.ep*self.q*(R1/R1_mag**3 - R2/R2_mag**3)

        return Ef 
    
    def E_field_dipole_approx(self):

        Rct = np.array([self.z_ct, self.y_ct, self.x_ct], dtype=np.float64)

        Rmct = np.array([-self.z_ct, self.y_ct, self.x_ct], dtype=np.float64)

        Rct_mid = np.array([0, self.y_ct, self.x_ct], dtype=np.float64)

        R = np.array([self.z,  self.y, self.x], dtype=np.float64)

        P = (Rct - Rmct)*self.q

        #P = np.array([-2*self.a, 0, 0])*self.q

        r = R - Rct_mid

        rmag = np.linalg.norm(r)

        rhat = r/rmag

        return k0/self.ep*(3*(np.sum(P*rhat))*rhat - P)/(rmag**3)
    

def main():

    XCT = np.linspace(-100, 100, 200)

    YCT = 0 

    ZCT = 5 

    Q = -ee 

    EP = 13

    X = 0

    Y = 0 

    Z = 67

    T_SIGE = 60

    T_OX = 5 

    Efield = np.empty((XCT.shape[0],3))

    Efield_ic = np.empty((XCT.shape[0],3)) 

    Efield_dd = np.empty((XCT.shape[0],3)) 

    for i in range(XCT.shape[0]):

        #Efield[i,:] = dipole_Efield(Q, Z, A, X[i], Y, EP).E_Field()
        Efield[i,:] = dipole_Efield(Q, ZCT, YCT, XCT[i], Z, Y, X, EP).E_field_dipole_approx()

        het = Charge_in_medium3(-ee, ZCT, YCT, XCT[i], EP, EP, EP, T_SIGE, T_OX, 1e-6)
        het.calc_image_charges()
        Efield_ic[i,:] = het.calc_ele_medium1(X, Y, Z)  

        het_dd = Charge_in_medium3(-ee, ZCT, YCT, XCT[i], ep_ox=3.9, ep_sige=13, ep_qw=11.7, t_sige=T_SIGE, t_ox=T_OX, r=1e-6)
        het_dd.calc_image_charges()
        Efield_dd[i,:] = het_dd.calc_ele_medium1(X, Y, Z)  
        
        if i%100 ==0 :

            print(i)


    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))  # 1 row, 1 columns

    #ratio2 = np.divide(E_med1_a[:,0]-E_med1_b[:,0], E_med1_a[:,2]-E_med1_b[:,2],  out=np.zeros_like(E_med1_a[:,0]), where=E_med1_a[:,2]!=0, dtype=np.float64)  # Ensures precision

    ax.scatter(XCT, Efield[:,0], alpha=0.7, marker='o', facecolors='none', edgecolors='blue', label = 'EZ')  # Scatter plot
    ax.scatter(XCT, Efield[:,2], alpha=0.7, marker='o', facecolors='none', edgecolors='red', label = 'EX')  # Scatter plot
    ax.scatter(XCT, Efield[:,1], alpha=0.7, marker='o', facecolors='none', edgecolors='black', label = 'EY')

    ax.scatter(XCT, Efield_ic[:,0], alpha=0.4, color='blue', marker= "^", label = 'EZ 1ic')  # Scatter plot
    ax.scatter(XCT, Efield_ic[:,2], alpha=0.4, color='red', marker= "^", label = 'EX 1ic')  # Scatter plot
    ax.scatter(XCT, Efield_ic[:,1], alpha=0.4, color='black', marker= "^", label = 'EY 1ic')

    ax.scatter(XCT, Efield_dd[:,0], alpha=0.7, color='blue', marker= "x", label = 'EZ dd')  # Scatter plot
    ax.scatter(XCT, Efield_dd[:,2], alpha=0.7, color='red', marker= "x", label = 'EX dd')  # Scatter plot
    ax.scatter(XCT, Efield_dd[:,1], alpha=0.7, color='black', marker= "x", label = 'EY dd')

    ax.set_title('EZ,EX,EY')
    ax.set_xlabel('XCT')
    ax.legend()

    #ax.set_ylim(ymin=-50, ymax=50)

    plt.tight_layout()  # Adjust spacing
    plt.show()



    # # Create subplots
    # fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)  # 3 row, 1 columns

    # # Labels for axes
    # labels = ['EZ', 'EY', 'EX']

    # # Loop through each subplot
    # for i, ax in enumerate(axes):
    #     ax.scatter(X, Efield[:, i], alpha=0.7)  # Scatter plot
    #     ax.set_title(labels[i])
    #     ax.set_xlabel('R')
        

    # plt.tight_layout()  # Adjust spacing
    # plt.show()


    # # Create subplots
    # fig, ax = plt.subplots(1, 1, figsize=(4, 4), sharey=True)  # 3 row, 1 columns

    # # Labels for axes
    # labels = ['EZ', 'EY', 'EX']

    # ratioXbyZ = np.divide(Efield[:, 2], Efield[:,0] )

    # ax.scatter(X, ratioXbyZ, alpha=0.7)  # Scatter plot
    # ax.set_title('EX/EZ')
    # ax.set_xlabel('R')
        

    # plt.tight_layout()  # Adjust spacing
    # plt.show()

if __name__ == "__main__":
    main()
        