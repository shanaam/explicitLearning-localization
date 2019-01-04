import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import scipy.ndimage.filters
import scipy.stats as st
import matplotlib.ticker as ticker


#%% set working directory
# os.chdir('c://Users/kineuser/Desktop/Shanaa/exp/explicit/data') #set the working directory AT SCHOOL PC
#os.chdir('E://Shanaa\'s Stuff/Documents/Shanaa/exp/explicit/data') #set the working directory AT HOME
os.chdir('D://shanaa/exp/explicit/data') #set the working directory ON LAPTOP

#%% defining some variables
#set default font for pyplot
plt.rc('font',family='Calibri', size = 9)

interpoints = [50, 90, 130]
#interpoints = np.arange(20, 160)

#Set colours
exp60col = '#0500a0'
imp60col = '#037fc4'
exp30col = '#ff8000'
imp30col = '#e51636'

#%% Confidence interval calculation
def get_locCI(data):
    participantNum = len(data)
    return np.array (st.t.interval(0.95, participantNum-1, loc=np.nanmean(data), scale=st.sem(data, nan_policy='omit')))

#%% makign the plot
def threePointPlot():

    #import Data
    imp30active = pd.read_csv('imp30_activeTapData.csv')
    exp30active = pd.read_csv('exp30_activeTapData.csv')
    imp60active = pd.read_csv('imp60_activeTapData.csv')
    exp60active = pd.read_csv('exp60_activeTapData.csv')
    
    imp30passive = pd.read_csv('imp30_passiveTapData.csv')
    exp30passive = pd.read_csv('exp30_passiveTapData.csv')
    imp60passive = pd.read_csv('imp60_passiveTapData.csv')
    exp60passive = pd.read_csv('exp60_passiveTapData.csv')
    
    
    #Data to plot
    imp30activeDevs = [np.nanmean(imp30active['50 deviation']), np.nanmean(imp30active['90 deviation']), np.nanmean(imp30active['130 deviation'])]
    exp30activeDevs = [np.nanmean(exp30active['50 deviation']), np.nanmean(exp30active['90 deviation']), np.nanmean(exp30active['130 deviation'])]
    imp60activeDevs = [np.nanmean(imp60active['50 deviation']), np.nanmean(imp60active['90 deviation']), np.nanmean(imp60active['130 deviation'])]
    exp60activeDevs = [np.nanmean(exp60active['50 deviation']), np.nanmean(exp60active['90 deviation']), np.nanmean(exp60active['130 deviation'])]

    imp30passiveDevs = [np.nanmean(imp30passive['50 deviation']), np.nanmean(imp30passive['90 deviation']), np.nanmean(imp30passive['130 deviation'])]
    exp30passiveDevs = [np.nanmean(exp30passive['50 deviation']), np.nanmean(exp30passive['90 deviation']), np.nanmean(exp30passive['130 deviation'])]
    imp60passiveDevs = [np.nanmean(imp60passive['50 deviation']), np.nanmean(imp60passive['90 deviation']), np.nanmean(imp60passive['130 deviation'])]
    exp60passiveDevs = [np.nanmean(exp60passive['50 deviation']), np.nanmean(exp60passive['90 deviation']), np.nanmean(exp60passive['130 deviation'])]

    imp30predDevs = [np.nanmean(imp30active['50 deviation'] - imp30passive['50 deviation']), np.nanmean(imp30active['90 deviation'] - imp30passive['90 deviation']), np.nanmean(imp30active['130 deviation'] - imp30passive['130 deviation'])]
    exp30predDevs = [np.nanmean(exp30active['50 deviation'] - exp30passive['50 deviation']), np.nanmean(exp30active['90 deviation'] - exp30passive['90 deviation']), np.nanmean(exp30active['130 deviation'] - exp30passive['130 deviation'])]
    imp60predDevs = [np.nanmean(imp60active['50 deviation'] - imp60passive['50 deviation']), np.nanmean(imp60active['90 deviation'] - imp60passive['90 deviation']), np.nanmean(imp60active['130 deviation'] - imp60passive['130 deviation'])]
    exp60predDevs = [np.nanmean(exp60active['50 deviation'] - exp60passive['50 deviation']), np.nanmean(exp60active['90 deviation'] - exp60passive['90 deviation']), np.nanmean(exp60active['130 deviation'] - exp60passive['130 deviation'])]


    #Confidence Intervals
    
    imp30activeCI = pd.DataFrame([get_locCI(imp30active['50 deviation']), get_locCI(imp30active['90 deviation']), get_locCI(imp30active['130 deviation'])], index = interpoints)
    exp30activeCI = pd.DataFrame([get_locCI(exp30active['50 deviation']), get_locCI(exp30active['90 deviation']), get_locCI(exp30active['130 deviation'])], index = interpoints)
    imp60activeCI = pd.DataFrame([get_locCI(imp60active['50 deviation']), get_locCI(imp60active['90 deviation']), get_locCI(imp60active['130 deviation'])], index = interpoints)
    exp60activeCI = pd.DataFrame([get_locCI(exp60active['50 deviation']), get_locCI(exp60active['90 deviation']), get_locCI(exp60active['130 deviation'])], index = interpoints)
    
    imp30passiveCI = pd.DataFrame([get_locCI(imp30passive['50 deviation']), get_locCI(imp30passive['90 deviation']), get_locCI(imp30passive['130 deviation'])], index = interpoints)
    exp30passiveCI = pd.DataFrame([get_locCI(exp30passive['50 deviation']), get_locCI(exp30passive['90 deviation']), get_locCI(exp30passive['130 deviation'])], index = interpoints)
    imp60passiveCI = pd.DataFrame([get_locCI(imp60passive['50 deviation']), get_locCI(imp60passive['90 deviation']), get_locCI(imp60passive['130 deviation'])], index = interpoints)
    exp60passiveCI = pd.DataFrame([get_locCI(exp60passive['50 deviation']), get_locCI(exp60passive['90 deviation']), get_locCI(exp60passive['130 deviation'])], index = interpoints)

    imp30predCI = pd.DataFrame([get_locCI(imp30active['50 deviation'] - imp30passive['50 deviation']), get_locCI(imp30active['90 deviation'] - imp30passive['90 deviation']), get_locCI(imp30active['130 deviation'] - imp30passive['130 deviation'])], index = interpoints)
    exp30predCI = pd.DataFrame([get_locCI(exp30active['50 deviation'] - exp30passive['50 deviation']), get_locCI(exp30active['90 deviation'] - exp30passive['90 deviation']), get_locCI(exp30active['130 deviation'] - exp30passive['130 deviation'])], index = interpoints)
    imp60predCI = pd.DataFrame([get_locCI(imp60active['50 deviation'] - imp60passive['50 deviation']), get_locCI(imp60active['90 deviation'] - imp60passive['90 deviation']), get_locCI(imp60active['130 deviation'] - imp60passive['130 deviation'])], index = interpoints)
    exp60predCI = pd.DataFrame([get_locCI(exp60active['50 deviation'] - exp60passive['50 deviation']), get_locCI(exp60active['90 deviation'] - exp60passive['90 deviation']), get_locCI(exp60active['130 deviation'] - exp60passive['130 deviation'])], index = interpoints)
