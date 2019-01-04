import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.interpolate import spline
#import scipy.ndimage.filters
import scipy.stats as st
import seaborn as sns
#import sys

# os.chdir('c://Users/kineuser/Desktop/Shanaa/exp/explicit/data') #set the working directory AT SCHOOL PC
#os.chdir('E://Shanaa\'s Stuff/Documents/Shanaa/exp/explicit/data') #set the working directory AT HOME
os.chdir('D://shanaa/exp/explicit/data') #set the working directory ON LAPTOP

#set default font for pyplot
plt.rc('font',family='Calibri', size = 9)

#Set colours
exp60col = '#0500a0'
imp60col = '#037fc4'
exp30col = '#ff8000'
imp30col = '#e51636'

#%%

#import aftereffects data

aeDF60exp = pd.read_csv('exp60_reachAEs_pp.csv', usecols = [1,2]).T
aeDF60imp = pd.read_csv('imp60_reachAEs_pp.csv', usecols = [1,2]).T
aeDF30exp = pd.read_csv('exp30_reachAEs_pp.csv', usecols = [1,2]).T
aeDF30imp = pd.read_csv('imp30_reachAEs_pp.csv', usecols = [1,2]).T

#make array of mean values
standard60e = aeDF60exp.mean(axis = 1)
standard60i = aeDF60imp.mean(axis = 1)
standard30e = aeDF30exp.mean(axis = 1)
standard30i = aeDF30imp.mean(axis = 1)
standardAE = np.array([standard60e, standard60i, standard30e, standard30i])

#function to calculate CIs (no NaN removal)
def get_CI(groupDF):
    participantNum = len(groupDF.T)
    return np.array (st.t.interval(0.95, participantNum-1, loc=np.mean(groupDF.iloc[:, 0:participantNum].T), scale=st.sem(groupDF.iloc[:, 0:participantNum].T)))

aeDF60eLowerCI = get_CI(aeDF60exp)[0]
aeDF60eUpperCI = get_CI(aeDF60exp)[1]
aeDF60iLowerCI = get_CI(aeDF60imp)[0]
aeDF60iUpperCI = get_CI(aeDF60imp)[1]
aeDF30eLowerCI = get_CI(aeDF30exp)[0]
aeDF30eUpperCI = get_CI(aeDF30exp)[1]
aeDF30iLowerCI = get_CI(aeDF30imp)[0]
aeDF30iUpperCI = get_CI(aeDF30imp)[1]
aeDFCI = list([aeDF60eLowerCI, aeDF60eUpperCI, aeDF60iLowerCI, aeDF60iUpperCI, aeDF30eLowerCI, aeDF30eUpperCI, aeDF30iLowerCI, aeDF30iUpperCI])


def plotAE(x, ci):
    
    fig, ax = plt.subplots(figsize = (3, 3)) #look this up later..
    
