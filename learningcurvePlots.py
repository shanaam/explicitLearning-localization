import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import scipy.ndimage.filters
import scipy.stats as st
from decimal import Decimal


# os.chdir('c://Users/kineuser/Desktop/Shanaa/exp/explicit/data') #set the working directory AT SCHOOL PC
#os.chdir('E://Shanaa\'s Stuff/Documents/Shanaa/exp/explicit/data') #set the working directory AT HOME
os.chdir('D://shanaa/exp/explicit/data') #set the working directory ON LAPTOP

#make a df where each column is a participant with first 90 reaches (so it should have 90 rows, and angles should be baseline subtracted!)
#make a new script for this (preprocessing)

#%%
#set default font for pyplot
plt.rc('font',family='Calibri', size = 9)

#Set colours
exp60col = '#0500a0'
imp60col = '#037fc4'
exp30col = '#ff8000'
imp30col = '#e51636'

#import learning curve data (medians)
learningCurveDF60exp = pd.read_csv('exp60_curves.csv') 
learningCurveDF60imp = pd.read_csv('imp60_curves.csv')
learningCurveDF30exp = pd.read_csv('exp30_curves.csv') 
learningCurveDF30imp = pd.read_csv('imp30_curves.csv')

#get raw means
standard60e = learningCurveDF60exp.mean(axis = 1)
standard60i = learningCurveDF60imp.mean(axis = 1)
standard30e = learningCurveDF30exp.mean(axis = 1)
standard30i = learningCurveDF30imp.mean(axis = 1)
standard = list([standard60e, standard60i, standard30e, standard30i, 'standard'])

#gauss filtered data
filtered60e = scipy.ndimage.filters.gaussian_filter1d(standard60e, sigma=1)
filtered60i = scipy.ndimage.filters.gaussian_filter1d(standard60i, sigma=1)
filtered30e = scipy.ndimage.filters.gaussian_filter1d(standard30e, sigma=1)
filtered30i = scipy.ndimage.filters.gaussian_filter1d(standard30i, sigma=1)
filtered = list([filtered60e, filtered60i, filtered30e, filtered30i, 'filtered'])

# get normalized means (dependancy = get raw means)
normStandard60e = standard60e/60
normStandard60i = standard60i/60
normStandard30e = standard30e/30
normStandard30i = standard30i/30
normStandard = list([normStandard60e, normStandard60i, normStandard30e, normStandard30i, 'normStandard'])

#gauss filtered data normalized
normFiltered60e = scipy.ndimage.filters.gaussian_filter1d(normStandard60e, sigma=1)
normFiltered60i = scipy.ndimage.filters.gaussian_filter1d(normStandard60i, sigma=1)
normFiltered30e = scipy.ndimage.filters.gaussian_filter1d(normStandard30e, sigma=1)
normFiltered30i = scipy.ndimage.filters.gaussian_filter1d(normStandard30i, sigma=1)
normFiltered =list([normFiltered60e, normFiltered60i, normFiltered30e, normFiltered30i, 'normFiltered'])

#%%
#function to calculate confidence intervals (with NaN removal)
def get_nanCI(groupDF):
    participantNum = len(groupDF.T)
    xNum = len(groupDF)
    test = np.array(groupDF.iloc[:, 0:participantNum])
    myList = list()
    for x in np.arange(xNum):
        myList.append(list(test[x][~np.isnan(test[x])]))
    
    
    CIList = list()
    for x in np.arange(xNum):
        CIList.append(st.t.interval(0.95, len(myList[x])-1, loc=np.mean(myList[x]), scale=st.sem(myList[x])))
    
    return np.array(CIList).T

#add CI columns
learningCurveDF60exp['lowerCI'] = get_nanCI(learningCurveDF60exp)[0]
learningCurveDF60exp['upperCI'] = get_nanCI(learningCurveDF60exp)[1]
learningCurveDF60imp['lowerCI'] = get_nanCI(learningCurveDF60imp)[0]
learningCurveDF60imp['upperCI'] = get_nanCI(learningCurveDF60imp)[1]
learningCurveDF30exp['lowerCI'] = get_nanCI(learningCurveDF30exp)[0]
learningCurveDF30exp['upperCI'] = get_nanCI(learningCurveDF30exp)[1]
learningCurveDF30imp['lowerCI'] = get_nanCI(learningCurveDF30imp)[0]
learningCurveDF30imp['upperCI'] = get_nanCI(learningCurveDF30imp)[1]

#standard data CIs
standard60eLowerCI = learningCurveDF60exp['lowerCI']
standard60eUpperCI = learningCurveDF60exp['upperCI']
standard60iLowerCI = learningCurveDF60imp['lowerCI']
standard60iUpperCI = learningCurveDF60imp['upperCI']
standard30eLowerCI = learningCurveDF30exp['lowerCI']
standard30eUpperCI = learningCurveDF30exp['upperCI']
standard30iLowerCI = learningCurveDF30imp['lowerCI']
standard30iUpperCI = learningCurveDF30imp['upperCI']
standardCI = list([standard60eLowerCI, standard60eUpperCI, standard60iLowerCI, standard60iUpperCI, standard30eLowerCI, standard30eUpperCI, standard30iLowerCI, standard30iUpperCI])

