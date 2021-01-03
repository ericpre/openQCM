

import numpy as np
import matplotlib.pyplot as plt
from numpy import loadtxt

################################################################################################################
def Openfile():
       import os
       import numpy as np
       from numpy import loadtxt
       import tkinter as Tk
       from tkinter import messagebox
       from tkinter.filedialog import askopenfilename
       fExtension='none'
       root =Tk.Tk()
       root.withdraw() # we don't want a full GUI, so keep the root window from appearing
       filename = askopenfilename(initialdir="C:/Users/",
                                 filetypes =(("text files", "*.txt"),("csv files", "*.csv"),("All files","*.*")),
                                 title = "Choose the TXT/CSV file...",
                                 defaultextension = 'txt')
       if filename != '':
          fName,fExtension = os.path.splitext(filename)
          if  fExtension=='.txt':
              #datac = loadtxt(filename)
              #messagebox.showinfo("Information","---TXT IMPORTED---")
              print("Information:","---TXT PLOTTED---")
          elif fExtension=='.csv':
              #datac = np.genfromtxt (filename, delimiter=",")

              #messagebox.showinfo("Information","---CSV IMPORTED---")
              print("Information:","---CSV PLOTTED---")
          else:
              messagebox.showinfo("Information","-FILE NOT VALID-")
       return filename
          
###########################################################################
# BASELINE ESTIMATION
# Estimates Baseline with Least Squares Polynomial Fit (LSP)
###########################################################################
def baseline_estimation(x,y,poly_order):
    # Least Squares Polynomial Fit (LSP)
    coeffs = np.polyfit(x,y,poly_order) 
    # Evaluate a polynomial at specific values
    poly_fitted = np.polyval(coeffs,x) 
    return poly_fitted,coeffs       
  
    
###########################################################################
# BASELINE CORRECTION
# estimates signal-baseline for amplitude and phase
###########################################################################
def baseline_correction(readFREQ,data_mag,data_ph):
    
    # input signal Amplitude
    (_polyfitted_all,s_coeffs_all) = baseline_estimation(readFREQ,data_mag,8)
    _mag_beseline_corrected_all = data_mag-_polyfitted_all
    
    # input signal Phase
    (_polyfitted_all_phase,_coeffs_all_phase) = baseline_estimation(readFREQ,data_ph,8)
    _phase_beseline_corrected_all = data_ph - _polyfitted_all_phase 
    return _mag_beseline_corrected_all, _phase_beseline_corrected_all
###############################################################################

print("SELECT .TXT SCAN FILE: 'Calibrate_5Mhz' or 'Calibrate_10Mhz'")
#filename_scan ='Calibration_10MHz.txt'
#filename ='All_sweep_10Mhz_Air.txt'
filename_scan=Openfile()
data  = loadtxt(filename_scan)
freq  = data[:,0]
mag   = data[:,1]
phase = data[:,2]

(mag_baseline, phase_baseline) = baseline_correction(freq,mag,phase)

fig = plt.figure('')
#plt.rcParams["figure.figsize"] = [16,9]
fig.suptitle('')
ax5 = fig.add_subplot(111)
#plt.axes(xlim=(xLimMax, xLimMin))
plt.xlabel('Frequency (Hz)')
#plt.ylim(10015333,10015340)                    #Set y min and max values
#plt.title('Amplitude/Phase')    #Plot the title
plt.grid(True)                                  #Turn the grid on
plt.ylabel('Phase (deg)')                    #Set ylabels
a0, = plt.plot(freq,phase_baseline,'b', label='Phase', lw=1) 
plt.legend(loc='upper right')                    #plot legend
plt2=plt.twinx()                                #Create a second y axis
#plt.ylim(5000,5300)                            #Set limits of second y axis
a1, = plt2.plot(freq,mag_baseline,'r', label='Amplitude', lw=1)
plt2.set_ylabel('Amplitude (dB)')                  #label second y axis
plt2.ticklabel_format(useOffset=False)          #Force matplotlib to NOT autoscale y axis
plt2.legend(loc='upper left')                   #plot legend
logo = plt.imread('openqcm-logo.png')
ax5.figure.figimage(logo, 5, 5, alpha=1, zorder=1)
plt.rcParams["figure.figsize"] = [16,9]
plt.show()

