from config import *


class Image_charge_calculator:

    ### Following ELECTRIC FIELDS IN DIELECTRIC MULTI-LAYERS CALCULATED BY DIGITAL COMPUTER by Takeshi Takashima an, Ryozo Ishibashi
    ### IEEE Trans. Electr. Insul, Vol EI-13, No 1, February 1978 

    ###################################################################################################################################################

    def __init__(self, q_ct, z_ct, y_ct, x_ct, ep_qw, ep_sige, ep_ox, t_sige, t_ox, r):
        
        self.q_ct = q_ct  # Initial charge q_1i
        self.z_ct = z_ct # position of initial charge q 
        self.x_ct = x_ct
        self.y_ct = y_ct
        self.ep1 = ep_qw  # dielectric constant 1 (rightmost layer)
        self.ep2 = ep_sige  # dielectric constant 2 (middle layer)
        self.ep3 = ep_ox  # dielectric constant 3 (leftmost layer, has conductor to the left of it) 
        #self.a = a  # thickness dielectric 1
        self.b = t_sige  # thickness dielectric 2
        self.c = t_ox  # thickness dielectric 3
        self.delta = r  # Small positive number for termination condition
        self.image_charges_q5s = []  # Store generated image charges
        self.image_charges_q4s = []  # Store generated image charges
        self.image_charges_q3s = []  # Store generated image charges
        self.image_charges_q2s = []  # Store generated image charges
        self.image_charges_q1s = []  # Store generated image charges

        self.alpha12 = ( self.ep1 - self.ep2 )/ (self.ep1 + self.ep2)
        self.beta12 = 1- self.alpha12

        self.alpha21 = -self.alpha12
        self.beta21 = 1 - self.alpha21

        self.alpha23 = ( self.ep2 - self.ep3 )/ (self.ep2 + self.ep3)
        self.beta23 = 1 - self.alpha23

        self.alpha32 = - self.alpha23 
        self.beta32 = 1 - self.alpha32

        #self.q0 = self.alpha12* self.q_initial
        #self.q11 = self.beta12 * self.q_initial

    def rule_i(self, q1i, z1i, level):

        if abs(q1i / self.q_ct) < self.delta:
            return  # Termination condition

        q2j = self.alpha23 * q1i
        z2j =  - z1i + 2* self.c
        q3k = self.beta23 * q1i
        z3k =  z1i
        
        self.image_charges_q2s.append((q2j, z2j, level, 'q2j'))
        self.image_charges_q3s.append((q3k, z3k, level, 'q3k'))
        
        self.rule_ii(q2j, z2j, level + 1)
        self.rule_iii(q3k, z3k, level + 1)

    def rule_ii(self, q2i, z2i, level):

        if abs(q2i / self.q_ct) < self.delta:
            return  # Termination condition
        
        q1j = self.alpha21 * q2i
        z1j = 2*(self.b + self.c) - z2i
        q5k = self.beta21 * q2i
        z5k = z2i
        
        self.image_charges_q1s.append((q1j, z1j, level, 'q1j'))
        self.image_charges_q5s.append((q5k, z5k, level, 'q5k'))

        #print("image charge = ", q5k , "co-ordinate = ", x5k, "level =", level, "\n")
        
        self.rule_i(q1j, z1j, level + 1)

    def rule_iii(self, q3i, z3i, level):

        #if abs(q3i / self.q_ct) < self.delta:
        #    return  # Termination condition

        q4j = -1 * q3i
        z4j = -z3i
        
        self.image_charges_q4s.append((q4j, z4j, level, 'q4j'))
        self.rule_iv(q4j, z4j, level + 1)

    def rule_iv(self, q4i, z4i, level):

        if abs(q4i / self.q_ct) < self.delta:
            return  # Termination condition

        q3j = self.alpha32 * q4i
        z3j = -z4i + 2*self.c
        q2k = self.beta32 * q4i
        z2k = z4i
        
        self.image_charges_q3s.append((q3j, z3j, level, 'q3j'))
        self.image_charges_q2s.append((q2k, z2k, level, 'q2k'))
        
        self.rule_iii(q3j, z3j, level + 1)
        self.rule_ii(q2k, z2k, level + 1)

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

        return self.image_charges_q5s, self.image_charges_q4s, self.image_charges_q3s, self.image_charges_q2s, self.image_charges_q1s
 