#gauss filtered data
filtered60eLowerCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF60exp['lowerCI'], sigma=1)
filtered60eUpperCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF60exp['upperCI'], sigma=1)
filtered60iLowerCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF60imp['lowerCI'], sigma=1)
filtered60iUpperCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF60imp['upperCI'], sigma=1)
filtered30eLowerCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF30exp['lowerCI'], sigma=1)
filtered30eUpperCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF30exp['upperCI'], sigma=1)
filtered30iLowerCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF30imp['lowerCI'], sigma=1)
filtered30iUpperCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF30imp['upperCI'], sigma=1)
filteredCI = list([filtered60eLowerCI, filtered60eUpperCI, filtered60iLowerCI, filtered60iUpperCI, filtered30eLowerCI, filtered30eUpperCI, filtered30iLowerCI, filtered30iUpperCI])

#normalized data
normStandard60eLowerCI = learningCurveDF60exp['lowerCI']/60
normStandard60eUpperCI = learningCurveDF60exp['upperCI']/60
normStandard60iLowerCI = learningCurveDF60imp['lowerCI']/60
normStandard60iUpperCI = learningCurveDF60imp['upperCI']/60
normStandard30eLowerCI = learningCurveDF30exp['lowerCI']/30
normStandard30eUpperCI = learningCurveDF30exp['upperCI']/30
normStandard30iLowerCI = learningCurveDF30imp['lowerCI']/30
normStandard30iUpperCI = learningCurveDF30imp['upperCI']/30
normStandardCI = list([normStandard60eLowerCI, normStandard60eUpperCI, normStandard60iLowerCI, normStandard60iUpperCI, normStandard30eLowerCI, normStandard30eUpperCI, normStandard30iLowerCI, normStandard30iUpperCI])

#gauss filtered data
normFiltered60eLowerCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF60exp['lowerCI']/60, sigma=1)
normFiltered60eUpperCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF60exp['upperCI']/60, sigma=1)
normFiltered60iLowerCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF60imp['lowerCI']/60, sigma=1)
normFiltered60iUpperCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF60imp['upperCI']/60, sigma=1)
normFiltered30eLowerCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF30exp['lowerCI']/30, sigma=1)
normFiltered30eUpperCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF30exp['upperCI']/30, sigma=1)
normFiltered30iLowerCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF30imp['lowerCI']/30, sigma=1)
normFiltered30iUpperCI = scipy.ndimage.filters.gaussian_filter1d(learningCurveDF30imp['upperCI']/30, sigma=1)
normFilteredCI = list([normFiltered60eLowerCI, normFiltered60eUpperCI, normFiltered60iLowerCI, normFiltered60iUpperCI, normFiltered30eLowerCI, normFiltered30eUpperCI, normFiltered30iLowerCI, normFiltered30iUpperCI])


#%% plot learning curve function
def plotLC(x):
    
    fig, ax = plt.subplots() #look this up later..
    figure = plt.gcf()
    figure.set_size_inches(2, 3)
    
    plt.plot(x[0], label = 'Explicit60', color = exp60col, linewidth = 2)
    plt.plot(x[1], label = 'Implicit60', color = imp60col, linestyle = '--', linewidth = 2)
    plt.plot(x[2], label = 'Explicit30', color = exp30col, linewidth = 2)
    plt.plot(x[3], label = 'Implicit30', color = imp30col, linestyle = '--', linewidth = 2)
    
#==============================================================================
#     #legend
#     legend = plt.legend(loc = 'lower right', fontsize =9)
#     legend.get_frame().set_facecolor('none')
#     legend.get_frame().set_linewidth(0.0)
#     
#==============================================================================
    
    #axes
    plt.xlabel('Trials')
    plt.ylabel('Angular Deviation (°)')
    
    ax.set_xlim(-2, 90)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom') 
    ax.yaxis.set_ticks_position('left') 
    
    #show
    plt.show()
    
#Break in plot
def plotBrokenLC(x, ci):
    
    xRange = np.arange(1,22)
    xRangePlot2 = np.arange(70,91)
    fig, (ax, ax2)  = plt.subplots(1, 2, sharey = True, facecolor = 'w', figsize = (2.5, 3)) #look this up later..
#    figure = plt.gcf()
    # figure.set_size_inches(3.75, 2.75)
    #Shaded area blocked    
    ax.fill_between(np.arange(0.5, 6.6), -10, 70, color = '#eeeeee', linewidth = 0.0, zorder = -10)