###############################################################################
#root = Tk()
#root.withdraw()
#dirpath = filedialog.askdirectory()
print("SELECT .CSV OUTPUT FILE")
filename = Openfile()#
import pandas as pd
data = pd.read_csv(filename)

Date = data['Date'].tolist()
Time = data['Time'].tolist()
relative_time = np.asarray(data[['Relative_time']])
Frequency = np.asarray(data[['Resonance_Frequency']])
Dissipation = np.asarray(data[['Dissipation']])
Temperature = np.asarray(data[['Temperature']])


###############################################################################
#PLOT Signal: Amplitude of resonant peaks per sweep
###############################################################################
'''
fig = plt.figure('Figure Title')
fig.suptitle('Signal: Frequency of resonance peaks')
ax5 = fig.add_subplot(111)
#plt.scatter(Frequency, c='r', alpha=0.5, marker='.')
plt.plot(Frequency,'g',lw=1,label="Amplitude of resonant peaks (Raw Data)")
#plt.scatter(sweep_range,vector_max_fit, c='g', alpha=0.5, marker='.')
#plt.plot(Dissipation,'y',lw=1,label="Amplitude of resonant peaks (Fitted Data)")
plt.xlabel('Sweeps Number (time)')
#ax.set_xticklabels(dataf_0[:,0])
plt.ylabel('Frequency(Hz)/Dissipation')
plt.grid(True)
logo = plt.imread('openqcm-logo_m.png')
#plt.rcParams["figure.figsize"] = [16,9]
ax5.figure.figimage(logo, 5, 5, alpha=1, zorder=1)
plt.legend()
plt.show()
'''

fig = plt.figure('')
fig.suptitle('')
#plt.rcParams["figure.figsize"] = [16,9]
ax5 = fig.add_subplot(111)
#plt.axes(xlim=(xLimMax, xLimMin))
plt.xlabel('time (in number of sweeps)')
#plt.ylim(10015333,10015340)                    #Set y min and max values
#plt.title('Resonance Frequency/Dissipation')    #Plot the title
plt.grid(True)                                  #Turn the grid on
plt.ylabel('Frequency (Hz)')                    #Set ylabels
a0, = plt.plot(Frequency,'g', label='Resonance Frequency', lw=1) 
plt.legend(loc='upper right')                    #plot legend
plt2=plt.twinx()                                #Create a second y axis
#plt.ylim(5000,5300)                            #Set limits of second y axis
a1, = plt2.plot(Dissipation,'#edb120', label='Dissipation', lw=1)
plt2.set_ylabel('Dissipation')                  #label second y axis
plt2.ticklabel_format(useOffset=False)          #Force matplotlib to NOT autoscale y axis
plt2.legend(loc='lower right')                   #plot legend
logo = plt.imread('openqcm-logo.png')
ax5.figure.figimage(logo, 5, 5, alpha=1, zorder=1)
plt.show()

###########################################################################################################

fig1 = plt.figure('')
#plt.rcParams["figure.figsize"] = [16,9]
fig1.suptitle('')
host = fig1.add_subplot(111) 
host.grid(True)   
par1 = host.twinx()
par2 = host.twinx()
host.set_xlabel("time (in number of sweeps)") 
host.set_ylabel("Resonance Frequency (Hz)")
par1.set_ylabel("Dissipation")
par2.set_ylabel("Temperature (°C)")

color1 = 'g'
color2 = '#edb120'
color3 = '#7e2f8e'

p1, = host.plot(Frequency,  color=color1, label="Resonance Frequency")
p2, = par1.plot(Dissipation,color=color2, label="Dissipation")
p3, = par2.plot(Temperature,color=color3, label="Temperature")

lns = [p1, p2, p3]
host.legend(handles=lns, loc='best')
logo = plt.imread('openqcm-logo.png')
host.figure.figimage(logo, 5, 5, alpha=1, zorder=1)
# right, left, top, bottom
par2.spines['right'].set_position(('outward', 60))      
# no x-ticks                 
#par2.xaxis.set_ticks([])
# Sometimes handy, same for xaxis
#par2.yaxis.set_ticks_position('right')
plt.show()

print('END')
