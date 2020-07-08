###Title: Plot the Total Density of States for each Orbital and Species
###Insitiution: University of Sydney - School of Physics
###Authour: Oliver Conquest
###Aknowledgments: The script that generates the DOSn files for each atom as been adopted 
###from VTST tools created by the Condensed Matter Theory group at the University of Texas.
###Files this script must be in the same directory as the INCAR, DOSCAR, POSCAR/CONTCAR (Rename CONTCAR to POSCAR), PROCAR and OUTCAR files
###Date Last Updated: 20-01-2020 Version 1.0

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import aselite as ase
from tkinter import Tk
from tkinter import filedialog
import csv
import sys
import os

sns.set()
sns.set_style("darkgrid") #Use Seaborn styles for the graphs

#####Method for User Input#####
def userInput(message):
    choose=input(message)
    try:
        str(choose)
    except ValueError:
        print('Your input was not a string please rerun the script')
        return userInput(message)
    if(choose=='y' or choose=='ye'or choose=='yes' or choose=='es'):
        return 'y'
    if(choose=='n' or choose=='no'or choose=='on' or choose=='o'):
        return 'n'
    else:
        print('The input string was not recognised as a yes or no. Please input y (for yes) or n (for no).')
        return userInput(message)


#####CHOOSE THE WORKING DIRECTORY#####
chooseDIR=userInput('Is this script located in your working directory? y/n:')
if(chooseDIR=='y'):
    DIR=os.getcwd()
else:
    root = Tk()
    root.wm_attributes('-topmost',1)
    root.withdraw()
    DIR=filedialog.askdirectory(initialdir=os.getcwd())
print('Your working directory is: '+DIR)
    
#############################################################################
#Split and sum the DOS of each atom into its own file, DOS0 is the Total DOS#
#Adopted from VTST Tools 'split_dos.py' script for Python 2.7               #
#############################################################################

#Reads the DOSCAR file
def read_dosfile():
    path=os.path.join(DIR,'DOSCAR')
    f = open(path, 'r')
    lines = f.readlines() #Saves contents of DOSCAR file as string
    f.close()
    index = 0
    natoms = int(lines[index].strip().split()[0])
    index = 5
    nedos = int(lines[index].strip().split()[2])
    efermi = float(lines[index].strip().split()[3])
    print(index, natoms, nedos, efermi)

    return lines, index, natoms, nedos, efermi

#Read POSCAR file and save the atom positions
def read_posfile(): 
    from ase.io import read #Package that recognises the VASP file format
    try:
        atoms = read('POSCAR')
    except IOError:
        print("[__main__]: Couldn't open input file POSCAR, atomic positions will not be written...\n")
        atoms = []
    return atoms

#Generates the DOS0 file with the Total Density of states and Integrated Density of States
def write_dos0(lines, index, nedos, efermi):

    path=os.path.join(DIR,'DOS0')
    fdos = open(path, 'w')
    line = lines[index+1].strip().split()
    ncols = int(len(line))
    n=0

    while n < nedos:
        index +=1
        e = float(lines[index].strip().split()[0])
        e_f = e-efermi #energy is zero at the fermi energy
        fdos.write('%15.8f ' % (e_f))

        for col in range(1, ncols):
            dos = float(lines[index].strip().split()[col])
            fdos.write('%15.8f ' % (dos))
        fdos.write('\n')
        n+=1
    return index