class Charge_in_medium3(Image_charge_calculator):

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

        return len(self.image_charges_q5s)
    
    def calc_potential_medium1(self, x, y, z):

        pot = 0

        for image_chrg in self.image_charges_q5s:

            pot = pot+ image_chrg[0]/ math.sqrt((z-image_chrg[1])**2+(y-self.y_ct)**2+(x-self.x_ct)**2)

        return k0/self.ep1*pot
    
    def calc_potential_medium2(self, x, y, z):

        pot=0 

        for image_chrg in self.image_charges_q1s:

            pot = pot+ image_chrg[0]/ math.sqrt((z-image_chrg[1])**2+(y-self.y_ct)**2+(x-self.x_ct)**2)

        for image_chrg in self.image_charges_q2s:

            pot = pot+ image_chrg[0]/ math.sqrt((z-image_chrg[1])**2+(y-self.y_ct)**2 + (x-self.x_ct)**2)

        return k0/self.ep2*pot

    def calc_potential_medium3(self, x, y, z):

        pot=0 

        for image_chrg in self.image_charges_q3s:

            pot = pot+ image_chrg[0]/ math.sqrt((z-image_chrg[1])**2+(y-self.y_ct)**2+ (x-self.x_ct)**2)

        for image_chrg in self.image_charges_q4s:

            pot = pot+ image_chrg[0]/ math.sqrt((z-image_chrg[1])**2+(y-self.y_ct)**2+ (x-self.x_ct)**2)


        return k0/self.ep3*pot
    
    def calc_ele_medium1(self, x, y, z):

        ele = np.zeros(3)

        for ic in self.image_charges_q5s:

            denom = ( (z-ic[1])**2 + (y-self.y_ct)**2 + (x-self.x_ct)**2 )**(3/2)

            ele[0] = ele[0]+ ic[0]*(z-ic[1])/denom

            ele[1] = ele[1]+ ic[0]*(y)/denom

            ele[2] = ele[2]+ ic[0]*(x)/denom

        return k0/self.ep1*ele
    
    def calc_ele_medium2(self, x, y, z):

        ele = np.zeros(3)

        for ic in self.image_charges_q1s:

            denom = ( (z-ic[1])**2 + (y-self.y_ct)**2 + (x-self.x_ct)**2 )**(3/2)

            ele[0] = ele[0]+ ic[0]*(z-ic[1])/denom

            ele[1] = ele[1]+ ic[0]*(y)/denom

            ele[2] = ele[2]+ ic[0]*(x)/denom

        for ic in self.image_charges_q2s:

            denom = ( (z-ic[1])**2 + (y-self.y_ct)**2 + (x-self.x_ct)**2 )**(3/2)

            ele[0] = ele[0]+ ic[0]*(z-ic[1])/denom

            ele[1] = ele[1]+ ic[0]*(y)/denom

            ele[2] = ele[2]+ ic[0]*(x)/denom

        return k0/self.ep2*ele
    
    def calc_ele_medium3(self, x, y, z):

        ele = np.zeros(3)

        for ic in self.image_charges_q3s:

            denom = ( (z-ic[1])**2 + (y-self.y_ct)**2 + (x-self.x_ct)**2 )**(3/2)

            ele[0] = ele[0]+ ic[0]*(z-ic[1])/denom

            ele[1] = ele[1]+ ic[0]*(y)/denom

            ele[2] = ele[2]+ ic[0]*(x)/denom

        for ic in self.image_charges_q4s:

            denom = ( (z-ic[1])**2 + (y-self.y_ct)**2 + (x-self.x_ct)**2 )**(3/2)

            ele[0] = ele[0]+ ic[0]*(z-ic[1])/denom

            ele[1] = ele[1]+ ic[0]*(y)/denom

            ele[2] = ele[2]+ ic[0]*(x)/denom

        return k0/self.ep3*ele




