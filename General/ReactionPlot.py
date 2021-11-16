#Authour: Oliver J. Conquest
#Organisation: University of Sydney
#Group: Condensed Matter Theory Research Group
#Date: 16/11/21 

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file1 = open("Input-CoTPP.csv","r")

f1_lines = file1.readlines()

Input = [line.strip("\n").split(",") for line in f1_lines]

#Initial lists for plotting
plt_Input = [[] for i in range(len(Input[0])+1)]

#Convert string numbers to int and float
for i in range(0,len(Input)):
    for k in range(0,len(Input[0])):
        if(i == 0):
            plt_Input[0].append(Input[i][k])
        if(i > 0 and k == 0):
             plt_Input[1].append(Input[i][k])
        if(i > 0 and k > 0):
            plt_Input[k+1].append(float(Input[i][k]))    

##############################################################################
####global plotting parameters - changes these values to refine your plot#####
##############################################################################
lstyle = '--' #line style of the connecting lines "--" for dash, "-." for dash-dot and ":" for dot, "-" gives a solid line.
linewidth = 1 #linewidth of the connecting lines
marker_size = 45 #marker box dimensions in points - recommend 30-50% of dpi value
marker_linewidth = 3 #sets the "thickness" or "boldness" of the marker
marker_transparency = 1 #percentage transparency of the marker
fig_x_size = 10.0 #inches
fig_y_size = 6.0 #inches
dpi = 120 #number of pixels per inch (ppi) - depending on the plot size, plot shift due to xlabel names dpi value should be adjusted until it matches nicely with the markers
plt.figure(figsize=(fig_x_size,fig_y_size),dpi = dpi) #set figure size
plt.xlabel("Reaction Step")
xtick_rotation = 45 #rotation of the x-ticks (or labels) in degrees 
plt.ylabel("Energy (eV)")
color_set = sns.color_palette("colorblind", len(plt_Input)-2) #choose the color palette - see seaborn documentaion for more palettes
Reaction_Step = list(np.linspace(1,len(plt_Input[1]),len(plt_Input[1]))) #creates a number array for the reaction steps

#####Generate reaction plot#####
for i in range(2,len(plt_Input)):
    plt.scatter(Reaction_Step,plt_Input[i],marker="_",s=(marker_size*72/dpi)**2,linewidth=marker_linewidth,color=color_set[i-2],alpha=marker_transparency,label=plt_Input[0][i-1],zorder=3)

    #Matplotlib fundamentals: figure() has dpi = 100 and figure_size = (6.4, 4.8) inches so 640 pixels horizontal and 480 pixels vertical.
    #Marker size is in units of points; in matplotlib we have 72 points per inch (ppi) so 1 point is 1/72 inches.
    xlow, xhigh = plt.xlim()
    ylow, yhigh = plt.ylim()
    xmarker_correction = (((marker_size*72/dpi))/(fig_x_size*dpi))*(xhigh-xlow) #distance from the center of the marker to its edge in the x direction
    ymarker_correction = (((marker_linewidth*72/dpi))/(fig_y_size*dpi))*(yhigh-ylow) #distance from the center of the marker to its edge in the y direction

    for k in range(0,len(plt_Input[1])-1):
        Line_x1 = Reaction_Step[k]+xmarker_correction
        Line_x2 = Reaction_Step[k+1]-xmarker_correction
        if(plt_Input[i][k] > plt_Input[i][k+1]):
            Line_y1 = plt_Input[i][k]-ymarker_correction
            Line_y2 = plt_Input[i][k+1]+ymarker_correction
        if(plt_Input[i][k] < plt_Input[i][k+1]):
            Line_y1 = plt_Input[i][k]+ymarker_correction
            Line_y2 = plt_Input[i][k+1]-ymarker_correction
        if(plt_Input[i][k] == plt_Input[i][k+1]):
            Line_y1 = plt_Input[i][k]
            Line_y2 = plt_Input[i][k+1]
        plt.plot([Line_x1,Line_x2],[Line_y1,Line_y2],linestyle=lstyle,linewidth=linewidth,color=color_set[i-2],zorder=1)
    
plt.legend()
plt.xticks(Reaction_Step, plt_Input[1], rotation = 45)
plt.tight_layout() #Avoid labels being cutoff!
plt.savefig("CoTPP-Plot.pdf",dpi=dpi*3,format="pdf")