#Used if there is no polarisation component to the orbitals
def write_nospin(lines, index, nedos, natoms, ncols, efermi):
    
    atoms = read_posfile()
    if len(atoms) < natoms:
    	pos = np.zeros((natoms, 3))
    else:
        pos = atoms.get_positions()

    for i in range(1,natoms+1):
        si = str(i)

    ## OPEN DOSi FOR WRITING ##
        path=os.path.join(DIR,'DOS'+si)
        fdos = open(path, 'w')
        index += 1
        ia = i-1
        n=0
        # fdos.write('# %d \n' % (ncols))
        fdos.write('# %15.8f %15.8f %15.8f \n' % (pos[ia,0], pos[ia,1], pos[ia,2])) #Writes the position to the DOSn file

    ### LOOP OVER NEDOS ###
        while n < nedos:
            index += 1
            e = float(lines[index].strip().split()[0])
            e_f = e-efermi
            fdos.write('%15.8f ' % (e_f))

            for col in range(1, ncols):
                dos = float(lines[index].strip().split()[col])
                fdos.write('%15.8f ' % (dos))
            fdos.write('\n')
            n+=1
    fdos.close()

#Used if orbitals have polarised component spin up and spin down states
def write_spin(lines, index, nedos, natoms, ncols, efermi):
    atoms = read_posfile()
    if len(atoms) < natoms:
        pos = np.zeros((natoms, 3))
    else:
        pos = atoms.get_positions()

    nsites = int((ncols -1)/2)

    for i in range(1,natoms+1):
        si = str(i)
    ## OPEN DOSi FOR WRITING ##
        path=os.path.join(DIR,'DOS'+si)
        fdos = open(path, 'w')
        index += 1
        ia = i-1
        n=0
        fdos.write('# %d \n' % (ncols))
        fdos.write('# %15.8f %15.8f %15.8f \n' % (pos[ia,0], pos[ia,1], pos[ia,2]))

    ### LOOP OVER NEDOS ###
        while n < nedos:
            index +=1   
            e = float(lines[index].strip().split()[0])
            e_f = e-efermi
            fdos.write('%15.8f ' % (e_f))

            for site in range(nsites):
                dos_up = float(lines[index].strip().split()[site*2+1])
                dos_down = float(lines[index].strip().split()[site*2+2])*-1
                fdos.write('%15.8f %15.8f ' % (dos_up, dos_down))
            fdos.write('\n')
            n+=1
        fdos.close()   

if __name__ == '__main__':
    import datetime
    import time
    import optparse
    runSplit=userInput('Run Split Density of States Code y/n: ')
    if(runSplit=='y'):
        lines, index, natoms, nedos, efermi = read_dosfile()
        index = write_dos0(lines, index, nedos, efermi)
        ## Test if a spin polarized calculation was performed ##
        line = lines[index+2].strip().split()
        ncols = int(len(line)) 
        if ncols==7 or ncols==19 or ncols==9 or ncols==33:
            write_spin(lines, index, nedos, natoms, ncols, efermi)
            is_spin=True
        else: 
            write_nospin(lines, index, nedos, natoms, ncols, efermi)
            is_spin=False
        print("Spin unrestricted calculation: ", is_spin)
    else:
        print('It is assumed the DOSn files have been generated.')


#################################################################################
#Reads the Individual DOSn files and plots the total DOS for each atomic species#
#################################################################################
from os import listdir
from os.path import isfile, join
import sys

#Finds the DOSn files in the current working directory and sorts them into accending order
DOSfiles = [f for f in listdir(DIR) if isfile(join(DIR, f)) and 'DOS' in f and f[3:len(f)].isnumeric()]
if(len(DOSfiles) < 2):
    print('Please check that the DOSn files have been generated. If your system is only a single atom you should expect to see atleast a single DOSn file')
    quit()
else:
    DOSfiles = sorted(DOSfiles, key=lambda a: int(a.split("S")[1])) #Sorts the DOSn files in numerical order

#This reads the atomic species name and quantity of each species, used for later summation. 
posPath=os.path.join(DIR,'POSCAR')
Pos = open(posPath, 'r')
for n in range(5):
    Pos.readline()
Natoms=Pos.readline().split()
try:
    check=int(Natoms[0])
    print(Natoms)
    Species=[]
except ValueError:
    Species=Natoms #Stores the species names if they are in the POSCAR file
    Natoms=Pos.readline().split()
if(len(Species)==len(Natoms)):  #Check the lists have the same length
    print('Species names have been recorded and teh quantity of atomic names matches quantity of atom numbers.')
    print(Species,Natoms)
