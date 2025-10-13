from config import *
from Image_charge_3d import *

### define a class whihc takes into account only the dipole 

def main():

    ### consider charge trap at a distance R_CT

    R_CT = np.linspace(-25,25,201)

    E_med1_a = np.empty((R_CT.shape[0],3))
    E_med1_b = np.empty((R_CT.shape[0],3))

    T_OX = 5 ### IN NM
    T_SIGE = 60 ### IN NM
    T_QW = 9   ### IN NM  ##irrelevnt

    EP_QW = 11.7
    EP_SIGE = 12.75
    EP_OX = 3.9 ## SiO2 

    # EP_QW = 11
    # EP_SIGE = 11
    # EP_OX = 11 ## SiO2 

    ## Dot location where e field and potential needs to be calculated 
    Z = 67       ### in qw
    Y = 0
    X = 0
    
    
    ## charge trap location 
    #X_CT = loops over RCT  ## in nm
    Y_CT = 0  ## in nm
    Z_CT = 5 ## in nm  ### at the oxide interface


    #het = Charge_in_medium3(ee, Z_CT, Y_CT, x_ct=10, ep_qw=EP_QW, ep_sige=EP_SIGE, ep_ox=EP_OX, t_sige=T_SIGE, t_ox=T_OX, r=1e-4)

    #img_chrgs = het.calc_image_charges() 

    #print(img_chrgs)

    for i in range(R_CT.shape[0]):
        ### Assume that R is in X direction , Y is zero. direction doesn't matter
        heta = Charge_in_medium3(-ee, Z_CT, Y_CT, R_CT[i], EP_QW, EP_SIGE, EP_OX, T_SIGE, T_OX, 1e-6)
        img_chrgs = heta.calc_image_charges() 
        E_med1_a[i,:] = heta.calc_ele_medium1(X, Y, Z)               ### qw


        hetb = Charge_in_medium3(-ee, Z_CT, Y_CT, R_CT[i]+0.1, EP_QW, EP_SIGE, EP_OX, T_SIGE, T_OX, 1e-6)
        img_chrgs = hetb.calc_image_charges() 
        E_med1_b[i,:] = hetb.calc_ele_medium1(X, Y, Z)               ### qw 

        if i%20 ==0:
            print(i)
            print(img_chrgs)

    '''

    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)  # 3 row, 1 columns

    # Labels for axes
    labels = ['EZ', 'EY', 'EX']

    # Loop through each subplot
    for i, ax in enumerate(axes):
        #ax.scatter(R_CT, E_med1_a[:, i]-E_med1_b[:,i], alpha=0.7)  # Scatter plot
        ax.scatter(R_CT, E_med1_a[:, i], alpha=0.7, color='blue')  # Scatter plot
        ax.scatter(R_CT, E_med1_b[:, i], alpha=0.7, color='red')  # Scatter plot
        ax.set_title(labels[i])
        ax.set_xlabel('R_CT')
        #if i == 0:
        #    ax.set_ylabel('E_med1_a[:, i]')

    plt.tight_layout()  # Adjust spacing
    plt.show()

    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))  # 1 row, 1 columns

    ratio = np.divide(E_med1_a[:,2], E_med1_a[:,0], dtype=np.float64)  # Ensures precision

    ax.scatter(R_CT, ratio, alpha=0.7)  # Scatter plot
    ax.set_title('EX/EZ, EY=0')
    ax.set_xlabel('X_CT')

    #ax.set_ylim(ymin=-50, ymax=50)

    plt.tight_layout()  # Adjust spacing
    plt.show()

    
    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))  # 1 row, 1 columns

    ratio = np.divide(E_med1_a[:,0], E_med1_a[:,2], dtype=np.float64, out=np.zeros_like(E_med1_a[:,2]), where=(E_med1_a[:,2])!=0)  # Ensures precision

    ax.scatter(R_CT, ratio, alpha=0.7)  # Scatter plot
    ax.set_title('EZ/EX, EY=0')
    ax.set_xlabel('X_CT')

    #ax.set_ylim(ymin=-50, ymax=50)

    plt.tight_layout()  # Adjust spacing
    plt.show()
    
    # Create subplots
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))  # 1 row, 1 columns

    plt.rcParams.update({'font.size': 16}) # Increase overall font size

    ratio = np.divide(E_med1_a[:,2]-E_med1_b[:,2], E_med1_a[:,0]-E_med1_b[:,0], dtype=np.float64)  # Ensures precision

    ax.scatter(R_CT, ratio, alpha=0.7)  # Scatter plot
    ax.set_title('del EX/ del EZ, EY=0, longitudinal disp 1A')
    ax.set_xlabel('X_CT')

    ax.set_ylim(ymin=-2, ymax=2)
    plt.xlim(-20,20)

    plt.tight_layout()  # Adjust spacing
    plt.show()
    
    '''
    # Create subplots
    #fig, ax = plt.subplots(1, 1, figsize=(4, 4))  # 1 row, 1 columns

    from matplotlib.transforms import Bbox

    # --- Define target inner box size (in inches) ---
    inner_width = 3.4     # PRB one-column box width
    inner_height = 2.55

    # --- Compute total figure size with margins ---
    # (these margins roughly account for labels/ticks)
    left_margin = 0.6
    bottom_margin = 0.5
    right_margin = 0.1
    top_margin = 0.2

    fig_width = inner_width + left_margin + right_margin
    fig_height = inner_height + bottom_margin + top_margin

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), constrained_layout=False)

    #clearfig, ax = plt.subplots(constrained_layout=False)
    fig.set_tight_layout(False)

    # --- Adjust axes box ---
    fig.subplots_adjust(
        left=left_margin/fig_width,
        right=1 - right_margin/fig_width,
        bottom=bottom_margin/fig_height,
        top=1 - top_margin/fig_height,
    )

    ratio2 = np.divide(E_med1_a[:,0]-E_med1_b[:,0], E_med1_a[:,2]-E_med1_b[:,2],  out=np.zeros_like(E_med1_a[:,0]), where=(E_med1_a[:,2])!=0, dtype=np.float64)  # Ensures precision

    ax.scatter(R_CT, ratio2, alpha=0.7)  # Scatter plot
    #ax.set_title('del EZ/ del EX, EY=0, longitudinal disp 1A')
    #ax.set_xlabel(r'coordinate of charge trap, $R_{CT}$')

    ax.set_ylim(ymin=np.min(ratio2), ymax=np.max(ratio2))
    ax.set_xlim(xmin=R_CT[0], xmax=R_CT[-1])
    XTICKS = [-25,-20,-25,-15,-10,-5,0, 5, 10, 15, 20, 25]
    YTICKS = [-3, -2, -2, 0, 1, 2, 3]
    ax.set_xticks(XTICKS)
    # --- Increase tick line width and tick label size ---
    ax.tick_params(axis='both', which='both', width=2, length=6, labelsize=10)

    # --- Add black border (axes spines) ---
    for spine in ax.spines.values():
        spine.set_linewidth(1)
        spine.set_color('black')


    plt.savefig("manuscript_delEz_by_delEx_long.png", dpi=300, bbox_inches='tight')
    plt.show()  # Still view in GUI


    print(E_med1_a[:,1])


if __name__ == "__main__":
    main()