#    ax.fill_between(np.arange(3.5,6.6), -10, 70, color = '#eeeeee', linewidth = 0.0)
    ax.axvline(x=3.5, ymin= -10 , ymax=70, color = 'white', linestyle = 'dashed', linewidth = 1, zorder = -5)
    ax2.fill_between(np.arange(80.5, 91), -10, 70, color = '#eeeeee', linewidth = 0.0, zorder = -10)

    
    ax. axhline(y=0, xmin= 0 , xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1, zorder = -5)
    ax2. axhline(y=0, xmin= 0 , xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1, zorder = -5)
    if x[-1] == 'normStandard':       
        ax. axhline(y=1, xmin= 0 , xmax=1, color = '#bababa', linestyle = 'dashed', linewidth = 1, zorder = -5)
        ax2. axhline(y=1, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1, zorder = -5)
    elif x[-1] == 'standard':
        ax. axhline(y=30, xmin= 0 , xmax=1, color = '#bababa', linestyle = 'dashed', linewidth = 1, zorder = -5)
        ax2. axhline(y=30, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1, zorder = -5)
        ax. axhline(y=60, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1, zorder = -5)
        ax2. axhline(y=60, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1, zorder = -5)
    
    ax.plot(xRange, x[0][xRange[0]-1 : xRange[-1]], label = 'I60', color = exp60col, linewidth = 2)
    ax.plot(xRange, x[1][xRange[0]-1 : xRange[-1]], label = 'NI60', color = imp60col, linewidth = 2, linestyle = 'dashed')
    ax.plot(xRange, x[2][xRange[0]-1 : xRange[-1]], label = 'I30', color = exp30col, linewidth = 2)
    ax.plot(xRange, x[3][xRange[0]-1 : xRange[-1]], label = 'NI30', color = imp30col, linewidth = 2, linestyle = 'dashed')
    
    ax2.plot(xRangePlot2, x[0][xRangePlot2[0]-1 : xRangePlot2[-1]], label = 'I60', color = exp60col, linewidth = 2)
    ax2.plot(xRangePlot2, x[1][xRangePlot2[0]-1 : xRangePlot2[-1]], label = 'NI60', color = imp60col, linewidth = 2, linestyle = 'dashed')
    ax2.plot(xRangePlot2, x[2][xRangePlot2[0]-1 : xRangePlot2[-1]], label = 'I30', color = exp30col, linewidth = 2)
    ax2.plot(xRangePlot2, x[3][xRangePlot2[0]-1 : xRangePlot2[-1]], label = 'NI30', color = imp30col, linewidth = 2, linestyle = 'dashed')

    ax.fill_between(xRange, ci[0][xRange[0]-1 : xRange[-1]], ci[1][xRange[0]-1 : xRange[-1]], alpha = 0.2, color = exp60col, linewidth = 0.0)
    ax.fill_between(xRange, ci[2][xRange[0]-1 : xRange[-1]], ci[3][xRange[0]-1 : xRange[-1]], alpha = 0.2, color = imp60col, linewidth = 0.0)
    ax.fill_between(xRange, ci[4][xRange[0]-1 : xRange[-1]], ci[5][xRange[0]-1 : xRange[-1]], alpha = 0.2, color = exp30col, linewidth = 0.0)
    ax.fill_between(xRange, ci[6][xRange[0]-1 : xRange[-1]], ci[7][xRange[0]-1 : xRange[-1]], alpha = 0.2, color = imp30col, linewidth = 0.0)
    ax2.fill_between(xRangePlot2, ci[0][xRangePlot2[0]-1 : xRangePlot2[-1]], ci[1][xRangePlot2[0]-1 : xRangePlot2[-1]], alpha = 0.2, color = exp60col, linewidth = 0.0)
    ax2.fill_between(xRangePlot2, ci[2][xRangePlot2[0]-1 : xRangePlot2[-1]], ci[3][xRangePlot2[0]-1 : xRangePlot2[-1]], alpha = 0.2, color = imp60col, linewidth = 0.0)
    ax2.fill_between(xRangePlot2, ci[4][xRangePlot2[0]-1 : xRangePlot2[-1]], ci[5][xRangePlot2[0]-1 : xRangePlot2[-1]], alpha = 0.2, color = exp30col, linewidth = 0.0)
    ax2.fill_between(xRangePlot2, ci[6][xRangePlot2[0]-1 : xRangePlot2[-1]], ci[7][xRangePlot2[0]-1 : xRangePlot2[-1]], alpha = 0.2, color = imp30col, linewidth = 0.0)

#    #legend
#    legend = plt.legend(loc = 'lower right', fontsize = 9)
#    legend.get_frame().set_facecolor('none')
#    legend.get_frame().set_linewidth(0.0)
    
    #axes labels (as texts)
    fig.text(0.5, .01,'Trials', ha = 'center')
    if x[-1] == 'standard':
        fig.text(0.01, 0.5,'Angular Deviation (°)', va = 'center', rotation = 'vertical')
    elif x[-1] == 'normStandard':
        fig.text(0.01, 0.5,'Normalized Angular Deviation', va = 'center', rotation = 'vertical')
        
    #axes
    ax.set_xlim(xRange[0]-2,xRange[-1])
    ax2.set_xlim(xRangePlot2[0]-1,xRangePlot2[-1])

    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    # ax.yaxis.tick_left()
    # ax.tick_params(labelright='off')
    # ax2.yaxis.tick_right()
    ax.xaxis.set_ticks_position('bottom') 
    ax.yaxis.set_ticks_position('left') 
    ax2.xaxis.set_ticks_position('bottom') 
    ax2.yaxis.set_tick_params(size=0) #gets rid of tick lines on second plot
    
    ax.set_xticks([1, 5, 10, 15, 20])
    ax2.set_xticks([70, 75, 80, 85, 90])
    if x[-1] == 'normStandard':
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1)
        ax2.spines[axis].set_linewidth(1)
    ax.tick_params(axis='both', length= 4, width= 1)
    ax2.tick_params(axis='x', length= 4, width= 1)

    plt.tight_layout() #makes room for the x-axis label
    if x[-1] == 'normStandard':
        ax.set_ylim(-0.2, 1.2, auto = False)
        ax2.set_ylim(-0.2, 1.2, auto = False)
    elif x[-1] == 'standard':
        ax.set_ylim(-10, 70)
        ax2.set_ylim(-10, 70)

    #save figure show
    plt.savefig(x[-1] + 'learningCurves.pdf', dpi = 100)
    plt.show()
    