if(len(Species)==0):
    print('The species names could not be read from the POSCAR file. Default names will be assigned.')
    for i in range(0,len(Natoms)):
        Species.append('Species '+str(i+1))
if(len(Species)!=len(Natoms)):
    print('There seems to be more atoms specified than expected. Please check files and restart.')
    quit()
Natoms=[int(x) for x in Natoms]
Pos.close()

def DOSCARformat():
    incarPath=os.path.join(DIR,'INCAR')
    try:
        INCAR = list(open(incarPath, 'r'))
    except FileNotFoundError:
        print('Please check the INCAR file is in the working directory')
        quit() #Could implement directory choice

    #Determine the value of INCAR paramaters that affect the DOSCAR file (inlude LMAXMIN search)
    ISPIN=1   #Default Value
    LORBIT='none'   #Default Value
    for i in range(0,len(INCAR)):
        if('ISPIN' in INCAR[i]): #Check if the default parameters have been used
            ISPIN=int(INCAR[i].split()[2]) 
        if('LORBIT' in INCAR[i]): 
            LORBIT=int(INCAR[i].split()[2])
    print('ISPIN = ' + str(ISPIN) + ', LORBIT = ' + str(LORBIT))

    if(LORBIT=='none'):
        LORBIT='default'
        return ISPIN,LORBIT
    if(LORBIT==1 or LORBIT==12 or LORBIT==11 or LORBIT==12):
        LORBIT='lm-resolved'
        return ISPIN,LORBIT
    else:
        LORBIT='l-decomposed'
        return ISPIN,LORBIT

#Provides the format of the DOSCAR file using the previous method
DOSformat=list(DOSCARformat())
print(sum(Natoms),len(DOSfiles))
print(DOSformat)

#####Get Total Density of States#####
def DOStotal():
    if(DOSformat[0]==1): #Non-polarised case
        dos0Path=os.path.join(DIR,'DOS0')
        with open(dos0Path,'r') as f:
            reader = csv.reader(f)
            data = list(reader)

        e=[]
        x=[]
        for i in range(1,len(data)):
            e.append(float(data[i][0].split()[0]))
            x.append(float(data[i][0].split()[1]))
        return e,x
    
    if(DOSformat[0]==2): #Polarised case
        dos0Path=os.path.join(DIR,'DOS0')
        with open(dos0Path,'r') as f:
            reader = csv.reader(f)
            data = list(reader)

        e=[]
        up=[]
        down=[]
        for i in range(1,len(data)):
            e.append(float(data[i][0].split()[0]))
            up.append(float(data[i][0].split()[1]))
            down.append(float(data[i][0].split()[2]))
        return e,up,down

