########energy.py reads the OSZICAR file and plots the eletronic relaxation steps with an inset plot to remove large initial values#####
####Date last updated: 07/08/2020####
####Author: Oliver Conquest####
####Institution: University of Sydney####
####Group: Condensed Matter Theory Group####

import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

#####SET THIS VALUE####
SP = input("Would you like to include an inset plot? (y/n) ") #y/n would you like to include an inset plot 
if(SP == 'y'):
    n=int(input("How many initial electronic steps do you want to remove from the data? ")) # number of points to cut off for sub plot

if(os.path.isfile("OSZICAR") == True):
    FILE = open("OSZICAR",'r')
    LINE = ""
    NEXT = 0
    EMPTY = 0
    IONIC = []
    SC = []
    tmpLEN = []
    SIZE = []


    while EMPTY < 10:
        LINE = FILE.readline()

        if(LINE.replace(" ","") == ""):
            EMPTY += 1
        if(EMPTY >= 10):
            break

        if(len(LINE.split()) >= 1 and LINE.split()[1] == 'F='):
            if(len(SIZE) == 0):
                SIZE.append(len(tmpLEN))
            else:
                SIZE.append(SIZE[-1]+len(tmpLEN))
            tmpLEN = []
            IONIC.append(float(LINE.split()[4]))
        if(len(LINE.split()) >= 1 and len(LINE.split()[0]) == 4):
            tmpLEN.append(int(LINE.split()[1]))
            SC.append(float(LINE.split()[2]))

    fig, ax1 = plt.subplots(figsize=(10,5))
    ax1.set_title('Electronic and Ionic Energy Convergence')

    colors=sns.color_palette("hls",2)
    ax1.set_xlabel('Electronic Relaxation Steps')
    ax1.set_ylabel('Electronic Relaxation Energy (eV)', color=colors[0])
    ax1.plot(SC, '-', color=colors[0], label='Electronic selfconsistency relaxation energies')
    ax1.tick_params(axis='y', labelcolor=colors[0])

    ax2 = ax1.twinx()
    ax2.set_ylabel('Ionic Relaxation (Converged SC) Energy (eV)', color=colors[1])
    ax2.plot(SIZE, IONIC, color=colors[1])
    ax2.tick_params(axis='y', labelcolor=colors[1])

    if(SP == 'y'):
        x=np.linspace(n,len(SC),len(SC)-n)
        ins = inset_axes(ax1, width="50%", height="50%", loc=1)
        EcloseUp = ins.plot(x,SC[n:], '-', color=colors[0], label='Initial SC steps removed')
        title = ins.text(.75,.93,f'Initial {n} Electronic Iterations Excluded', fontsize = 12, horizontalalignment='center', transform=ax1.transAxes)
        ins.tick_params(axis = 'y', labelcolor=colors[0], labelleft=True, labelbottom=True)

    fig.tight_layout()
    plt.show()

    fig.savefig('CoPc-CO2_CM1_Negative.pdf', dpi=600, format='pdf')
        
    
            