#%% plot some things
# plotLC(standard)
# plotLC(filtered)
# plotLC(normStandard)
# plotLC(normFiltered)

plotBrokenLC(standard, standardCI)
# plotBrokenLC(filtered, filteredCI)
plotBrokenLC(normStandard, normStandardCI)
#plotBrokenLC(normFiltered, normFilteredCI)
 
 
# x = standard
# ci = standardCI
#%%
#for blocking data (trials must be vertical)
class trainingDF: 
    #class variable (same for all instances of this class)
    block1a, block1b = 0, 2 #start and end points for block 1
    block2a, block2b = 3, 5
    blockF = 9 #Just the number of trials MAKE SURE THIS matches 'AOVdata' in preprocessing
    
    def __init__(self, df, rotSize):
        self.df = df
        self.rotSize = rotSize
        self.normalized = "only do math on the angle columns (divide by rotSize" #wtf is this??        
        
        self.block1 = self.df[self.block1a : self.block1b +1].mean(0)
        self.block2 = self.df[self.block2a : self.block2b +1].mean(0)
        self.finalBlock = self.df.tail(self.blockF).mean(0)
        
        self.block1AOV = ([item for sublist in np.array(self.df[self.block1a:self.block1b +1]) for item in sublist])
        
        self.normBlock1 = self.block1 / rotSize
        self.normBlock2 = self.block2 / rotSize
        self.normFinalBlock = self.finalBlock / rotSize
        
    def means(self):
        print('block 1 mean = {}'.format(np.nanmean(self.block1)))
        print('block 2 mean = {}'.format(np.nanmean(self.block2)))
        print('Final block mean = {}'.format(np.nanmean(self.finalBlock)))
        print('NORMALIZED block 1 mean = {}'.format(np.nanmean(self.normBlock1)))
        print('NORMALIZED block 2 mean = {}'.format(np.nanmean(self.normBlock2)))
        print('NORMALIZED Final block mean = {}'.format(np.nanmean(self.normFinalBlock)))

    def meanAtTrial(self, trialNum):
        print('mean at trial {} = {}'.format(trialNum, np.nanmean(self.df.iloc[trialNum -1])))
        print('mean at trial {} when NORMALIZED = {}'.format(trialNum, np.nanmean(self.df.iloc[trialNum -1] / self.rotSize)))
        
    def withinGroupTTests(self):
        if self.blockF == self.block2b-self.block2a + 1: 
            print("\nblock 1v2: p-value = " + str(Decimal(str(st.ttest_rel(self.block1, self.block2, nan_policy= 'omit')[1])).quantize(Decimal('.0001'))))
            print("block 2vFinal: p-value = " + str(Decimal(str(st.ttest_rel(self.block2, self.finalBlock, nan_policy= 'omit')[1])).quantize(Decimal('.0001'))))
            print("block 1vFinal: p-value = " + str(Decimal(str(st.ttest_rel(self.block1, self.finalBlock, nan_policy= 'omit')[1])).quantize(Decimal('.0001'))))
            #print("Normalized block 1v2: p-value = " + str(Decimal(str(stats.ttest_rel(self.normBlock1, self.normBlock2, nan_policy= 'omit')[1])).quantize(Decimal('.0001'))))
            #print("Normalized block 2vFinal: p-value = " + str(Decimal(str(stats.ttest_rel(self.normBlock2, self.normFinalBlock, nan_policy= 'omit')[1])).quantize(Decimal('.0001'))))
            #normalized groups give the same p-value
        else:
            return

#==============================================================================
# class afterEffectsDF:
#     def __init__(self, df, rotSize):
#         self.df = df
#         self.rotSize = rotSize
#         normColumn = df.angularDevs / rotSize
#         self.normalized = pd.DataFrame([normColumn, df.trialNum, df.instruction, df.participant], ['angularDevs', 'trialNum', 'instruction', 'participant']).T
#         
#         self.withStrat = df[df.instruction == 'with'] 
#         self.withoutStrat = df[df.instruction == 'without']
# 
#         self.normWithStrat = self.normalized[self.normalized.instruction == 'with'] 
#         self.normWithoutStrat = self.normalized[self.normalized.instruction == 'without']
# 
#==============================================================================

class afterEffectsDF_pp:
    def __init__(self, df, rotSize):
        self.df = df
        self.rotSize = rotSize
        normInclusive = df.inclusive / rotSize
        normExclusive = df.exclusive / rotSize

        self.normalized = pd.DataFrame([df.participant, normExclusive, normInclusive], ['participant', 'exclusive', 'inclusive']).T
        
        self.withStrat = df.inclusive
        self.withoutStrat = df.exclusive
        self.explicitComp = df.inclusive - df.exclusive
        
        self.ratio = df.awarenessRatio

        self.normWithStrat = self.normalized.inclusive
        self.normWithoutStrat = self.normalized.exclusive
        