#    ax. axhline(y=15, xmin= 0 , xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 2)
    ax. axhline(y=30, xmin= 0 , xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
    ax. axhline(y=60, xmin= 0 , xmax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)

#==============================================================================
#     #Distinct plot
#     plt.plot([0, 1],x[0], label = 'Instructed 60', color = exp60col, linewidth = 0, marker = "o", markersize = 10, mew = 5)
#     plt.plot([0, 1],x[1], label = 'Non-instructed 60', color = imp60col, linewidth = 0, marker = "o", markersize = 10, mew = 5)
#     plt.plot([0, 1],x[2], label = 'Instructed 30', color = exp30col, linewidth = 0, marker = "o", markersize = 10, mew = 5)
#     plt.plot([0, 1],x[3], label = 'Non-instructed 30', color = imp30col, linewidth = 0, marker = "o", markersize = 10, mew = 5)
#     
#     plt.plot([0, 1],x[0], label = 'Instructed 60', color = exp60col, linewidth = 4, alpha = 0.5)
#     plt.plot([0, 1],x[1], label = 'Non-instructed 60', color = imp60col, linewidth = 4, linestyle = 'dashed', alpha = 0.5)
#     plt.plot([0, 1],x[2], label = 'Instructed 30', color = exp30col, linewidth = 4, alpha = 0.5)
#     plt.plot([0, 1],x[3], label = 'Non-instructed 30', color = imp30col, linewidth = 4, linestyle = 'dashed', alpha = 0.5)
# 
#     plt.errorbar(x = [0,1] , y = x[0], yerr = ci[0] - x[0], alpha = 0.2, color = exp60col, linewidth = 10, linestyle = 'none')
#     plt.errorbar(x = [0,1] , y = x[1], yerr = ci[2] - x[1], alpha = 0.2, color = imp60col, linewidth = 10, linestyle = 'none')
#     plt.errorbar(x = [0,1] , y = x[2], yerr = ci[4] - x[2], alpha = 0.2, color = exp30col, linewidth = 10, linestyle = 'none')
#     plt.errorbar(x = [0,1] , y = x[3], yerr = ci[6] - x[3], alpha = 0.2, color = imp30col, linewidth = 10, linestyle = 'none')
#     
#==============================================================================
    #Regular plot
    plt.plot([0, 1],x[3], label = 'NI30', color = imp30col, linewidth = 2, linestyle = 'dashed')
    plt.plot([0, 1],x[2], label = 'I30', color = exp30col, linewidth = 2)
    plt.plot([0, 1],x[1], label = 'NI60', color = imp60col, linewidth = 2, linestyle = 'dashed')
    plt.plot([0, 1],x[0], label = 'I60', color = exp60col, linewidth = 2)

    plt.fill_between([0, 1] ,ci[0] , ci[1], alpha = 0.2, color = exp60col, linewidth = 0.0)
    plt.fill_between([0, 1] ,ci[2] , ci[3], alpha = 0.2, color = imp60col, linewidth = 0.0)
    plt.fill_between([0, 1] ,ci[4] , ci[5], alpha = 0.2, color = exp30col, linewidth = 0.0)
    plt.fill_between([0, 1] ,ci[6] , ci[7], alpha = 0.2, color = imp30col, linewidth = 0.0)

    #legend
    legend = plt.legend(loc = 'upper left', fontsize = 9)
    legend.get_frame().set_facecolor('none')
    legend.get_frame().set_linewidth(0.0)
    
    #axes
    plt.xticks([0, 1],["Without\nStrategy", "With\nStrategy"])
    plt.ylabel('Angular Deviation (°)')
    
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(0, 60)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom') 
    ax.yaxis.set_ticks_position('left') 
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1)        
    ax.tick_params(axis='both', length= 4, width= 1)
    
    plt.tight_layout() #makes room for the x-axis label
    
    #save and show
    plt.savefig('afterEffects.pdf', dpi = 100, transparency = True)
    plt.show()


#%% make plot 
plotAE(standardAE, aeDFCI)

# For testing
# x = standardAE
# ci = aeDFCI
# groupDF = aeDF30imp


 #%%awareness plot
#==============================================================================
# awareness = np.array([np.mean(imp30aware), np.mean(exp30aware), np.mean(imp60aware), np.mean(exp60aware)])
# awareness = np.append([np.arange(0, 4)],[awareness], axis = 0) #make an array of means
# 
#==============================================================================
def plotAwareness():
    awarenessDF = pd.read_csv('participantAwareness.csv')[['group', 'Points']]

    exp60aware = list(awarenessDF.loc[awarenessDF['group'] == '60explicit']['Points'])
    imp60aware = list(awarenessDF.loc[awarenessDF['group'] == '60implicit']['Points'])
    exp30aware = list(awarenessDF.loc[awarenessDF['group'] == '30explicit']['Points'])
    imp30aware = list(awarenessDF.loc[awarenessDF['group'] == '30implicit']['Points'])
    
    allData = [np.array(exp60aware),np.array(imp60aware), np.array(exp30aware),np.array(imp30aware)]

    fig, ax = plt.subplots(figsize = (4, 4)) 
    