#==============================================================================
#     activeGroup = [imp30active, exp30active, imp60active, exp60active]
#     passiveGroup = [imp30passive, exp30passive, imp60passive, exp60passive]
#     
#==============================================================================
    fig, (ax, ax2, ax3)  = plt.subplots(1, 3, sharey = True, facecolor = 'w', figsize = (6.5, 3))
        
    ax. axhline(y=0, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
    ax2. axhline(y=0, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
    ax3. axhline(y=0, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)

    #ACTIVE plot
    ax.plot(interpoints, imp30activeDevs, label = 'NI30', color = imp30col, linewidth = 2, linestyle = 'dashed')
    ax.plot(interpoints, exp30activeDevs, label = 'I30', color = exp30col, linewidth = 2)
    ax.plot(interpoints, imp60activeDevs, label = 'NI60', color = imp60col, linewidth = 2, linestyle = 'dashed')
    ax.plot(interpoints, exp60activeDevs, label = 'I60', color = exp60col, linewidth = 2)
    
    ax.fill_between(interpoints ,imp30activeCI[0] ,imp30activeCI[1], alpha = 0.2, color = imp30col, linewidth = 0.0)
    ax.fill_between(interpoints ,exp30activeCI[0] ,exp30activeCI[1], alpha = 0.2, color = exp30col, linewidth = 0.0)
    ax.fill_between(interpoints ,imp60activeCI[0] ,imp60activeCI[1], alpha = 0.2, color = imp60col, linewidth = 0.0)
    ax.fill_between(interpoints ,exp60activeCI[0] ,exp60activeCI[1], alpha = 0.2, color = exp60col, linewidth = 0.0)

    #PASSIVE plot
    ax2.plot(interpoints, imp30passiveDevs, label = 'NI30', color = imp30col, linewidth = 2, linestyle = 'dashed')
    ax2.plot(interpoints, exp30passiveDevs, label = 'I30', color = exp30col, linewidth = 2)
    ax2.plot(interpoints, imp60passiveDevs, label = 'NI60', color = imp60col, linewidth = 2, linestyle = 'dashed')
    ax2.plot(interpoints, exp60passiveDevs, label = 'I60', color = exp60col, linewidth = 2)
    
    ax2.fill_between(interpoints ,imp30passiveCI[0] ,imp30passiveCI[1], alpha = 0.2, color = imp30col, linewidth = 0.0)
    ax2.fill_between(interpoints ,exp30passiveCI[0] ,exp30passiveCI[1], alpha = 0.2, color = exp30col, linewidth = 0.0)
    ax2.fill_between(interpoints ,imp60passiveCI[0] ,imp60passiveCI[1], alpha = 0.2, color = imp60col, linewidth = 0.0)
    ax2.fill_between(interpoints ,exp60passiveCI[0] ,exp60passiveCI[1], alpha = 0.2, color = exp60col, linewidth = 0.0)

    
    #PREDICTED CONSEQUENCES plot
    ax3.plot(interpoints, imp30predDevs, label = 'NI30', color = imp30col, linewidth = 2, linestyle = 'dashed')
    ax3.plot(interpoints, exp30predDevs, label = 'I30', color = exp30col, linewidth = 2)
    ax3.plot(interpoints, imp60predDevs, label = 'NI60', color = imp60col, linewidth = 2, linestyle = 'dashed')
    ax3.plot(interpoints, exp60predDevs, label = 'I60', color = exp60col, linewidth = 2)

    ax3.fill_between(interpoints ,imp30predCI[0] ,imp30predCI[1], alpha = 0.2, color = imp30col, linewidth = 0.0)
    ax3.fill_between(interpoints ,exp30predCI[0] ,exp30predCI[1], alpha = 0.2, color = exp30col, linewidth = 0.0)
    ax3.fill_between(interpoints ,imp60predCI[0] ,imp60predCI[1], alpha = 0.2, color = imp60col, linewidth = 0.0)
    ax3.fill_between(interpoints ,exp60predCI[0] ,exp60predCI[1], alpha = 0.2, color = exp60col, linewidth = 0.0)

    #Plot means
    #ACTIVE plot
    ax.plot(161, np.nanmean(imp30activeDevs), color = imp30col, linewidth = 1, marker = '.')
    ax.plot(167, np.nanmean(exp30activeDevs), color = exp30col, linewidth = 1, marker = '.')
    ax.plot(173, np.nanmean(imp60activeDevs), color = imp60col, linewidth = 1, marker = '.')
    ax.plot(179, np.nanmean(exp60activeDevs), color = exp60col, linewidth = 1, marker = '.')
    
    ax.errorbar(x = 161 , y = np.nanmean(imp30activeDevs), yerr = np.nanmean(imp30activeCI[0]) -  np.nanmean(imp30activeDevs), alpha = 0.2, color = imp30col, linewidth = 2)
    ax.errorbar(x = 167 , y = np.nanmean(exp30activeDevs), yerr = np.nanmean(exp30activeCI[0]) -  np.nanmean(exp30activeDevs), alpha = 0.2, color = exp30col, linewidth = 2)
    ax.errorbar(x = 173 , y = np.nanmean(imp60activeDevs), yerr = np.nanmean(imp60activeCI[0]) -  np.nanmean(imp60activeDevs), alpha = 0.2, color = imp60col, linewidth = 2)
    ax.errorbar(x = 179 , y = np.nanmean(exp60activeDevs), yerr = np.nanmean(exp60activeCI[0]) -  np.nanmean(exp60activeDevs), alpha = 0.2, color = exp60col, linewidth = 2)
    
    #PASSIVE plot
    ax2.plot(161, np.nanmean(imp30passiveDevs), color = imp30col, linewidth = 1, marker = '.')
    ax2.plot(167, np.nanmean(exp30passiveDevs), color = exp30col, linewidth = 1, marker = '.')
    ax2.plot(173, np.nanmean(imp60passiveDevs), color = imp60col, linewidth = 1, marker = '.')
    ax2.plot(179, np.nanmean(exp60passiveDevs), color = exp60col, linewidth = 1, marker = '.')
    
    ax2.errorbar(x = 161 , y = np.nanmean(imp30passiveDevs), yerr = np.nanmean(imp30passiveCI[0]) -  np.nanmean(imp30passiveDevs), alpha = 0.2, color = imp30col, linewidth = 2)
    ax2.errorbar(x = 167 , y = np.nanmean(exp30passiveDevs), yerr = np.nanmean(exp30passiveCI[0]) -  np.nanmean(exp30passiveDevs), alpha = 0.2, color = exp30col, linewidth = 2)
    ax2.errorbar(x = 173 , y = np.nanmean(imp60passiveDevs), yerr = np.nanmean(imp60passiveCI[0]) -  np.nanmean(imp60passiveDevs), alpha = 0.2, color = imp60col, linewidth = 2)
    ax2.errorbar(x = 179 , y = np.nanmean(exp60passiveDevs), yerr = np.nanmean(exp60passiveCI[0]) -  np.nanmean(exp60passiveDevs), alpha = 0.2, color = exp60col, linewidth = 2)
    
    #PREDICTED CONSEQUENCES plot
    ax3.plot(161, np.nanmean(imp30predDevs), color = imp30col, linewidth = 0, marker = '.')
    ax3.plot(167, np.nanmean(exp30predDevs), color = exp30col, linewidth = 0, marker = '.')
    ax3.plot(173, np.nanmean(imp60predDevs), color = imp60col, linewidth = 0, marker = '.')
    ax3.plot(179, np.nanmean(exp60predDevs), color = exp60col, linewidth = 0, marker = '.')
    
    ax3.errorbar(x = 161 , y = np.nanmean(imp30predDevs), yerr = np.nanmean(imp30predCI[0]) -  np.nanmean(imp30predDevs), alpha = 0.2, color = imp30col, linewidth = 2)
    ax3.errorbar(x = 167 , y = np.nanmean(exp30predDevs), yerr = np.nanmean(exp30predCI[0]) -  np.nanmean(exp30predDevs), alpha = 0.2, color = exp30col, linewidth = 2)
    ax3.errorbar(x = 173 , y = np.nanmean(imp60predDevs), yerr = np.nanmean(imp60predCI[0]) -  np.nanmean(imp60predDevs), alpha = 0.2, color = imp60col, linewidth = 2)
    ax3.errorbar(x = 179 , y = np.nanmean(exp60predDevs), yerr = np.nanmean(exp60predCI[0]) -  np.nanmean(exp60predDevs), alpha = 0.2, color = exp60col, linewidth = 2)

#==============================================================================
#     #legend
#     legend = plt.legend(loc = 'upper right', fontsize = 38)
#     legend.get_frame().set_facecolor('none')
#     legend.get_frame().set_linewidth(0.0)
#     
#==============================================================================
    ax.set_title('Active\nLocalization')
    ax2.set_title('Passive\nLocalization')
    ax3.set_title('Predicted\nConsequences')
    
    #axes
    #axes labels (as texts)
    fig.text(0.5, 0.01,'Hand Angle (°)', ha = 'center')
    fig.text(0, 0.5,'Shift in Localization (°)', va = 'center', rotation = 'vertical')

    ax.set_xlim(30, 185)
    ax.set_ylim(10, -20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom') 
    ax.yaxis.set_ticks_position('left')
#    ax.xaxis.set_major_locator(ticker.MultipleLocator(45))
    
    ax2.set_xlim(30, 185)
    ax2.set_ylim(10, -20)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.xaxis.set_ticks_position('bottom') 
    ax2.yaxis.set_ticks_position('left')
#    ax2.xaxis.set_major_locator(ticker.MultipleLocator(45))

    
    ax3.set_xlim(30, 185)
    ax3.set_ylim(10, -20)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.xaxis.set_ticks_position('bottom') 
    ax3.yaxis.set_ticks_position('left')
#    ax3.xaxis.set_major_locator(ticker.MultipleLocator(45))

    plt.setp((ax, ax2, ax3), xticks=[50, 90, 130, 170], xticklabels=["50", "90", '130', 'mean'])
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1)
        ax2.spines[axis].set_linewidth(1)
        ax3.spines[axis].set_linewidth(1)

    ax.tick_params(axis='both', length= 4, width= 1)
    ax2.tick_params(axis='both', length= 4, width= 1)
    ax3.tick_params(axis='both', length= 4, width= 1)
    
    plt.tight_layout() #makes room for the x-axis label
    
    #save and show
    plt.savefig('localizations_per_pp.pdf', dpi = 100)
    plt.show()
    
    
#==============================================================================
#     for group in passiveGroup:
#         regress = kernelRegression( group.reachAngle , group.deviation , 30, interpoints)
#         _ = ax.plot(xRange, regress, label = 'Explicit 30', color = 'black', linewidth = 2)
# 
#     plt.show()
# 
#==============================================================================
#%%plot
threePointPlot()

