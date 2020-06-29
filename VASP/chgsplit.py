####chgsplit.py script reads any spin polarised PARCHG file and splits it into the total and magnetic components####
####Date last updated: 29/06/2020####
####Author: Oliver Conquest####
####Institution: University of Sydney####
####Group: Condensed Matter Theory Group####

import os
import numpy as np
from tkinter import Tk
from tkinter import filedialog
import multiprocessing as mp

#####User selection of the working directory#####
def getDIR():
    chooseDIR=input('Is this script located in your working directory? y/n:')
    if(chooseDIR=='y'):
        DIR=os.getcwd()
        print('Your working directory is: '+DIR)
        return DIR
    else:
        root = Tk()
        root.wm_attributes('-topmost',1)
        root.withdraw()
        DIR=filedialog.askdirectory(initialdir=os.getcwd())
        os.chdir(DIR)
        print('Your working directory is: '+DIR)
        return DIR

#####Search cwd for PARCHG files#####
def checkFiles():
    PATH = getDIR()
    FILES = [f for f in os.listdir(PATH) if os.path.isfile(f)]
    TMP = []
    for F in FILES:
        if("PARCHG" in F):
            TMP.append(F)
    FILES = TMP
    return FILES

#####Split the PARCHG files into total and magnetic components#####
def splitFiles(FILE):
    LINE = ""
    EMPTY = 0
    COUNT = 0
    CHARGCOUNT = 0
    ATOMNUM = 0
    GRIDLOC = 0
    GRIDSIZE = 0
    FILEIN = open(FILE,'r')
    FILEOUT1 = open("tot_"+FILE,'w')
    FILEOUT2 = open("mag_"+FILE,'w')

    while EMPTY < 10:
        
        LINE = FILEIN.readline()

        ##Writes the POSCAR format lines required at the start of the file along with the dimensions
        if(GRIDLOC == 0 or COUNT <= GRIDLOC):
            FILEOUT1.write(LINE)
            FILEOUT2.write(LINE)

        ##Writes the charge density block for both the total and the magnetic components
        if(len(LINE.split()) == 10):
            CHARGCOUNT += 1
            if(CHARGCOUNT <= GRIDSIZE):
                FILEOUT1.write(LINE)
            if(CHARGCOUNT > GRIDSIZE):
                FILEOUT2.write(LINE)

        ##Provides a break condition for the while loop
        if(EMPTY > 10):
            break
        if(LINE == ""):
            EMPTY += 1
        else:
            EMPTY = 0

        ##Determines the number of atoms in the system and calculates the location of the grid dimensions based on the file format
        if(COUNT == 6):
            try:
                ATOMNUM = sum([int(A) for A in LINE.split()])
                GRIDLOC = COUNT+ATOMNUM+3
                print(f"Number of Atoms in the system is: {ATOMNUM} and the location of the x,y and z grid point numbers is on line {GRIDLOC} of this file.")
            except ValueError:
                print("Cannot find number of atoms at the start of the file.")
        ##Determines the grid size and divides by 10 since PARCHG and CHG files only record the charge density for every 10th step 
        if(COUNT == GRIDLOC and COUNT != 0):
            try:
                GRIDSIZE = np.prod([int(N) for N in LINE.split()])/10
                print(f"The number of grid points is: {GRIDSIZE}")
            except ValueError:
                print("Could not calculate the number of grid points for this system file.")

        

        COUNT += 1
    FILEIN.close()
    FILEOUT1.close()
    FILEOUT2.close()

##This conditional may not be necessary but the multiprocessing library may return an error if it is not present
if __name__ == '__main__':
    FILES = checkFiles()
    print(FILES)
    pool = mp.Pool(mp.cpu_count())
    pool.map(splitFiles, FILES)
    pool.close()