#==============================================================================
#     bplot = ax.boxplot(allData, vert=False, patch_artist=True)   # fill with color
#     # fill with colors
#     colors = [exp60col, imp60col, exp30col, imp30col]
#     for patch, color in zip(bplot['boxes'], colors):
#         patch.set_facecolor(color)
#     
#==============================================================================
    
    plt.plot(0, 4, label = 'Instructed 60', color = exp60col, linewidth = 0, marker = "o", markersize = np.sqrt(exp60aware.count(0) / np.pi)* 50,  alpha=0.4)
    plt.plot(1, 4, label = 'Instructed 60', color = exp60col, linewidth = 0, marker = "o", markersize = np.sqrt(exp60aware.count(1) / np.pi)* 50,  alpha=0.4)
    plt.plot(2, 4, label = 'Instructed 60', color = exp60col, linewidth = 0, marker = "o", markersize = np.sqrt(exp60aware.count(2) / np.pi)* 50,  alpha=0.4)
    plt.plot(3, 4, label = 'Instructed 60', color = exp60col, linewidth = 0, marker = "o", markersize = np.sqrt(exp60aware.count(3) / np.pi)* 50,  alpha=0.4)
    
    plt.plot(0, 3, label = 'Non-instructed 60', color = imp60col, linewidth = 0, marker = "o", markersize = np.sqrt(imp60aware.count(0) / np.pi)* 50,  alpha=0.4)
    plt.plot(1, 3, label = 'Non-instructed 60', color = imp60col, linewidth = 0, marker = "o", markersize = np.sqrt(imp60aware.count(1) / np.pi)* 50,  alpha=0.4)
    plt.plot(2, 3, label = 'Non-instructed 60', color = imp60col, linewidth = 0, marker = "o", markersize = np.sqrt(imp60aware.count(2) / np.pi)* 50,  alpha=0.4)
    plt.plot(3, 3, label = 'Non-instructed 60', color = imp60col, linewidth = 0, marker = "o", markersize = np.sqrt(imp60aware.count(3) / np.pi)* 50,  alpha=0.4)
    
    plt.plot(0, 2, label = 'Instructed 30', color = exp30col, linewidth = 0, marker = "o", markersize = np.sqrt(exp30aware.count(0) / np.pi)* 50,  alpha=0.4)
    plt.plot(1, 2, label = 'Instructed 30', color = exp30col, linewidth = 0, marker = "o", markersize = np.sqrt(exp30aware.count(1) / np.pi)* 50,  alpha=0.4)
    plt.plot(2, 2, label = 'Instructed 30', color = exp30col, linewidth = 0, marker = "o", markersize = np.sqrt(exp30aware.count(2) / np.pi)* 50,  alpha=0.4)
    plt.plot(3, 2, label = 'Instructed 30', color = exp30col, linewidth = 0, marker = "o", markersize = np.sqrt(exp30aware.count(3) / np.pi)* 50,  alpha=0.4)

    plt.plot(0, 1, label = 'Non-instructed 30', color = imp30col, linewidth = 0, marker = "o", markersize = np.sqrt(imp30aware.count(0) / np.pi)* 50,  alpha=0.4)
    plt.plot(1, 1, label = 'Non-instructed 30', color = imp30col, linewidth = 0, marker = "o", markersize = np.sqrt(imp30aware.count(1) / np.pi)* 50,  alpha=0.4)
    plt.plot(2, 1, label = 'Non-instructed 30', color = imp30col, linewidth = 0, marker = "o", markersize = np.sqrt(imp30aware.count(2) / np.pi)* 50,  alpha=0.4)
    plt.plot(3, 1, label = 'Non-instructed 30', color = imp30col, linewidth = 0, marker = "o", markersize = np.sqrt(imp30aware.count(3) / np.pi)* 50,  alpha=0.4)

    #axes
    plt.xticks([0, 1, 2, 3],["0", "1", '2', '3'])
    plt.yticks([1, 2, 3, 4],["Non-instructed\n30", "Instructed\n30", 'Non-instructed\n60', 'Instructed\n60'])
    plt.xlabel('Awareness Score')
    
    ax.set_xlim(-1, 4)
    ax.set_ylim(0, 5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom') 
    ax.yaxis.set_ticks_position('left') 
    
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)        
    ax.tick_params(axis='both', length= 9, width= 2)
    
    #save and show
    plt.savefig('awarenessPlot.pdf', dpi = 100, transparency = True)

    plt.show()

#plotAwareness()

#%% correlations

def plotCorrelations(LAdata, colours):
    
    fig, axes  = plt.subplots(2, 2, sharey = True, facecolor = 'w', figsize = (3, 3)) #look this up later..

    for key in LAdata:
        axes[0,0].scatter(LAdata[key]['awarenessRatio'], LAdata[key]['prop_means'], label = key, color = colours[key], marker = '.')
        
    for key in LAdata:
        axes[0,1].scatter(LAdata[key]['awareness_score'], LAdata[key]['prop_means'], label = key, color = colours[key], marker = '.')    
        
    for key in LAdata:
        axes[1,0].scatter(LAdata[key]['awarenessRatio'], LAdata[key]['pred_means'], label = key, color = colours[key], marker = '.')
        
    for key in LAdata:
        axes[1,1].scatter(LAdata[key]['awareness_score'], LAdata[key]['pred_means'], label = key, color = colours[key], marker = '.')
    
    #legend    
    legend = axes[0,0].legend(loc = 'upper left', fontsize = 9)
    legend.get_frame().set_facecolor('none')
    legend.get_frame().set_linewidth(0.0)

    #axes
