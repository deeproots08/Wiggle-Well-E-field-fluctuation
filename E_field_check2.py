from config import *
from Image_charge_3d import *

### define a class whihc takes into account only the dipole 

class only_one_ic(Charge_in_medium3):

    def calc_image_charges(self):


        q40 = self.q_ct
        z40 = self.z_ct
        level = 0

        q41 = -self.q_ct
        z41 = -self.z_ct
        level = 0

        self.image_charges_q4s.append((q40, z40, level, 'q4j'))
        self.image_charges_q4s.append((q41, z41, level, 'q4j'))
        self.rule_iv(q40, z40, level + 1)
        self.rule_iv(q41, z41, level + 1)

        ### keep only initial two charges 

        self.image_charges_q5s.sort(key=lambda x: x[2])
        self.image_charges_q4s.sort(key=lambda x: x[2])
        self.image_charges_q3s.sort(key=lambda x: x[2])
        self.image_charges_q2s.sort(key=lambda x: x[2])
        self.image_charges_q1s.sort(key=lambda x: x[2])

        self.image_charges_q5s = self.image_charges_q5s[:2]
        self.image_charges_q4s = self.image_charges_q4s[:2]
        self.image_charges_q3s = self.image_charges_q3s[:2]
        self.image_charges_q2s = self.image_charges_q2s[:2]
        self.image_charges_q1s = self.image_charges_q1s[:2]

        return self.image_charges_q5s, self.image_charges_q4s, self.image_charges_q3s, self.image_charges_q2s, self.image_charges_q1s 
    

def main():

    ### consider charge trap at a distance R_CT

    R_CT = np.linspace(-50,50,201)

    V_in_medium1_a = np.empty_like(R_CT)
    V_in_medium1_b = np.empty_like(R_CT)
    E_med1_a = np.empty((R_CT.shape[0],3))
    E_med1_b = np.empty((R_CT.shape[0],3))

    T_OX = 5 ### IN NM
    T_SIGE = 60 ### IN NM
    T_QW = 9   ### IN NM 

    # EP_QW = 11.7
    # EP_SIGE = 13
    # EP_OX = 3.9 ## SiO2 

    EP_QW = 11
    EP_SIGE = 11
    EP_OX = 11 ## SiO2 

    ## Dot location where e field and potential needs to be calculated 
    Z = 67       ### in qw
    Y = 0
    X = 0
    
    
    ## charge trap location 
    #X_CT = loops over RCT  ## in nm
    Y_CT = 0  ## in nm
    Z_CT = 4.9 ## in nm  ### at the oxide interface


    het = Charge_in_medium3(ee, Z_CT, Y_CT, x_ct=10, ep_qw=EP_QW, ep_sige=EP_SIGE, ep_ox=EP_OX, t_sige=T_SIGE, t_ox=T_OX, r=1e-4)

    img_chrgs = het.calc_image_charges() 

    print(img_chrgs)

    for i in range(R_CT.shape[0]):
        ### Assume that R is in X direction , Y is zero. direction doesn't matter

        X_CT = R_CT[i] ## in nm

        #heta = Charge_in_medium3(ee, Z_CT, Y_CT, X_CT, EP_QW, EP_SIGE, EP_OX, T_SIGE, T_OX, 1e-6)
        heta = Charge_in_medium3(-ee, Z_CT, Y_CT, X_CT, EP_QW, EP_SIGE, EP_OX, T_SIGE, T_OX, 1e-6)

        img_chrgs = heta.calc_image_charges() 

        #print(img_chrgs)


        V_in_medium1_a[i] = heta.calc_potential_medium1(X, Y, Z)   ### qw
        E_med1_a[i,:] = heta.calc_ele_medium1(X, Y, Z)               ### qw

        #print(V_in_medium1_a, "in mV", E_med1_a , "in mV/nm")
        #print(V_in_medium2, "in mV", E_med2 , "in mV/nm")


        X_CT = R_CT[i]+0.1 ## in nm

        #hetb = Charge_in_medium3(ee, Z_CT, Y_CT, X_CT, EP_QW, EP_SIGE, EP_OX, T_SIGE, T_OX, 1e-6)
        hetb = Charge_in_medium3(ee, Z_CT, Y_CT, X_CT, EP_QW, EP_SIGE, EP_OX, T_SIGE, T_OX, 1e-6)

        img_chrgs = hetb.calc_image_charges() 

        #print(img_chrgs)

        V_in_medium1_b[i] = hetb.calc_potential_medium1(X, Y, Z)   ### qw 
        E_med1_b[i,:] = hetb.calc_ele_medium1(X, Y, Z)               ### qw 

        if i%20 ==0:
            print(i)
            print(img_chrgs)
        #print(V_in_medium1_b, "in mV", E_med1_b , "in mV/nm")
        #print(V_in_medium2, "in mV", E_med2 , "in mV/nm")


    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)  # 3 row, 1 columns

    # Labels for axes
    labels = ['EZ', 'EY', 'EX']

    # Loop through each subplot
    for i, ax in enumerate(axes):
        ax.scatter(R_CT, E_med1_a[:, i], alpha=0.7)  # Scatter plot
        ax.set_title(labels[i])
        ax.set_xlabel('R_CT')
        if i == 0:
            ax.set_ylabel('E_med1_a[:, i]')

    plt.tight_layout()  # Adjust spacing
    plt.show()

    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))  # 1 row, 1 columns

    # Labels for axes
    labels = ['EZ', 'EY', 'EX']

    ratio = np.divide(E_med1_a[:,2], E_med1_a[:,0], dtype=np.float64)  # Ensures precision

    ax.scatter(R_CT, ratio, alpha=0.7)  # Scatter plot
    ax.set_title('EX/EZ, EY=0')
    ax.set_xlabel('R_CT')

    plt.tight_layout()  # Adjust spacing
    plt.show()

    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))  # 1 row, 1 columns

    # Labels for axes
    labels = ['EZ', 'EY', 'EX']

    ratio2 = np.divide(E_med1_a[:,0], E_med1_a[:,2],  out=np.zeros_like(E_med1_a[:,0]), where=E_med1_a[:,2]!=0, dtype=np.float64)  # Ensures precision

    ax.scatter(R_CT, ratio2, alpha=0.7)  # Scatter plot
    ax.set_title('EX/EZ, EY=0')
    ax.set_xlabel('R_CT')

    plt.tight_layout()  # Adjust spacing
    plt.show()

    print(E_med1_a[:,1])


if __name__ == "__main__":
    main()