class TapDF:
    def __init__(self, passive_df, active_df, rotSize):
        self.prop_df = passive_df #SHIFTS proprioceptive estimates
        self.active_df = active_df
        
        pred_dfTemp = pd.DataFrame()
        pred_dfTemp['50 deviation'] = active_df['50 deviation'] - passive_df['50 deviation']
        pred_dfTemp['90 deviation'] = active_df['90 deviation'] - passive_df['90 deviation']
        pred_dfTemp['130 deviation'] = active_df['130 deviation'] - passive_df['130 deviation']
        pred_dfTemp['type'] = active_df['type']
        pred_dfTemp['participant'] = active_df['participant']   
        self.pred_df = pred_dfTemp #SHIFTS predicted consequences
        
        prop_meanTemp = pd.DataFrame()
        prop_meanTemp['meanDeviations']= passive_df[['50 deviation', '90 deviation', '130 deviation']].mean(1)
        prop_meanTemp['type'] = passive_df['type']
        prop_meanTemp['participant'] = passive_df['participant']
        self.prop_means = prop_meanTemp 
 
        pred_meanTemp = pd.DataFrame()
        pred_meanTemp['meanDeviations']= self.pred_df[['50 deviation', '90 deviation', '130 deviation']].mean(1)
        pred_meanTemp['type'] = self.pred_df['type']
        pred_meanTemp['participant'] = self.pred_df['participant']
        self.pred_means = pred_meanTemp 
        
        self.rotSize = rotSize
      

def flattenList(data):
    return [item for sublist in data for item in sublist]