#    ax.xlabel('Strategy Use Ratio')
#    ax.ylabel('Afferent-based changes \nin hand-localization (°)')
    
    ratioSubplots = [(0,0), (1,0)]
    awarenessSubplots = [(0,1), (1,1)]

    for subplot in ratioSubplots:
        axes[subplot].set_xlim(0, 1.2)
        axes[subplot].set_ylim(10, -30)
        axes[subplot].spines['top'].set_visible(False)
        axes[subplot].spines['right'].set_visible(False)
        axes[subplot].xaxis.set_ticks_position('bottom') 
        axes[subplot].yaxis.set_ticks_position('left')
        axes[subplot].set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        axes[subplot].spines['left'].set_bounds(10, -30)
        axes[subplot].spines['bottom'].set_bounds(0, 1)
        
    for subplot in awarenessSubplots:
        axes[subplot].set_xlim(-1, 4)
        axes[subplot].set_ylim(10, -30)
        axes[subplot].spines['top'].set_visible(False)
        axes[subplot].spines['right'].set_visible(False)
        axes[subplot].xaxis.set_ticks_position('bottom') 
        axes[subplot].yaxis.set_ticks_position('left')
        axes[subplot].set_xticks([0, 1, 2, 3])
        axes[subplot].spines['left'].set_bounds(10, -30)
        axes[subplot].spines['bottom'].set_bounds(0, 3)
        
    axes[0,0].set_ylabel('Afferent based changes in localization')
    axes[1,0].set_ylabel('Afferent based changes in localization')
    axes[1,0].set_xlabel('Awareness ratio')
    axes[1,1].set_xlabel('Awareness score')

    plt.savefig('correlationPlots.pdf', dpi = 100, transparency = True)


    plt.show()   
    
    
def plotAwareCorr(LAdata, colours):
    
    fig, ax  = plt.subplots(figsize = (3, 3)) #look this up later..
    
    ax. axvline(x=0.5, ymin= 0 , ymax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)

    for key in LAdata:
        #ax.scatter(LAdata[key]['awarenessRatio'], LAdata[key]['awareness_score'] + offsets[key], label = key, color = colours[key], marker = '.', linewidths = 0, s = 100, alpha = 0.7)
        allData = pd.concat( [LAdata[key] for key in LAdata], ignore_index=True)

    sns.regplot(allData['awareness_score'],  allData['prop_means'] * -1,  color = affCol, label = 'Afferent Changes', marker = '.', x_jitter = 0.2, scatter_kws={'linewidths':0, 'alpha':0.4, 's':100})
    sns.regplot(allData['awareness_score'],  allData['pred_means'] * -1,  color = effCol, label = 'Efferent Changes', marker = '.', x_jitter = 0.2, scatter_kws={'linewidths':0, 'alpha':0.4, 's':100})
 
    #legend    
    legend = ax.legend(loc = 'upper left', fontsize = 9, labelspacing=0.2)
    legend.get_frame().set_facecolor('none')
    legend.get_frame().set_linewidth(0.0)

    #ax
    ax.set_facecolor('w')

    ax.set_xlim(-1, 4)
    ax.set_ylim(-10, 30)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom') 
    ax.yaxis.set_ticks_position('left')
    ax.set_xticks([0, 1, 2, 3])
#    ax.spines['left'].set_bounds(0, 3)
#    ax.spines['bottom'].set_bounds(0.2, 1)
    
        
    ax.set_ylabel('Changes in Localization (°)')
    ax.set_xlabel('Questionnaire Awareness Score')

    
    plt.savefig('awarenessCorrPlots.pdf', dpi = 100, transparency = True)


    plt.show()    

def propPredVExc(LAdata, colours):
    
    fig, ax  = plt.subplots(figsize = (3, 3)) #look this up later..
    
#    ax. axvline(x=0.5, ymin= 0 , ymax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
#
    for key in LAdata:
#        ax.scatter(LAdata[key]['awarenessRatio'], LAdata[key]['awareness_score'] + offsets[key], label = key, color = colours[key], marker = '.')

        #regression line
        allData = pd.concat( [LAdata[key] for key in LAdata], ignore_index=True)

    sns.regplot(allData['exclusive'],  allData['prop_means'] * -1,  color = affCol, label = 'Afferent Changes', marker = '.', scatter_kws={'linewidths':0, 'alpha':0.7, 's':100})
    sns.regplot(allData['exclusive'],  allData['pred_means'] * -1,  color = effCol, label = 'Efferent Changes', marker = '.', scatter_kws={'linewidths':0, 'alpha':0.7, 's':100})
       
