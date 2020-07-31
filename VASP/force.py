import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

#####SET THESE VALUES####
SP = input("Would you like to include an inset plot? (y/n) ") #y/n would you like to include an inset plot 
if(SP == 'y'):
    n=int(input("How many starting iterations would you like to remove? ")) # number of points to cut off for sub plot

PATH = os.getcwd()
FORCE = []

###### Return force and position data from the OUTCAR file #####
if(os.path.isfile('OUTCAR')):
    print("OUTCAR file exists")
    F = open('OUTCAR')
    line = ""
    emptyCount = 0
    while "General timing and accounting informations for this job" not in line and emptyCount < 10:
        line = F.readline()
        if(line.replace(" ","") == ""):
            emptyCount += 1
        else:
            emptyCount = 0
        if("TOTAL-FORCE" in line):
            F.readline()
            tmpline = ""
            tmpFORCE = []
            while "--------------" not in tmpline:
                tmpline = F.readline()
                if("-------------" in tmpline): 
                    break
                tmpFORCE.append(tmpline.split())
            FORCE.append(tmpFORCE)

##### Output the force data for each iteration and atom #####

TOTALFORCE = [[] for n in range(len(FORCE[0]))]
XFORCE = [[] for n in range(len(FORCE[0]))]
YFORCE = [[] for n in range(len(FORCE[0]))]
ZFORCE = [[] for n in range(len(FORCE[0]))]
for i in range(len(FORCE)):
    for j in range(len(FORCE[i])):
        TOTALFORCE[j].append(float(FORCE[i][j][3])+float(FORCE[i][j][4])+float(FORCE[i][j][5]))
        XFORCE[j].append(float(FORCE[i][j][3]))
        YFORCE[j].append(float(FORCE[i][j][4]))
        ZFORCE[j].append(float(FORCE[i][j][5]))   
        

MAXTOTALFORCE = []
AVGFORCE = []
for k in range(len(TOTALFORCE[0])):
    MAXTOTALFORCE.append(max([abs(max(list(zip(*TOTALFORCE))[k])), abs(min(list(zip(*TOTALFORCE))[k]))]))
    AVGFORCE.append(np.mean(list(zip(*TOTALFORCE))[k])) 

MAXXFORCE = []
for k in range(len(XFORCE[0])):
    MAXXFORCE.append(max([abs(max(list(zip(*XFORCE))[k])), abs(min(list(zip(*XFORCE))[k]))]))

MAXYFORCE = []
for k in range(len(YFORCE[0])):
    MAXYFORCE.append(max([abs(max(list(zip(*YFORCE))[k])), abs(min(list(zip(*YFORCE))[k]))]))

MAXZFORCE = []
for k in range(len(ZFORCE[0])):
    if(abs(max(list(zip(*ZFORCE))[k])) < abs(min(list(zip(*ZFORCE))[k]))):
        MAXZFORCE.append(min(list(zip(*ZFORCE))[k]))
    else:
        MAXZFORCE.append(max(list(zip(*ZFORCE))[k]))

fig, ax = plt.subplots(figsize=(10,5))
colors=sns.color_palette("hls",4)    
ax.plot(MAXTOTALFORCE, color=colors[0], label='Total')
ax.plot(MAXXFORCE, color=colors[1], label = 'X')
ax.plot(MAXYFORCE, color=colors[2], label = 'Y')
ax.plot(MAXZFORCE, color=colors[3], label = 'Z')
ax.set_title("Cobalt Porphyrin Positive Standard")
ax.set_xlabel('Structural Relaxation Iteration')
ax.set_ylabel('Maximum Force on Atom (eV/A)')
ax.legend()
if(SP == 'y'):
        x=np.linspace(n,len(MAXTOTALFORCE),len(MAXTOTALFORCE)-n)
        ins = inset_axes(ax, width="50%", height="50%", loc=1)
        TotalcloseUp = ins.plot(x, MAXTOTALFORCE[n:], '-', color=colors[0], label='Total')
        XcloseUp = ins.plot(x, MAXXFORCE[n:], '-', color=colors[1], label='X')
        YcloseUp = ins.plot(x, MAXYFORCE[n:], '-', color=colors[2], label='Y')
        ZcloseUp = ins.plot(x, MAXZFORCE[n:], '-', color=colors[3], label='Z')
        leg = ins.legend()
        title = ins.text(.725,.93,f'Initial {n} Iterations Excluded', fontsize = 12, horizontalalignment='center', transform=ax.transAxes)
        ins.tick_params(labelleft=True, labelbottom=True)

fig.tight_layout()
plt.show()

fig.savefig("CoP-Std-Pos.pdf", dpi=600, format='pdf')


##### Uncomment this code if you would like to plot the total forces on each atom #####

"""colors = sns.color_palette("hls", len(FORCE[0]))
for i in range(len(FORCE)):
    for j in range(len(FORCE[i])):
        plt.plot(i,float(FORCE[i][j][3])+float(FORCE[i][j][4])+float(FORCE[i][j][5]), '.', color = colors[j])

plt.show()"""