def main():
    Q_CT = 1e-12 ### 1pC in C

    Z_CT = 1e-2 #### cm 
    X_CT = 2E-2 #### cm
    Y_CT = 3E-2 #### cm  

    C = 2e-2 
    B = 1e-2 

    EP3 = 1.7
    EP2 = 4
    EP1 = 1

    het = Charge_in_medium3(Q_CT, Z_CT, Y_CT, X_CT, EP1, EP2, EP3, B, C, 1e-4)

    Img_chrgs = het.calc_image_charges() 

    print(Img_chrgs)

    Z = 3E-2
    Y = 1e-2
    X = 1e-2


    V_in_medium1 = het.calc_potential_medium1(X, Y, Z)
    V_in_medium2 = het.calc_potential_medium2(X, Y, Z)
    E_med1 = het.calc_ele_medium1(X, Y, Z)
    E_med2 = het.calc_ele_medium2(X, Y, Z)

    print(V_in_medium1, V_in_medium2)
    print(E_med1*np.array((EP1,1,1)), E_med2*np.array((EP2,1,1)))

    Z = 3E-2
    Y = 3e-2
    X = 2e-2


    V_in_medium1 = het.calc_potential_medium1(X, Y, Z)
    V_in_medium2 = het.calc_potential_medium2(X, Y, Z)
    E_med1 = het.calc_ele_medium1(X, Y, Z)
    E_med2 = het.calc_ele_medium2(X, Y, Z)

    print(V_in_medium1, V_in_medium2)
    print(E_med1*np.array((EP1,1,1)), E_med2*np.array((EP2,1,1)))

    Z = 3E-2
    Y = 0
    X = 0


    V_in_medium1 = het.calc_potential_medium1(X, Y, Z)
    V_in_medium2 = het.calc_potential_medium2(X, Y, Z)
    E_med1 = het.calc_ele_medium1(X, Y, Z)
    E_med2 = het.calc_ele_medium2(X, Y, Z)

    print(V_in_medium1, V_in_medium2)
    print(E_med1*np.array((EP1,1,1)), E_med2*np.array((EP2,1,1)))


    Z = 2E-2
    Y = 0e-2
    X = 0e-2


    V_in_medium3 = het.calc_potential_medium3(X, Y, Z)
    V_in_medium2 = het.calc_potential_medium2(X, Y, Z)
    E_med3 = het.calc_ele_medium3(X, Y, Z)
    E_med2 = het.calc_ele_medium2(X, Y, Z)

    print(V_in_medium3, V_in_medium2)
    print(E_med3*np.array((EP3,1,1)), E_med2*np.array((EP2,1,1)))

    Z = 2E-2
    Y = 3e-2
    X = 3e-2


    V_in_medium3 = het.calc_potential_medium3(X, Y, Z)
    V_in_medium2 = het.calc_potential_medium2(X, Y, Z)
    E_med3 = het.calc_ele_medium3(X, Y, Z)
    E_med2 = het.calc_ele_medium2(X, Y, Z)

    print(V_in_medium3, V_in_medium2)
    print(E_med3*np.array((EP3,1,1)), E_med2*np.array((EP2,1,1)))


    Z = 2E-2
    Y = 1e-2
    X = 2e-2


    V_in_medium3 = het.calc_potential_medium3(X, Y, Z)
    V_in_medium2 = het.calc_potential_medium2(X, Y, Z)
    E_med3 = het.calc_ele_medium3(X, Y, Z)
    E_med2 = het.calc_ele_medium2(X, Y, Z)

    print(V_in_medium3, V_in_medium2)
    print(E_med3*np.array((EP3,1,1)), E_med2*np.array((EP2,1,1)))

if __name__ == "__main__":
    main()