#    #legend    
#    legend = ax.legend(loc = 'best', fontsize = 9, labelspacing=0.2)
#    legend.get_frame().set_facecolor('none')
#    legend.get_frame().set_linewidth(0.0)

    #ax
    ax.set_facecolor('w')

#    ax.set_xlim(0, 1.2)
    ax.set_ylim(-10, 30)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
#    ax.xaxis.set_ticks_position('bottom') 
#    ax.yaxis.set_ticks_position('left')
    ax.set_xticks([10, 20, 30])
#    ax.set_yticks([0, 1, 2, 3])
#    ax.spines['left'].set_bounds(0, 3)
#    ax.spines['bottom'].set_bounds(0.2, 1)
        
        
    ax.set_ylabel('Changes in Localization (°)')
    ax.set_xlabel('Without Strategy')

    
    plt.savefig('propPredVExc.pdf', dpi = 100, transparency = True)


    plt.show()    

def propPredVInc(LAdata, colours):
    
    fig, ax  = plt.subplots(figsize = (3, 3)) #look this up later..
    
#    ax. axvline(x=0.5, ymin= 0 , ymax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
#
    for key in LAdata:
#        ax.scatter(LAdata[key]['awarenessRatio'], LAdata[key]['awareness_score'] + offsets[key], label = key, color = colours[key], marker = '.')

        #regression line
        allData = pd.concat( [LAdata[key] for key in LAdata], ignore_index=True)

    sns.regplot(allData['inclusive'],  allData['prop_means'] * -1,  color = affCol, label = 'Afferent Changes', marker = '.', scatter_kws={'linewidths':0, 'alpha':0.7, 's':100})
    sns.regplot(allData['inclusive'],  allData['pred_means'] * -1,  color = effCol, label = 'Efferent Changes', marker = '.', scatter_kws={'linewidths':0, 'alpha':0.7, 's':100})
       
#    #legend    
#    legend = ax.legend(loc = 'best', fontsize = 9, labelspacing=0.2)
#    legend.get_frame().set_facecolor('none')
#    legend.get_frame().set_linewidth(0.0)

    #ax
    ax.set_facecolor('w')

#    ax.set_xlim(0, 1.2)
    ax.set_ylim(-10, 30)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
#    ax.xaxis.set_ticks_position('bottom') 
#    ax.yaxis.set_ticks_position('left')
#    ax.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
#    ax.set_yticks([0, 1, 2, 3])
#    ax.spines['left'].set_bounds(0, 3)
#    ax.spines['bottom'].set_bounds(0.2, 1)
        
        
    ax.set_ylabel('Changes in Localization (°)')
    ax.set_xlabel('With Strategy')

    
    plt.savefig('propPredVInc.pdf', dpi = 100, transparency = True)


    plt.show()  
    
def propPredVRatio(LAdata, colours):
    
    fig, ax  = plt.subplots(figsize = (3, 3)) #look this up later..
    
#    ax. axvline(x=0.5, ymin= 0 , ymax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
#
    for key in LAdata:
#        ax.scatter(LAdata[key]['awarenessRatio'], LAdata[key]['awareness_score'] + offsets[key], label = key, color = colours[key], marker = '.')

        #regression line
        allData = pd.concat( [LAdata[key] for key in LAdata], ignore_index=True)

    sns.regplot(allData['awarenessRatio'],  allData['prop_means'],  color = affCol, label = 'Afferent Changes', marker = '.', scatter_kws={'linewidths':0, 'alpha':0.7, 's':100})
    sns.regplot(allData['awarenessRatio'],  allData['pred_means'],  color = effCol, label = 'Efferent Changes', marker = '.', scatter_kws={'linewidths':0, 'alpha':0.7, 's':100})
       
    #legend    
    legend = ax.legend(loc = 'best', fontsize = 9, labelspacing=0.2)
    legend.get_frame().set_facecolor('none')
    legend.get_frame().set_linewidth(0.0)

    #ax
    ax.set_facecolor('w')