def cohen_d(x,y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(((nx-1)*np.std(x, ddof=1) ** 2 + (ny-1)*np.std(y, ddof=1) ** 2) / dof)

#%% make instances of my DF classes using reach data
        
imp30curves = trainingDF(pd.read_csv('imp30_curves.csv'), 30)
exp30curves = trainingDF(pd.read_csv('exp30_curves.csv'), 30)
imp60curves = trainingDF(pd.read_csv('imp60_curves.csv'), 60)
exp60curves = trainingDF(pd.read_csv('exp60_curves.csv'), 60)

#==============================================================================
# imp30ae = afterEffectsDF(pd.read_csv('imp30_reachAEs.csv'), 30)
# exp30ae = afterEffectsDF(pd.read_csv('exp30_reachAEs.csv'), 30)
# imp60ae = afterEffectsDF(pd.read_csv('imp60_reachAEs.csv'), 60)
# exp60ae = afterEffectsDF(pd.read_csv('exp60_reachAEs.csv'), 60)
#==============================================================================

imp30ae_pp = afterEffectsDF_pp(pd.read_csv('imp30_reachAEs_pp.csv'), 30)
exp30ae_pp = afterEffectsDF_pp(pd.read_csv('exp30_reachAEs_pp.csv'), 30)
imp60ae_pp = afterEffectsDF_pp(pd.read_csv('imp60_reachAEs_pp.csv'), 60)
exp60ae_pp = afterEffectsDF_pp(pd.read_csv('exp60_reachAEs_pp.csv'), 60)
#==============================================================================
# impAgae_pp = afterEffectsDF_pp(pd.read_csv('impAg_reachAEs_pp.csv'), 60)
# expAgae_pp = afterEffectsDF_pp(pd.read_csv('expAg_reachAEs_pp.csv'), 60)
# 
#==============================================================================

imp30tap = TapDF(pd.read_csv('imp30_passiveTapData.csv'), pd.read_csv('imp30_activeTapData.csv'), 30)
exp30tap = TapDF(pd.read_csv('exp30_passiveTapData.csv'), pd.read_csv('exp30_activeTapData.csv'), 30)
imp60tap = TapDF(pd.read_csv('imp60_passiveTapData.csv'), pd.read_csv('imp60_activeTapData.csv'), 60)
exp60tap = TapDF(pd.read_csv('exp60_passiveTapData.csv'), pd.read_csv('exp60_activeTapData.csv'), 60)

#%%extra plots
#set default font for pyplot
plt.rc('font',family='Calibri', size = 9)

def get_nanCI(groupDF):
    participantNum = len(groupDF.T)
    xNum = len(groupDF)
    test = np.array(groupDF.iloc[:, 0:participantNum])
    myList = list()
    for x in np.arange(xNum):
        myList.append(list(test[x][~np.isnan(test[x])]))
    
    CIList = list()
    for x in np.arange(xNum):
        CIList.append(st.t.interval(0.95, len(myList[x])-1, loc=np.mean(myList[x]), scale=st.sem(myList[x])))
    
    return np.array(CIList).T

def get_CI(data):
    participantNum = len(data)
    return np.array (st.t.interval(0.95, participantNum-1, loc=np.nanmean(data), scale=st.sem(data, nan_policy='omit')))

def plotLCmeans(x = 'standard'):
    #Set colours
    exp60col = '#0500a0'
    imp60col = '#037fc4'
    exp30col = '#ff8000'
    imp30col = '#e51636'
    
    fig, (ax, ax2)  = plt.subplots(1, 2, sharey = True, facecolor = 'w', figsize = (2.5, 3))
        
    ax. axhline(y=0, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
    ax2. axhline(y=0, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)  
    
    ax.plot(7, np.nanmean(imp30curves.block1), color = imp30col, linewidth = 1, marker = '.')
    ax.plot(9, np.nanmean(exp30curves.block1), color = exp30col, linewidth = 1, marker = '.')
    ax.plot(11, np.nanmean(imp60curves.block1), color = imp60col, linewidth = 1, marker = '.')
    ax.plot(13, np.nanmean(exp60curves.block1), color = exp60col, linewidth = 1, marker = '.')
    
    ax.plot(27, np.nanmean(imp30curves.block2), color = imp30col, linewidth = 1, marker = '.')
    ax.plot(29, np.nanmean(exp30curves.block2), color = exp30col, linewidth = 1, marker = '.')
    ax.plot(31, np.nanmean(imp60curves.block2), color = imp60col, linewidth = 1, marker = '.')
    ax.plot(33, np.nanmean(exp60curves.block2), color = exp60col, linewidth = 1, marker = '.')
    
    ax2.plot(47, np.nanmean(imp30curves.finalBlock), color = imp30col, linewidth = 1, marker = '.')
    ax2.plot(49, np.nanmean(exp30curves.finalBlock), color = exp30col, linewidth = 1, marker = '.')
    ax2.plot(51, np.nanmean(imp60curves.finalBlock), color = imp60col, linewidth = 1, marker = '.')
    ax2.plot(53, np.nanmean(exp60curves.finalBlock), color = exp60col, linewidth = 1, marker = '.')
    
    ax.errorbar(x = 7 , y = np.nanmean(imp30curves.block1), yerr = get_CI(imp30curves.block1)[1] - np.nanmean(imp30curves.block1), alpha = 0.2, color = imp30col, linewidth = 2)
    ax.errorbar(x = 9 , y = np.nanmean(exp30curves.block1), yerr = get_CI(exp30curves.block1)[1] - np.nanmean(exp30curves.block1), alpha = 0.2, color = exp30col, linewidth = 2)
    ax.errorbar(x = 11 , y = np.nanmean(imp60curves.block1), yerr = get_CI(imp60curves.block1)[1] - np.nanmean(imp60curves.block1), alpha = 0.2, color = imp60col, linewidth = 2)
    ax.errorbar(x = 13 , y = np.nanmean(exp60curves.block1), yerr = get_CI(exp60curves.block1)[1] - np.nanmean(exp60curves.block1), alpha = 0.2, color = exp60col, linewidth = 2)

    ax.errorbar(x = 27 , y = np.nanmean(imp30curves.block2), yerr = get_CI(imp30curves.block2)[1] - np.nanmean(imp30curves.block2), alpha = 0.2, color = imp30col, linewidth = 2)
    ax.errorbar(x = 29 , y = np.nanmean(exp30curves.block2), yerr = get_CI(exp30curves.block2)[1] - np.nanmean(exp30curves.block2), alpha = 0.2, color = exp30col, linewidth = 2)
    ax.errorbar(x = 31 , y = np.nanmean(imp60curves.block2), yerr = get_CI(imp60curves.block2)[1] - np.nanmean(imp60curves.block2), alpha = 0.2, color = imp60col, linewidth = 2)
    ax.errorbar(x = 33 , y = np.nanmean(exp60curves.block2), yerr = get_CI(exp60curves.block2)[1] - np.nanmean(exp60curves.block2), alpha = 0.2, color = exp60col, linewidth = 2)

    ax2.errorbar(x = 47 , y = np.nanmean(imp30curves.finalBlock), yerr = get_CI(imp30curves.finalBlock)[1] - np.nanmean(imp30curves.finalBlock), alpha = 0.2, color = imp30col, linewidth = 2)
    ax2.errorbar(x = 49 , y = np.nanmean(exp30curves.finalBlock), yerr = get_CI(exp30curves.finalBlock)[1] - np.nanmean(exp30curves.finalBlock), alpha = 0.2, color = exp30col, linewidth = 2)
    ax2.errorbar(x = 51 , y = np.nanmean(imp60curves.finalBlock), yerr = get_CI(imp60curves.finalBlock)[1] - np.nanmean(imp60curves.finalBlock), alpha = 0.2, color = imp60col, linewidth = 2)
    ax2.errorbar(x = 53 , y = np.nanmean(exp60curves.finalBlock), yerr = get_CI(exp60curves.finalBlock)[1] - np.nanmean(exp60curves.finalBlock), alpha = 0.2, color = exp60col, linewidth = 2)


    #axes labels (as texts)
    fig.text(0.5, .01,'Block', ha = 'center')
    if x == 'standard':
        fig.text(0.01, 0.5,'Angular Deviation (°)', va = 'center', rotation = 'vertical')
        
        ax. axhline(y=60, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
        ax2. axhline(y=60, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1) 
        ax. axhline(y=30, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
        ax2. axhline(y=30, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)  
    
    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    # ax.yaxis.tick_left()
    # ax.tick_params(labelright='off')
    # ax2.yaxis.tick_right()
    ax.xaxis.set_ticks_position('bottom') 
    ax.yaxis.set_ticks_position('left') 
    ax2.xaxis.set_ticks_position('bottom') 
    ax2.yaxis.set_tick_params(size=0) #gets rid of tick lines on second plot
    
    plt.setp((ax), xticks=[10,30], xticklabels=['1', '2'])
    plt.setp((ax2), xticks=[50], xticklabels=['Final'])

    if x == 'normStandard':
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1)
        ax2.spines[axis].set_linewidth(1)
    ax.tick_params(axis='both', length= 4, width= 1)
    ax2.tick_params(axis='x', length= 4, width= 1)

    plt.tight_layout() #makes room for the x-axis label
        #axes
    ax.set_xlim(0,40) #ranges
    ax2.set_xlim(40,60)
    if x == 'normStandard':
        ax.set_ylim(-0.2, 1.2, auto = False)
        ax2.set_ylim(-0.2, 1.2, auto = False)
    elif x == 'standard':
        ax.set_ylim(-10, 70)
        ax2.set_ylim(-10, 70)

    #save figure show
    plt.savefig('blockedLearning.pdf', dpi = 100, transparency = True)
    plt.show()
    
def plotNormLCmeans(x = 'normStandard'):
    #Set colours
    exp60col = '#0500a0'
    imp60col = '#037fc4'
    exp30col = '#ff8000'
    imp30col = '#e51636'
    
    fig, (ax, ax2)  = plt.subplots(1, 2, sharey = True, facecolor = 'w', figsize = (2.5, 3))
        
    ax. axhline(y=0, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
    ax2. axhline(y=0, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)  
    
    ax.plot([7, 27], [np.nanmean(imp30curves.normBlock1), np.nanmean(imp30curves.normBlock2)], color = imp30col, linewidth = 1, marker = '.', linestyle = 'dashed')
    ax.plot([9, 29], [np.nanmean(exp30curves.normBlock1), np.nanmean(exp30curves.normBlock2)], color = exp30col, linewidth = 1, marker = '.', linestyle = 'dashed')
    ax.plot([11, 31], [np.nanmean(imp60curves.normBlock1), np.nanmean(imp60curves.normBlock2)], color = imp60col, linewidth = 1, marker = '.', linestyle = 'dashed')
    ax.plot([13, 33], [np.nanmean(exp60curves.normBlock1), np.nanmean(exp60curves.normBlock2)], color = exp60col, linewidth = 1, marker = '.', linestyle = 'dashed')
        
    ax2.plot(47, np.nanmean(imp30curves.normFinalBlock), color = imp30col, linewidth = 1, marker = '.')
    ax2.plot(49, np.nanmean(exp30curves.normFinalBlock), color = exp30col, linewidth = 1, marker = '.')
    ax2.plot(51, np.nanmean(imp60curves.normFinalBlock), color = imp60col, linewidth = 1, marker = '.')
    ax2.plot(53, np.nanmean(exp60curves.normFinalBlock), color = exp60col, linewidth = 1, marker = '.')
    
    ax.errorbar(x = 7 , y = np.nanmean(imp30curves.normBlock1), yerr = get_CI(imp30curves.normBlock1)[1] - np.nanmean(imp30curves.normBlock1), alpha = 0.2, color = imp30col, linewidth = 2)
    ax.errorbar(x = 9 , y = np.nanmean(exp30curves.normBlock1), yerr = get_CI(exp30curves.normBlock1)[1] - np.nanmean(exp30curves.normBlock1), alpha = 0.2, color = exp30col, linewidth = 2)
    ax.errorbar(x = 11 , y = np.nanmean(imp60curves.normBlock1), yerr = get_CI(imp60curves.normBlock1)[1] - np.nanmean(imp60curves.normBlock1), alpha = 0.2, color = imp60col, linewidth = 2)
    ax.errorbar(x = 13 , y = np.nanmean(exp60curves.normBlock1), yerr = get_CI(exp60curves.normBlock1)[1] - np.nanmean(exp60curves.normBlock1), alpha = 0.2, color = exp60col, linewidth = 2)

    ax.errorbar(x = 27 , y = np.nanmean(imp30curves.normBlock2), yerr = get_CI(imp30curves.normBlock2)[1] - np.nanmean(imp30curves.normBlock2), alpha = 0.2, color = imp30col, linewidth = 2)
    ax.errorbar(x = 29 , y = np.nanmean(exp30curves.normBlock2), yerr = get_CI(exp30curves.normBlock2)[1] - np.nanmean(exp30curves.normBlock2), alpha = 0.2, color = exp30col, linewidth = 2)
    ax.errorbar(x = 31 , y = np.nanmean(imp60curves.normBlock2), yerr = get_CI(imp60curves.normBlock2)[1] - np.nanmean(imp60curves.normBlock2), alpha = 0.2, color = imp60col, linewidth = 2)
    ax.errorbar(x = 33 , y = np.nanmean(exp60curves.normBlock2), yerr = get_CI(exp60curves.normBlock2)[1] - np.nanmean(exp60curves.normBlock2), alpha = 0.2, color = exp60col, linewidth = 2)

    ax2.errorbar(x = 47 , y = np.nanmean(imp30curves.normFinalBlock), yerr = get_CI(imp30curves.normFinalBlock)[1] - np.nanmean(imp30curves.normFinalBlock), alpha = 0.2, color = imp30col, linewidth = 2)
    ax2.errorbar(x = 49 , y = np.nanmean(exp30curves.normFinalBlock), yerr = get_CI(exp30curves.normFinalBlock)[1] - np.nanmean(exp30curves.normFinalBlock), alpha = 0.2, color = exp30col, linewidth = 2)
    ax2.errorbar(x = 51 , y = np.nanmean(imp60curves.normFinalBlock), yerr = get_CI(imp60curves.normFinalBlock)[1] - np.nanmean(imp60curves.normFinalBlock), alpha = 0.2, color = imp60col, linewidth = 2)
    ax2.errorbar(x = 53 , y = np.nanmean(exp60curves.normFinalBlock), yerr = get_CI(exp60curves.normFinalBlock)[1] - np.nanmean(exp60curves.normFinalBlock), alpha = 0.2, color = exp60col, linewidth = 2)


    #axes labels (as texts)
    fig.text(0.5, .01,'Block', ha = 'center')
    if x == 'standard':
        fig.text(0.01, 0.5,'Angular Deviation (°)', va = 'center', rotation = 'vertical')
        
        ax. axhline(y=60, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
        ax2. axhline(y=60, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1) 
        ax. axhline(y=30, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
        ax2. axhline(y=30, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
    elif x =='normStandard':
        ax. axhline(y=1, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
        ax2. axhline(y=1, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1) 

    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    # ax.yaxis.tick_left()
    # ax.tick_params(labelright='off')
    # ax2.yaxis.tick_right()
    ax.xaxis.set_ticks_position('bottom') 
    ax.yaxis.set_ticks_position('left') 
    ax2.xaxis.set_ticks_position('bottom') 
    ax2.yaxis.set_tick_params(size=0) #gets rid of tick lines on second plot
    
    plt.setp((ax), xticks=[10,30], xticklabels=['1', '2'])
    plt.setp((ax2), xticks=[50], xticklabels=['Final'])

    if x == 'normStandard':
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1)
        ax2.spines[axis].set_linewidth(1)
    ax.tick_params(axis='both', length= 4, width= 1)
    ax2.tick_params(axis='x', length= 4, width= 1)

    plt.tight_layout() #makes room for the x-axis label
    
    #axes
    ax.set_xlim(0,40) #ranges
    ax2.set_xlim(40,60)
    if x == 'normStandard':
        ax.set_ylim(-0.2, 1.2, auto = False)
        ax2.set_ylim(-0.2, 1.2, auto = False)
    elif x == 'standard':
        ax.set_ylim(-10, 70)
        ax2.set_ylim(-10, 70)

    #save figure show
    plt.savefig('blockedNormLearning.pdf', dpi = 100, transparency = True)
    plt.show()
    


def AEratios():
    #Set colours
    exp60col = '#0500a0'
    imp60col = '#037fc4'
    exp30col = '#ff8000'
    imp30col = '#e51636'
    
    fig, ax = plt.subplots(figsize = (3, 3)) #look this up later..
        
    ax. axhline(y=0.5, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
#    ax. axhline(y=1, xmin= 0, xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)

    ax.plot(2, np.nanmean(imp30ae_pp.ratio), color = imp30col, linewidth = 1, marker = '.')
    ax.plot(4, np.nanmean(exp30ae_pp.ratio), color = exp30col, linewidth = 1, marker = '.')
    ax.plot(6, np.nanmean(imp60ae_pp.ratio), color = imp60col, linewidth = 1, marker = '.')
    ax.plot(8, np.nanmean(exp60ae_pp.ratio), color = exp60col, linewidth = 1, marker = '.')
        
    ax.errorbar(x = 2 , y = np.nanmean(imp30ae_pp.ratio), yerr = get_CI(imp30ae_pp.ratio)[1] - np.nanmean(imp30ae_pp.ratio), alpha = 0.2, color = imp30col, linewidth = 3)
    ax.errorbar(x = 4 , y = np.nanmean(exp30ae_pp.ratio), yerr = get_CI(exp30ae_pp.ratio)[1] - np.nanmean(exp30ae_pp.ratio), alpha = 0.2, color = exp30col, linewidth = 3)
    ax.errorbar(x = 6 , y = np.nanmean(imp60ae_pp.ratio), yerr = get_CI(imp60ae_pp.ratio)[1] - np.nanmean(imp60ae_pp.ratio), alpha = 0.2, color = imp60col, linewidth = 3)
    ax.errorbar(x = 8 , y = np.nanmean(exp60ae_pp.ratio), yerr = get_CI(exp60ae_pp.ratio)[1] - np.nanmean(exp60ae_pp.ratio), alpha = 0.2, color = exp60col, linewidth = 3)

    #axes labels (as texts)
#    fig.text(0.5, .01,'Group', ha = 'center')
    plt.ylabel('Strategy Use Ratio')
#    plt.xlabel('Group')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # ax.yaxis.tick_left()
    # ax.tick_params(labelright='off')
    # ax2.yaxis.tick_right()
    ax.xaxis.set_ticks_position('bottom') 
    ax.yaxis.set_ticks_position('left') 
    
    plt.setp((ax), xticks=[2,4, 6, 8], xticklabels=['NI\n30', 'I\n30', 'NI\n60', 'I\n60'])

    ax.set_yticks([0.5, 0.6, 0.7, 0.8])
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1)
    ax.tick_params(axis='both', length= 4, width= 1)

    plt.tight_layout() #makes room for the x-axis label
    
    #axes
    ax.set_xlim(0,10) #ranges
#    ax.set_ylim(-0.2, 1.2, auto = False)

    #save figure show
    plt.savefig('AEratios.pdf', dpi = 100, transparency = True)
    plt.show()


#%%plot

plotLCmeans()
plotNormLCmeans()