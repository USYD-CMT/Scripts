import os
import csv

path = os.getcwd()
print(path)
DIR=[x[0] for x in os.walk(path)]
print(DIR[0])
inumjobs = len(DIR)
print('The number of sub directories is '+str(inumjobs))
SYS=[]
ENERGY=[]
ELAPSED=[]
MAG=[]
CPU=[]
MEM=[]
SU=[]
MAXATOMFORCE = []


for i in range(0, inumjobs):
  if(DIR[i]!=path):
    os.chdir(DIR[i])
    print(DIR[i])

    if(os.path.isfile('INCAR')==True and os.path.isfile('POSCAR')==True and os.path.isfile('KPOINTS')==True):
      if(os.path.isfile('ENERGY.dat')==True):
        EF=open('ENERGY.dat', 'r')
        En=EF.readlines()
        EF.close()
        Etail=En[-1].split()
        if('E0=' in Etail):
          Engy=float(Etail[int(Etail.index('E0='))+1])
          ENERGY.append(Engy)
        else:
          ENERGY.append('No Value')
        if('mag=' in Etail):
          mag=float(Etail[int(Etail.index('mag='))+1])
          MAG.append(mag)
        else:
          MAG.append('No Value')
      else:
        ENERGY.append('No File')
        MAG.append('No File')

      IF=open('INCAR', 'r')
      Sys=IF.readline().split()[2]
      SYS.append(Sys)
      IF.close()

      if(os.path.isfile('output.txt')==True):
        OF=open('output.txt','r')
        Output=OF.readlines()
        OF.close()
        START=0
        END=0
        if('START_TIME' in Output[0]):
          try:
            START=int(Output[0].split()[4])
            print(START)
          except:
            print('The time index either does not exists or is not in a format that can be converted into an integer.')
        for i in range(int(len(Output)-20),len(Output)):
          if('END_TIME' in Output[i]):
            try:
              END=int(Output[i].split()[4])
              print(END)
            except:
              print('The time index either does not exists or is not in a format that can be converted into an integer.')
            ELAPSED.append(round((END-START)/3600,1))

          if('NCPUs' in Output[i]):
            CPU.append(int(Output[i].split()[5]))
          elif(len(CPU)==len(ENERGY)-1 and i==len(Output)-1):
            CPU.append('No Value')

          if('Memory' in Output[i]):
            MEM.append(str(Output[i].split()[5]))
          elif(len(MEM)==len(ENERGY)-1 and i==len(Output)-1):
            MEM.append('No Value')

          if('Service' in Output[i]):
            SU.append(float(Output[i].split()[2]))
          elif(len(SU)==len(ENERGY)-1 and i==len(Output)-1):
            SU.append('No Value')
        if(END==0):
          ELAPSED.append('No end time recorded')
      else:
        ELAPSED.append('No file')
        CPU.append('No file')
        MEM.append('No file')
        SU.append('No file')

      FORCE = []
      if(os.path.isfile('OUTCAR')==True):
        print("OUTCAR file exists")
        F = open('OUTCAR')
        line = ""
        emptyCount = 0 
        while "General timing and accounting informations for this job" not in line or emptyCount < 10:
            if(emptyCount > 10):
              break
            line = F.readline()
            if(line.replace(" ","")==""):
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

        
        if(len(FORCE) > 0):
            XFORCE = [[] for n in range(len(FORCE[0]))]
            YFORCE = [[] for n in range(len(FORCE[0]))]
            ZFORCE = [[] for n in range(len(FORCE[0]))]
            for i in range(len(FORCE)):
              for j in range(len(FORCE[i])):
                XFORCE[j].append(float(FORCE[i][j][3]))
                YFORCE[j].append(float(FORCE[i][j][4]))
                ZFORCE[j].append(float(FORCE[i][j][5]))

            MAXXFORCE = []
            for k in range(len(XFORCE[0])):
              MAXXFORCE.append(max([abs(max(list(zip(*XFORCE))[k])), abs(min(list(zip(*XFORCE))[k]))]))

            MAXYFORCE = []
            for k in range(len(YFORCE[0])):
              MAXYFORCE.append(max([abs(max(list(zip(*YFORCE))[k])), abs(min(list(zip(*YFORCE))[k]))]))

            MAXZFORCE = []
            for k in range(len(ZFORCE[0])):
              MAXZFORCE.append(max([abs(max(list(zip(*ZFORCE))[k])), abs(min(list(zip(*ZFORCE))[k]))]))
        
            MAXATOMFORCE.append(max([MAXXFORCE[-1],MAXYFORCE[-1],MAXZFORCE[-1]]))
        else:
            MAXATOMFORCE.append('No Value')
      else:
        MAXATOMFORCE.append('No file')

    os.chdir(path)
    print(os.getcwd())

print(SYS,ENERGY,MAG,ELAPSED,CPU,MEM,SU,MAXATOMFORCE)
print(len(SYS),len(ENERGY),len(MAG),len(ELAPSED),len(CPU),len(MEM),len(SU),len(MAXATOMFORCE))
with open('results.csv', 'w') as o:
  writer = csv.writer(o, delimiter=',')
  writer.writerow(['System Name','Ground State Energy (eV)','Magnetic Moment (bohr Magneton)', 'Elapsed Time (Hours)','CPUs Used','Used Memory (GB)','Service Units', 'Force Converged (Max Force on Atom) eV/A'])
  writer.writerows(zip(SYS, ENERGY, MAG, ELAPSED, CPU, MEM, SU, MAXATOMFORCE))

print("Yeah! All done!")