#    ax.set_xlim(0, 1.2)
    ax.set_ylim(-30, 10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
#    ax.xaxis.set_ticks_position('bottom') 
#    ax.yaxis.set_ticks_position('left')
#    ax.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
#    ax.set_yticks([0, 1, 2, 3])
#    ax.spines['left'].set_bounds(0, 3)
#    ax.spines['bottom'].set_bounds(0.2, 1)
        
        
    ax.set_ylabel('Changes in Localization (°)')
    ax.set_xlabel('Strategy Use Ratio')

    
    plt.savefig('propPredVRatio.pdf', dpi = 100, transparency = True)


    plt.show() 

def ExcVInc(LAdata, colours):
    
    fig, ax  = plt.subplots(figsize = (3, 3)) #look this up later..
    
#    ax. axvline(x=0.5, ymin= 0 , ymax= 1, color = '#bababa', linestyle = 'dashed', linewidth = 1)
#
    for key in LAdata:
#        ax.scatter(LAdata[key]['awarenessRatio'], LAdata[key]['awareness_score'] + offsets[key], label = key, color = colours[key], marker = '.')

        #regression line
        allData = pd.concat( [LAdata[key] for key in LAdata], ignore_index=True)

    sns.regplot(allData['inclusive'],  allData['exclusive'],  color = 'grey', marker = '.', scatter_kws={'linewidths':0, 'alpha':0.7, 's':100})
       
#    #legend    
#    legend = ax.legend(loc = 'best', fontsize = 9, labelspacing=0.2)
#    legend.get_frame().set_facecolor('none')
#    legend.get_frame().set_linewidth(0.0)
#
    #ax
    ax.set_facecolor('w')

#    ax.set_xlim(0, 1.2)
#    ax.set_ylim(-30, 10)
#    ax.spines['top'].set_visible(False)
#    ax.spines['right'].set_visible(False)
#    ax.xaxis.set_ticks_position('bottom') 
#    ax.yaxis.set_ticks_position('left')
#    ax.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
#    ax.set_yticks([0, 1, 2, 3])
#    ax.spines['left'].set_bounds(0, 3)
#    ax.spines['bottom'].set_bounds(0.2, 1)
        
        
    ax.set_ylabel('Without Strategy')
    ax.set_xlabel('With Strategy')

    
    plt.savefig('ExcVInc.pdf', dpi = 100, transparency = True)


    plt.show()          
    
LAdata = {'NI30' : pd.read_csv('imp30_locAwareness.csv'),
    'I30' : pd.read_csv('exp30_locAwareness.csv'),
    'NI60' : pd.read_csv('imp60_locAwareness.csv'),
    'I60' : pd.read_csv('exp60_locAwareness.csv')}
colours = {'NI30': imp30col, 'I30': exp30col, 'NI60': imp60col, 'I60': exp60col}
offsets = {'NI30': 0.30, 'I30': 0.10, 'NI60': -0.10, 'I60': -0.30}
affCol = '#8c058c'
effCol = '#067217'

#plotCorrelations(LAdata, colours)
plotAwareCorr(LAdata, colours)
propPredVExc(LAdata, colours)
propPredVInc(LAdata, colours)
#propPredVRatio(LAdata, colours)
#ExcVInc(LAdata, colours)

#%%
##Violin plots
#aeDF60exp = pd.read_csv('exp60_reachAEs_pp.csv', usecols = [1,2])
#aeDF60exp['group'] = 'I60'
#aeDF60imp = pd.read_csv('imp60_reachAEs_pp.csv', usecols = [1,2])
#aeDF60imp['group'] = 'NI60'
#aeDF30exp = pd.read_csv('exp30_reachAEs_pp.csv', usecols = [1,2])
#aeDF30exp['group'] = 'I30'
#aeDF30imp = pd.read_csv('imp30_reachAEs_pp.csv', usecols = [1,2])
#aeDF30imp['group'] = 'NI30'
#
#aeDF = pd.concat([aeDF30imp, aeDF30exp, aeDF60imp, aeDF60exp])
#aeDF2 = pd.melt(aeDF, id_vars=['group'], value_vars=['inclusive', 'exclusive'])
#aeDF2.columns = ['group', 'strategyUse', 'reachDeviation']
#    
#fig, ax  = plt.subplots(figsize = (5, 5)) #look this up later..
#
#ax = sns.violinplot(x= 'group', y = 'reachDeviation', hue='strategyUse', data= aeDF2, palette="muted")
#
#legend = ax.legend(loc = 'upper left', fontsize = 9, labelspacing=0.2)
#
#plt.show()