####DOS Orbital Method#####
def DOSorbital(Case):
    dos1Path=os.path.join(DIR,'DOS1')
    Total=[]
    i=0
    Sum=1
    Start=0
    if(list(open(dos1Path))[0].split()[0]=='#'): #Accounts for the atomic position included in DOSn files 
        Start=1
    if(list(open(dos1Path))[1].split()[0]=='#'):
        Start=2
    length=len(list(open(dos1Path))[Start].split())

    while i < len(Natoms):
        tmp=[[] for n in range(0,length)]
        Nextatom=1
        for j in range(Sum,Sum+Natoms[i]):
            DOS = list(open(DIR+'\\'+DOSfiles[j], 'r'))
            for k in range(Start,len(DOS)):
                if(Nextatom==1):
                     tmp[0].append(float(DOS[k].split()[0]))
                for m in range(1,length):
                    if(Nextatom==1):
                        tmp[m].append(float(DOS[k].split()[m]))
                    else:
                        tmp[m][k-Start]=tmp[m][k-Start]+float(DOS[k].split()[m])
            Nextatom=0
        Sum=Sum+Natoms[i]
        Total.append(tmp)
        i+=1
    print('The number of atomic species: '+str(len(Total)))
    
    ####Plot the Orbitals of each Species
    if (Case==1):
        orbitFormat=['s','p_y','p_z','p_x','d_xy','d_yz','d_z2-r2','d_xz','d_x2-y2']
        Title='Density of States (Nonpolarised and lm-Resolved)'
    if(Case==2):
        orbitFormat=['s','p','d']
        Title='Density of States (Nonpolarised and l-Decomposed)'
    if(Case==3):
        orbitFormat=['s-up','s-down','p_y-up','p_y-down','p_z-up','p_z-down','p_x-up','p_x-down','d_xy-up','d_xy-down','d_yz-up','d_yz-down','d_z2-r2-up','d_z2-r2-down','d_xz-up','d_xz-down','d_x2-y2-up','d_x2-y2-down']
        Title='Density of States (Polarised and lm-Resolved)'
    if(Case==4):
        orbitFormat=['s-up','s-down','p-up','p-down','d-up','d-down']
        Title='Density of States (Polarised and l-Decomposed)'
    plt.figure(figsize=(20,10))
    if(len(list(DOStotal()))==2):
        plt.plot(list(DOStotal())[0],list(DOStotal())[1],color='k',label='Total Density of States')
        plt.fill_between(list(DOStotal())[0],list(DOStotal())[1],step="pre", alpha=0.3, color='k')
    if(len(list(DOStotal()))==3):
        plt.plot(list(DOStotal())[0],list(DOStotal())[1],color='m',label='Total Spin Up Density of States')
        plt.fill_between(list(DOStotal())[0],list(DOStotal())[1],step="pre", alpha=0.3, color='m')
        negspin=[-x for x in list(DOStotal())[2]]
        plt.plot(list(DOStotal())[0],negspin,color='y',label='Total Spin Down Density of States')
        plt.fill_between(list(DOStotal())[0],negspin,step="pre", alpha=0.3, color='y')
    sns.set_palette(sns.color_palette("hls", len(Total)*length)) #Use this line to change the colour palette of the plot
    for i in range(0,len(Total)):
        for k in range(1,length):
            plt.plot(Total[i][0],Total[i][k], label=str(Species[i])+' '+orbitFormat[k-1]+'-Orbital') #Implement scalable species name
    plt.axvline(x=0, linestyle='--', color='k', label='Fermi Level')
    plt.legend(loc='upper left', fontsize=6)
    plt.xlabel('Energy (eV)')
    plt.ylabel('Density of States (States/eV)')
    plt.title(Title)
    fig=plt.gcf()
    plt.show(block=False)

    #Option to save your plot
    save=userInput('Would you like to save this plot as a PDF to your current working directory? y/n ')
    if(save=='y'):
        fig.savefig(DIR+'\\'+'DOS_Orbital_Plot.pdf',dpi=600, format='pdf')
        quit()
    else:
        quit()


####Case 1: nonpolarised and lm-resolved####
if(DOSformat[0]==1 and DOSformat[1]=='lm-resolved' and sum(Natoms)==len(DOSfiles)-1):
    print('DOSCAR file format is non-polarised and lm-resolved')
    DOSorbital(1)

####Case 2 nonpolarised and l-decomposed####
if(DOSformat[0]==1 and DOSformat[1]=='l-decomposed' and sum(Natoms)==len(DOSfiles)-1):
    print('DOSCAR file format is non-polarised and l-decomposed')
    DOSorbital(2)

####Case 3 polarised and lm-resolved####
if(DOSformat[0]==2 and DOSformat[1]=='lm-resolved' and sum(Natoms)==len(DOSfiles)-1):
    print('DOSCAR file format is polarised and l-decomposed')
    DOSorbital(3)

####Case 4 polarised and l-decomposed####
if(DOSformat[0]==2 and DOSformat[1]=='l-decomposed' and sum(Natoms)==len(DOSfiles)-1):
    print('DOSCAR file format is polarised and l-decomposed')
    DOSorbital(4)              