### File to calculate variation due to dipole electric field 

from config import *

class dipole_Efield:

    def __init__(self, q, z, a, x, y, ep ):

        self.q = q #charge on dipole 
        self.z = z # disance of dipole centre from obs. pt which is origin in nm
        self.a = a # 2a is length of dipole in nm
        self.x = x # x coordinate of dipole
        self.y = y # y coordinate of the dipole 
        self.ep = ep # dielectric

    def E_Field(self):

        R = np.array([-self.z+self.a,  -self.y, -self.x], dtype=np.float64) 

        Rp = np.array([-self.z-self.a, -self.y, -self.x ], dtype=np.float64)

        R_mag = np.linalg.norm(R)

        Rp_mag = np.linalg.norm(Rp) 

        Ef = k0/self.ep*self.q*(R/R_mag**3 - Rp/Rp_mag**3)

        return Ef 
    
    def E_field_dipole_approx(self):

        P = np.array([-2*self.a, 0, 0])*self.q

        r = np.array([-self.z, -self.y, -self.x])

        rmag = np.linalg.norm(r)

        rhat = r/rmag

        return k0/self.ep*(3*(np.sum(P*rhat))*rhat - P)/(rmag**3)
    

def main():

    X = np.linspace(-100, 100, 200)

    Y = 0 

    Z = -67 

    A = 4.9

    Q = -ee 

    EP = 11

    Efield = np.empty((X.shape[0],3))

    for i in range(X.shape[0]):

        #Efield[i,:] = dipole_Efield(Q, Z, A, X[i], Y, EP).E_Field()
        Efield[i,:] = dipole_Efield(Q, Z, A, X[i], Y, EP).E_field_dipole_approx()
        
        if i%100 ==0 :

            print(i)


    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)  # 3 row, 1 columns

    # Labels for axes
    labels = ['EZ', 'EY', 'EX']

    # Loop through each subplot
    for i, ax in enumerate(axes):
        ax.scatter(X, Efield[:, i], alpha=0.7)  # Scatter plot
        ax.set_title(labels[i])
        ax.set_xlabel('R')
        

    plt.tight_layout()  # Adjust spacing
    plt.show()


    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize=(4, 4), sharey=True)  # 3 row, 1 columns

    # Labels for axes
    labels = ['EZ', 'EY', 'EX']

    ratioXbyZ = np.divide(Efield[:, 2], Efield[:,0] )

    ax.scatter(X, ratioXbyZ, alpha=0.7)  # Scatter plot
    ax.set_title('EX/EZ')
    ax.set_xlabel('R')
        

    plt.tight_layout()  # Adjust spacing
    plt.show()

if __name__ == "__main__":
    main()
        