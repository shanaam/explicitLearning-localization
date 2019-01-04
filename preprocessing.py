#CHECK if there is outlier removal for tap BL calcs
import os
import sys
import pandas as pd
import numpy as np
import glob
import math

import multiprocessing

# os.chdir('c://Users/kineuser/Desktop/Shanaa/exp/explicit/data') #set the working directory AT SCHOOL PC
#os.chdir('E://Shanaa\'s Stuff/Documents/Shanaa/exp/explicit/data') #set the working directory AT HOME
os.chdir('D://shanaa/exp/explicit/data') #set the working directory ON LAPTOP

# #checks the number of files in participant folders
# from os.path import join, getsize
# for root, dirs, files in os.walk('exp60/'):
#     print(root, "consumes ", end="")
#     print(sum([getsize(join(root, name)) for name in files]), end="")
#     print(" bytes in", len(files), "non-directory files")

#Define some things
targAngs = [45, 90, 135] #The possible angles of yellow targets
interpoints = [50, 90, 130]
homePosition = [0, -8.5] #Home position for the robot

#%%functions

#returns LIST of all the participant names in a given directory (group)
def names (group): 
    return next(os.walk(group))[1]
    
#returns a DATAFRAME for reach data 
def readReachData (participant, perturbation, taskType): #perturbation can be either 'aligned' OR 'rotated', taskType can be 'train' or 'no_cursor'
    if perturbation == 'aligned':
        return pd.read_table( glob.glob( participant + '*' + 'align' + '*' + taskType + '_selected.txt')[0], header = None, names = ['TrialNum', 'TargetAng', 'Cursor X', 'Cursor Y', 'Robot X', 'Robot Y', 'Screen Offset X', 'Screen Offset Y', 'Home Position X', 'Home Position Y','Target X','Target Y', 'BlockNum', 'Rotation', 'Time (ms)', 'Selected', 'Reach', 'Unknown', 'MaxV'])
    elif perturbation == 'rotated':
        filename = glob.glob( participant + '*' + taskType + '_selected.txt')
        filename.sort(key= len)
        return pd.read_table(filename[1], header = None, names = ['TrialNum', 'TargetAng', 'Cursor X', 'Cursor Y', 'Robot X', 'Robot Y', 'Screen Offset X', 'Screen Offset Y', 'Home Position X', 'Home Position Y','Target X','Target Y', 'BlockNum', 'Rotation', 'Time (ms)', 'Selected', 'Reach', 'Unknown', 'MaxV'])

#return angular deviation given a single row of data and a target angle (math)
def angleDevCalc (row, targAng):
    return (math.degrees(math.atan2(row['Robot Y'] - homePosition[1], row['Robot X'] - homePosition[0])) % 360) - targAng #modulo 360 to fix the disconnect at 180 degrees

#return a LIST of mean angular deviations PER target angle given a dataframe, first trial to calculate, and last trial (exclusive)
def meanAngDevs (df, start, end): 
    angles = []
    for targAng in targAngs:
        robotXY = df[(df.Selected == 1) & (df.MaxV == 1) & (df.TargetAng == targAng) & (df.TrialNum >= start) & (df.TrialNum < end)][['Robot X', 'Robot Y']]
        angleDevs = []
        for idx, row in robotXY.iterrows():
            angleDevs.append( angleDevCalc(row, targAng) ) ##Angular deviation
        
#        #remove outliers from the list, THEN append (**being stingy with the outliers here cause they should all be the same**)
#        angleDevs = [v if np.abs(v - np.nanmean(angleDevs)) <= (2*np.nanstd(angleDevs)) else np.nan for v in angleDevs]
#        
        angles.append(np.nanmedian(angleDevs))
    return angles
  
#returns a LIST of baseline angles for each target
def baselineAngMeans (df, taskType):
    if taskType == 'train':
        angles = meanAngDevs(df, 16, 46)
    elif taskType == 'no_cursor':
        angles = meanAngDevs(df, 100, 325)
    return angles

#returns a LIST of training angles for each target (THIS DOES NOT NEED TO BE A FUNCTION)   
def trainAngMeans (df):
    angles = meanAngDevs(df, 1, 91)
    return angles
    
#return a list of angular deviations for a dataframe, given start and end trials.
def reachAngles (participant, start, end, taskType= 'train'): #tasktype can be 'train' or 'no_cursor'
    baselines = baselineAngMeans(readReachData(participant, 'aligned', taskType), taskType)
    df = readReachData(participant, 'rotated', taskType)
    if taskType == 'train':
        robotXY = df[(df.MaxV == 1) & (df.TrialNum >= start) & (df.TrialNum < end)][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']]
        reachAngs = []
        for idx, row in robotXY.iterrows():
            # print (row.TrialNum)
            if row.Selected == 1:
                # print (math.degrees(math.atan2(row['Robot Y'] - homePosition[1], row['Robot X'] - homePosition[0])) % 360)
                if row.TargetAng == 45:
                    reachAngs.append( angleDevCalc(row, 45) - baselines[0] )
                elif row.TargetAng == 90:
                    reachAngs.append( angleDevCalc(row, 90) - baselines[1] )
                else:
                    reachAngs.append( angleDevCalc(row, 135) - baselines[2] )
            else:
                reachAngs.append(np.nan)
        return reachAngs
        
    elif taskType == 'no_cursor':
        halfBlocks = pd.Series([np.arange(187, 196), np.arange(340, 349), np.arange(475, 484), np.arange(628, 637), np.arange(196, 205), np.arange(331, 340), np.arange(484, 493), np.arange(619, 628)], np.arange(1, 9))
        typeA = list(halfBlocks[1]) + list(halfBlocks[2]) + list(halfBlocks[3]) + list(halfBlocks[4])
        typeB = list(halfBlocks[5]) + list(halfBlocks[6]) + list(halfBlocks[7]) + list(halfBlocks[8])
        #for EI: typeA are Exclusive, for IE: typeA are Inclusive
        
        filename = glob.glob( participant + '*' +  'no_cursor_selected.txt')
        filename.sort(key= len)
        filename = filename[1]
        if 'EI' in filename:
            print('EI')
            exclusiveXY = df[(df.MaxV == 1) & (df.TrialNum.isin(typeA))][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']] # Exclusive
            inclusiveXY = df[(df.MaxV == 1) & (df.TrialNum.isin(typeB))][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']] # Inclusive
        elif 'IE' in filename:
            print ('IE')
            inclusiveXY = df[(df.MaxV == 1) & (df.TrialNum.isin(typeA))][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']] # Inclusive
            exclusiveXY = df[(df.MaxV == 1) & (df.TrialNum.isin(typeB))][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']] # Exclusive
            
        angularDevsInc = []
        trialNums = []
        instructionType = []
        participantName = []
        
        for idx, row in inclusiveXY.iterrows():
            # print (row.TrialNum)
            trialNums.append(row.TrialNum)
            instructionType.append('with')
            participantName.append(participant[-8:-1])
            if row.Selected == 1:
                # print (math.degrees(math.atan2(row['Robot Y'] - homePosition[1], row['Robot X'] - homePosition[0])) % 360)
                if row.TargetAng == 45:
                    angularDevsInc.append( angleDevCalc(row, 45) - baselines[0] )
                elif row.TargetAng == 90:
                    angularDevsInc.append( angleDevCalc(row, 90) - baselines[1] )
                else:
                    angularDevsInc.append( angleDevCalc(row, 135) - baselines[2] )
            else:
                angularDevsInc.append(np.nan)
                
        #remove outliers  (only for no_cursor)    
#        angularDevsInc = [v if np.abs(v - np.nanmean(angularDevsInc)) <= (3*np.nanstd(angularDevsInc)) else np.nan for v in angularDevsInc]
        
        angularDevsExc = []
        for idx, row in exclusiveXY.iterrows():
            # print (row.TrialNum)
            trialNums.append(row.TrialNum)
            instructionType.append('without')
            participantName.append(participant[-8:-1])
            if row.Selected == 1:
                # print (math.degrees(math.atan2(row['Robot Y'] - homePosition[1], row['Robot X'] - homePosition[0])) % 360)
                if row.TargetAng == 45:
                    angularDevsExc.append( angleDevCalc(row, 45) - baselines[0] )
                elif row.TargetAng == 90:
                    angularDevsExc.append( angleDevCalc(row, 90) - baselines[1] )
                else:
                    angularDevsExc.append( angleDevCalc(row, 135) - baselines[2] )
            else:
                angularDevsExc.append(np.nan)
        
        #remove outliers      
#        angularDevsExc = [v if np.abs(v - np.nanmean(angularDevsExc)) <= (3*np.nanstd(angularDevsExc)) else np.nan for v in angularDevsExc]

        
        return pd.DataFrame([angularDevsInc + angularDevsExc, trialNums, instructionType, participantName], ['angularDevs', 'trialNum', 'instruction', 'participant']).T

#save some CSVs    
def makeTrainingCSV(group):
    if group not in ['imp30/', 'exp30/', 'imp60/', 'exp60/', 'cursorJump/']:
        print (group + ' IS AN INCORRECT GROUP NAME!!!; format = \'imp30/\'')
        quit()
    else:
        groupdf = pd.DataFrame() #make a blank df
        for name in names(group):
            participant = group + name + '/'
            print(participant)
            # print(len(reachAngles(participant, 1, 91)))
            groupdf[name] = reachAngles(participant, 1, 91)
            # print(pd.DataFrame(reachAngles(participant, 1, 91), columns= [name])) #used for testing, ignore
            
        #remove outliers
#        print ('removing outliers (3stdev)')
#        for idx, row in groupdf.iterrows():
#            groupdf.iloc[idx] = groupdf.iloc[idx][~((groupdf.iloc[idx]-groupdf.iloc[idx].mean()).abs()>3*groupdf.iloc[idx].std())] #keep only the ones that are within +3 to -3 standard deviations PER ROW
        groupdf.to_csv( group[0:5] + '_curves.csv', header= True, index= False)

#save some CSVs    
def makeAfterEffectCSV(group):
    if group not in ['imp30/', 'exp30/', 'imp60/', 'exp60/', 'cursorJump/']:
        print (group + ' IS AN INCORRECT GROUP NAME!!!; format = \'imp30/\'')
        quit()
    else:
        groupdf = pd.DataFrame() #make a blank df
#        blockedLC = pd.read_csv('learningCurveAOVdata.csv')
        for name in names(group):
            participant = group + name + '/'
            print(participant)
#            finalBlockmean = float(blockedLC[blockedLC.participant == name]['finalblockmean'])
            
            #per participant stuff
            allData = reachAngles(participant, 1, 1, taskType= 'no_cursor')
            withStratMean = allData[allData.instruction == 'with'].angularDevs.median()
            withoutStratMean = allData[allData.instruction == 'without'].angularDevs.median() #should be 16.768 for ag_0906
            
#            awarenessRatio = (withStratMean - withoutStratMean)/ (finalBlockmean - withoutStratMean)
            seriesToAdd = pd.DataFrame([participant[-8 :-1], withoutStratMean, withStratMean], ['participant', 'exclusive', 'inclusive']).T          
            groupdf = pd.concat([groupdf, seriesToAdd])
            
        groupdf['awarenessRatio'] = groupdf.inclusive / (groupdf.inclusive + groupdf. exclusive)

        #save as .csv
        groupdf.to_csv( group[0:5] + '_reachAEs_pp.csv', header= True, index= False)

#==============================================================================
#         #All trials
#             groupdf = pd.concat([groupdf, reachAngles(participant, 1, 1, taskType= 'no_cursor')])
#             print(len(groupdf))
# 
#             # print(pd.DataFrame(reachAngles(participant, 1, 91), columns= [name])) #used for testing, ignore
#             
#         #save as .csv
#         groupdf.to_csv( group[0:5] + '_reachAEs.csv', header= True, index= False)
# 
#==============================================================================
#%% non baseline corrected for omnibus uses
#return a list of angular deviations for a dataframe, given start and end trials.
def nonBLReachAngles (participant, start, end, taskType= 'train'): #tasktype can be 'train' or 'no_cursor'
    df = readReachData(participant, 'rotated', taskType)
    bldf = readReachData(participant, 'aligned', taskType)

    if taskType == 'train':
        robotXY = df[(df.MaxV == 1) & (df.TrialNum >= start) & (df.TrialNum < end)][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']]
        reachAngs = []
    
    if taskType == 'train':
        robotXY = df[(df.MaxV == 1) & (df.TrialNum >= start) & (df.TrialNum < end)][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']]
        reachAngs = []
        for idx, row in robotXY.iterrows():
            # print (row.TrialNum)
            if row.Selected == 1:
                # print (math.degrees(math.atan2(row['Robot Y'] - homePosition[1], row['Robot X'] - homePosition[0])) % 360)
                if row.TargetAng == 45:
                    reachAngs.append( angleDevCalc(row, 45))
                elif row.TargetAng == 90:
                    reachAngs.append( angleDevCalc(row, 90))
                else:
                    reachAngs.append( angleDevCalc(row, 135))
            else:
                reachAngs.append(np.nan)
        return reachAngs
    
    elif taskType == 'no_cursor':
        halfBlocks = pd.Series([np.arange(187, 196), np.arange(340, 349), np.arange(475, 484), np.arange(628, 637), np.arange(196, 205), np.arange(331, 340), np.arange(484, 493), np.arange(619, 628)], np.arange(1, 9))
        typeA = list(halfBlocks[1]) + list(halfBlocks[2]) + list(halfBlocks[3]) + list(halfBlocks[4])
        typeB = list(halfBlocks[5]) + list(halfBlocks[6]) + list(halfBlocks[7]) + list(halfBlocks[8])
        #for EI: typeA are Exclusive, for IE: typeA are Inclusive
        
        filename = glob.glob( participant + '*' +  'no_cursor_selected.txt')
        filename.sort(key= len)
        filename = filename[1]
        if 'EI' in filename:
            print('EI')
            exclusiveXY = df[(df.MaxV == 1) & (df.TrialNum.isin(typeA))][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']] # Exclude
            inclusiveXY = df[(df.MaxV == 1) & (df.TrialNum.isin(typeB))][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']] # Include
        elif 'IE' in filename:
            print ('IE')
            inclusiveXY = df[(df.MaxV == 1) & (df.TrialNum.isin(typeA))][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']] # Include
            exclusiveXY = df[(df.MaxV == 1) & (df.TrialNum.isin(typeB))][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']] # Exclude
        
        bldfUse = bldf[bldf.MaxV == 1][['TrialNum', 'TargetAng', 'Robot X', 'Robot Y', 'Selected']] # Exclude
   
        angularDevsAligned = []
        trialNums = []
        session = []
        stratUse = []
        participantName = []
        
        #No cursor reaches from aligned session
        for idx, row in bldfUse.iterrows():
            # print (row.TrialNum)
            trialNums.append(row.TrialNum)
            session.append('aligned')
            stratUse.append('without')
            participantName.append(participant[-8:-1])
            if row.Selected == 1:
                # print (math.degrees(math.atan2(row['Robot Y'] - homePosition[1], row['Robot X'] - homePosition[0])) % 360)
                if row.TargetAng == 45:
                    angularDevsAligned.append( angleDevCalc(row, 45))
                elif row.TargetAng == 90:
                    angularDevsAligned.append( angleDevCalc(row, 90))
                else:
                    angularDevsAligned.append( angleDevCalc(row, 135))
            else:
                angularDevsAligned.append(np.nan)

                   
        angularDevsExc = []
        for idx, row in exclusiveXY.iterrows():
            # print (row.TrialNum)
            trialNums.append(row.TrialNum)
            session.append('rotated')
            stratUse.append('without')
            participantName.append(participant[-8:-1])
            if row.Selected == 1:
                # print (math.degrees(math.atan2(row['Robot Y'] - homePosition[1], row['Robot X'] - homePosition[0])) % 360)
                if row.TargetAng == 45:
                    angularDevsExc.append( angleDevCalc(row, 45))
                elif row.TargetAng == 90:
                    angularDevsExc.append( angleDevCalc(row, 90))
                else:
                    angularDevsExc.append( angleDevCalc(row, 135))
            else:
                angularDevsExc.append(np.nan)


        angularDevsInc = []
        for idx, row in inclusiveXY.iterrows():
            # print (row.TrialNum)
            trialNums.append(row.TrialNum)
            session.append('rotated')
            stratUse.append('with')
            participantName.append(participant[-8:-1])
            if row.Selected == 1:
                # print (math.degrees(math.atan2(row['Robot Y'] - homePosition[1], row['Robot X'] - homePosition[0])) % 360)
                if row.TargetAng == 45:
                    angularDevsInc.append( angleDevCalc(row, 45))
                elif row.TargetAng == 90:
                    angularDevsInc.append( angleDevCalc(row, 90))
                else:
                    angularDevsInc.append( angleDevCalc(row, 135))
            else:
                angularDevsInc.append(np.nan)
        
        finalDF = pd.DataFrame([angularDevsAligned + angularDevsExc + angularDevsInc, trialNums, session, stratUse, participantName], ['angularDevs', 'trialNum', 'session', 'stratUse', 'participant']).T
        
        return finalDF

#save some CSVs    
def makeNonBLAfterEffectCSV(group):
    if group not in ['imp30/', 'exp30/', 'imp60/', 'exp60/', 'cursorJump/']:
        print (group + ' IS AN INCORRECT GROUP NAME!!!; format = \'imp30/\'')
        quit()
    else:
        groupdf = pd.DataFrame() #make a blank df
        for name in names(group):
            participant = group + name + '/'
            print(participant)
            
            #per participant stuff
            allData = nonBLReachAngles(participant, 1, 1, taskType= 'no_cursor')
            alignedMedian = allData[allData.session == 'aligned'].angularDevs.median()
            rotatedWithoutMedian = allData[(allData.session == 'rotated') & (allData.stratUse == 'without')].angularDevs.median()
            seriesToAdd = pd.DataFrame([participant[-8 :-1], alignedMedian, rotatedWithoutMedian], ['participant', 'aligned', 'rotatedWithout']).T          
            groupdf = pd.concat([groupdf, seriesToAdd])
            
#        groupdf['awarenessRatio'] = groupdf.inclusive / (groupdf.inclusive + groupdf. exclusive)

        #save as .csv
        groupdf.to_csv( group[0:5] + '_sessionAEs_pp.csv', header= True, index= False)
            


#%%Tap Stuff

#kernel Regression
def kernelRegression(x, y, width, interpoints):
    output = []
    for interpoint in interpoints:
        w = np.exp(-1 * ((np.array(x) - interpoint)**2 / (2 * width**2)))
        sums = np.nansum(np.array(w)*np.array(y)) / np.nansum(np.array(w))
        output.append(sums)
    return output

#returns a DATAFRAME for tap data
def readTapData (participant, perturbation, taskType): #perturbation can be either 'aligned' OR 'rotated', taskType can be 'active' or 'passive'
    # return pd.read_table( glob.glob( participant + '*' + perturbation + '*' + taskType + '_tap.txt')[0] )
    if perturbation == 'aligned':
        return pd.read_table( glob.glob( participant + '*' + 'align' + '*' + taskType + '_tap_selected.txt')[0])
    elif perturbation == 'rotated':
        filename = glob.glob( participant + '*' + taskType + '_tap_selected.txt')
        filename.sort(key= len)
        return pd.read_table(filename[1])

#==============================================================================
# #THIS STUFF HAS TO DO WITH CALIBRATION FILE (not used in new methods)
# 
# #returns a DATAFRAME for calibration data
# def readCalibration (participant):
#     return pd.read_table( glob.glob( participant + '*' + '_calibration.txt')[0], header = None, names = ['TrialNum', 'TargetAng', 'RobotHomeX', 'RobotHomeY', 'RobotOutX', 'RobotOutY', 'TapHomeX', 'TapHomeY', 'TapOutX', 'TapOutY'] )
# 
# #return a LIST (2 long) with x and y from calibration
# def calibratedHome (participant):
#     calibration = readCalibration(participant)
#     return list([np.mean(calibration.TapHomeX), np.mean(calibration.TapHomeY)])
# 
# #return tap deviation given a single row of data and a target angle
# def tapDevCalc (row, participant):
#     return (180 - (math.degrees(math.atan2((row['YTouch'] - calibratedHome(participant)[1]) *1.2, row['XTouch'] - calibratedHome(participant)[0])) % 360) ) - row['TargetAngle'] #modulo 360 to fix the disconnect at 180 degrees
#==============================================================================

# #return tap deviation given a single row of data and a target angle
def tapDevCalc (row, participant):
    return (math.degrees(math.atan2((row['tapy_cm']), row['tapx_cm']) % 360) - row['targetangle_deg']) #modulo 360 to fix the disconnect at 180 degrees

#return a DATAFRAME of reach angles and angular deviations for a single participant
def tapAngs (participant, movementType, phase, per_pp = False): #phase can be 'rotated' or 'aligned'
    if movementType == 'active':
        activedf = readTapData(participant, phase, 'active')
        activeTapXY = activedf[['trial', 'targetangle_deg', 'tapx_cm', 'tapy_cm', 'selected']]
       
#==============================================================================
#         #get baselines
#         activeBLdf = readTapData(participant, 'aligned', 'active')
#         activeBLlist = []
#         for idx, row in activeBLdf.iterrows():
#             if row.selected == 1:
#                 activeBLlist.append(tapDevCalc(row, participant))
#             else:
#                 activeBLlist.append(np.nan)
#         #remove outliers from bl data.
#         activeBLlist = [v if np.abs(v - np.nanmean(activeBLlist)) <= (3*np.nanstd(activeBLlist)) else np.nan for v in activeBLlist]      
#                 
#         activeBL = np.nanmean(activeBLlist)       
#==============================================================================
        tapAngs = pd.DataFrame(columns=['reachAngle', 'deviation', 'type', 'trial', 'participant'])
        tapAngsIdx = 0
        
        for idx, row in activeTapXY.iterrows():
            #pd.DataFrame([row.TargetAngle, tapDevCalc(row, participant)- activeBL, row['Trial#'], participant[-8:-1]], columns=['reachAngle', 'Deviation', 'Trial#', 'participant']).append(tapAngs)
            if row['selected'] == 1:
                tapAngs.loc[tapAngsIdx] = ([row.targetangle_deg, tapDevCalc(row, participant), 'active', row['trial'], participant[-8:-1]])
            else:
                tapAngs.loc[tapAngsIdx] = ([row.targetangle_deg, np.nan, 'active', row['trial'], participant[-8:-1]])
            tapAngsIdx += 1
        
        #Outlier removal before kernel regression
        tapAngs.deviation = [v if np.abs(v - np.nanmean(tapAngs.deviation)) <= (3*np.nanstd(tapAngs.deviation)) else np.nan for v in tapAngs.deviation]
        
        if per_pp == True:
            interpointDev = kernelRegression(tapAngs.reachAngle, tapAngs.deviation, 10, interpoints)
            tapAngs_per_pp = pd.DataFrame(columns=[str(interpoints[0]) + ' deviation', str(interpoints[1]) + ' deviation', str(interpoints[2]) + ' deviation', 'type', 'participant'])
            tapAngs_per_pp.loc[0] = ([interpointDev[0], interpointDev[1], interpointDev[2], 'active', participant[-8:-1]])
            return tapAngs_per_pp
        return tapAngs    
    
    else:
        passivedf = readTapData(participant, phase, 'passive')
        passiveTapXY = passivedf[['trial', 'targetangle_deg', 'tapx_cm', 'tapy_cm', 'selected']]
        
#==============================================================================
#         #Calculate baseline
#         passiveBLdf = readTapData(participant, 'aligned', 'passive')
#         passiveBLlist = []
#         for idx, row in passiveBLdf.iterrows():
#             if row.selected == 1:
#                 passiveBLlist.append(tapDevCalc(row, participant))
#             else:
#                 passiveBLlist.append(np.nan)                
#         #remove outliers from bl data.
#         passiveBLlist = [v if np.abs(v - np.nanmean(passiveBLlist)) <= (3*np.nanstd(passiveBLlist)) else np.nan for v in passiveBLlist]      
#         passiveBL = np.nanmean(passiveBLlist)
# 
#==============================================================================
        tapAngs = pd.DataFrame(columns=['reachAngle', 'deviation', 'type', 'trial', 'participant'])
        tapAngsIdx = 0

        for idx, row in passiveTapXY.iterrows():
            #pd.DataFrame([row.TargetAngle, tapDevCalc(row, participant)- activeBL, row['Trial#'], participant[-8:-1]], columns=['reachAngle', 'Deviation', 'Trial#', 'participant']).append(tapAngs)
            if row['selected'] == 1:
                tapAngs.loc[tapAngsIdx] = ([row.targetangle_deg, tapDevCalc(row, participant), 'passive', row['trial'], participant[-8:-1]])
            else:
                tapAngs.loc[tapAngsIdx] = ([row.targetangle_deg, np.nan, 'passive', row['trial'], participant[-8:-1]])
            tapAngsIdx += 1
        
        #Outlier removal before kernel regression
        tapAngs.deviation = [v if np.abs(v - np.nanmean(tapAngs.deviation)) <= (3*np.nanstd(tapAngs.deviation)) else np.nan for v in tapAngs.deviation]
       
        if per_pp == True:
            interpointDev = kernelRegression(tapAngs.reachAngle, tapAngs.deviation, 10, interpoints)
            tapAngs_per_pp = pd.DataFrame(columns=[str(interpoints[0]) + ' deviation', str(interpoints[1]) + ' deviation', str(interpoints[2]) + ' deviation', 'type', 'participant'])
            tapAngs_per_pp.loc[0] = ([interpointDev[0], interpointDev[1], interpointDev[2], 'passive', participant[-8:-1]])
            return tapAngs_per_pp

        return tapAngs
    
#==============================================================================
#     passiveTapAngs = []
#     activeTapAngs = []
#     for idx, row in passiveTapXY.iterrows():
#         # print (math.degrees(math.atan2(row['Robot Y'] - homePosition[1], row['Robot X'] - homePosition[0])) % 360)
#         passiveTapAngs.append(tapDevCalc(row, participant) - passiveBL)
#     meanPassiveTaps = np.mean(passiveTapAngs)
#     for idx, row in activeTapXY.iterrows():
#         activeTapAngs.append(tapDevCalc(row, participant)- activeBL)
#     meanActiveTaps = np.mean(activeTapAngs)
#     
#     #Next return line is only for getting participant means
#     # return pd.DataFrame([0, meanPassiveTaps, 1, meanActiveTaps], index=['passiveReachAngle', 'passiveDeviation', 'activeReachAngle', 'activeDeviation']).T
# 
#     return pd.DataFrame([np.array(passiveTapXY['TargetAngle']), passiveTapAngs, np.array(passiveTapXY['Trial#']), np.array(activeTapXY['TargetAngle']), activeTapAngs], index=['passiveReachAngle', 'passiveDeviation','Trial#', 'activeReachAngle', 'activeDeviation']).T
# 
#==============================================================================

def makeTapCSVs (group):

    listOfNames = names(group)
#==============================================================================
#     participant = (group + listOfNames[0] + '/')
#     # tapDF = pd.DataFrame([], columns=['passiveReachAngle', 'passiveDeviation', 'activeReachAngle', 'activeDeviation'])
#     tapDF = tapAngs(participant)
#     
#==============================================================================
    tapDFaligned = pd.DataFrame()

    for part in listOfNames:
        participant = (group + part + '/')
        print(participant)
        tapDFaligned = pd.concat([tapDFaligned, tapAngs(participant, 'active', 'aligned', per_pp = True)])
        #tapDF = tapDF.append(tapAngs(participant)

#    #Outlier removal    
#    tapDFaligned['50 deviation'] = [v if np.abs(v - np.nanmean(tapDFaligned['50 deviation'])) <= (3*np.nanstd(tapDFaligned['50 deviation'])) else np.nan for v in tapDFaligned['50 deviation']]    
#    tapDFaligned['90 deviation'] = [v if np.abs(v - np.nanmean(tapDFaligned['90 deviation'])) <= (3*np.nanstd(tapDFaligned['90 deviation'])) else np.nan for v in tapDFaligned['90 deviation']]    
#    tapDFaligned['130 deviation'] = [v if np.abs(v - np.nanmean(tapDFaligned['130 deviation'])) <= (3*np.nanstd(tapDFaligned['130 deviation'])) else np.nan for v in tapDFaligned['130 deviation']]
    
    #Save active aligned
    tapDFaligned.to_csv(group[0:5] + '_activeTapData_aligned.csv', header= True, index= False) ## Save explicit stuff

    tapDFrotated = pd.DataFrame()

    for part in listOfNames:
        participant = (group + part + '/')
        print(participant)
        tapDFrotated = pd.concat([tapDFrotated, tapAngs(participant, 'active', 'rotated', per_pp = True)])
        #tapDF = tapDF.append(tapAngs(participant)

#    #Outlier removal    
#    tapDFrotated['50 deviation'] = [v if np.abs(v - np.nanmean(tapDFrotated['50 deviation'])) <= (3*np.nanstd(tapDFrotated['50 deviation'])) else np.nan for v in tapDFrotated['50 deviation']]    
#    tapDFrotated['90 deviation'] = [v if np.abs(v - np.nanmean(tapDFrotated['90 deviation'])) <= (3*np.nanstd(tapDFrotated['90 deviation'])) else np.nan for v in tapDFrotated['90 deviation']]    
#    tapDFrotated['130 deviation'] = [v if np.abs(v - np.nanmean(tapDFrotated['130 deviation'])) <= (3*np.nanstd(tapDFrotated['130 deviation'])) else np.nan for v in tapDFrotated['130 deviation']]
#   
    #Save active rotated
    tapDFrotated.to_csv(group[0:5] + '_activeTapData_rotated.csv', header= True, index= False) ## Save explicit stuff

    changeInTapDF = pd.DataFrame()

    changeInTapDF['50 deviation'] = tapDFrotated['50 deviation'] - tapDFaligned['50 deviation']
    changeInTapDF['90 deviation'] = tapDFrotated['90 deviation'] - tapDFaligned['90 deviation']
    changeInTapDF['130 deviation'] = tapDFrotated['130 deviation'] - tapDFaligned['130 deviation']
    changeInTapDF['type'] = tapDFrotated['type']
    changeInTapDF['participant'] = tapDFrotated['participant']
    #save to csv
    changeInTapDF.to_csv(group[0:5] + '_activeTapData.csv', header= True, index= False) ## Save explicit stuff
    
    #repeat for passive
    tapDFaligned = pd.DataFrame()
    
    for part in listOfNames:
        participant = (group + part + '/')
        print(participant)
        tapDFaligned = pd.concat([tapDFaligned, tapAngs(participant, 'passive', 'aligned', per_pp = True)])
        #tapDF = tapDF.append(tapAngs(participant)

    #Outlier removal    
    tapDFaligned['50 deviation'] = [v if np.abs(v - np.nanmean(tapDFaligned['50 deviation'])) <= (3*np.nanstd(tapDFaligned['50 deviation'])) else np.nan for v in tapDFaligned['50 deviation']]    
    tapDFaligned['90 deviation'] = [v if np.abs(v - np.nanmean(tapDFaligned['90 deviation'])) <= (3*np.nanstd(tapDFaligned['90 deviation'])) else np.nan for v in tapDFaligned['90 deviation']]    
    tapDFaligned['130 deviation'] = [v if np.abs(v - np.nanmean(tapDFaligned['130 deviation'])) <= (3*np.nanstd(tapDFaligned['130 deviation'])) else np.nan for v in tapDFaligned['130 deviation']]
  
    #Save passive aligned
    tapDFaligned.to_csv(group[0:5] + '_passiveTapData_aligned.csv', header= True, index= False) ## Save explicit stuff
    tapDFrotated = pd.DataFrame()

    for part in listOfNames:
        participant = (group + part + '/')
        print(participant)
        tapDFrotated = pd.concat([tapDFrotated, tapAngs(participant, 'passive', 'rotated', per_pp = True)])
        #tapDF = tapDF.append(tapAngs(participant)

#    #Outlier removal    
#    tapDFrotated['50 deviation'] = [v if np.abs(v - np.nanmean(tapDFrotated['50 deviation'])) <= (3*np.nanstd(tapDFrotated['50 deviation'])) else np.nan for v in tapDFrotated['50 deviation']]    
#    tapDFrotated['90 deviation'] = [v if np.abs(v - np.nanmean(tapDFrotated['90 deviation'])) <= (3*np.nanstd(tapDFrotated['90 deviation'])) else np.nan for v in tapDFrotated['90 deviation']]    
#    tapDFrotated['130 deviation'] = [v if np.abs(v - np.nanmean(tapDFrotated['130 deviation'])) <= (3*np.nanstd(tapDFrotated['130 deviation'])) else np.nan for v in tapDFrotated['130 deviation']]
   
    #Save active aligned
    tapDFrotated.to_csv(group[0:5] + '_passiveTapData_rotated.csv', header= True, index= False) ## Save explicit stuff

    changeInTapDF = pd.DataFrame()

    changeInTapDF['50 deviation'] = tapDFrotated['50 deviation'] - tapDFaligned['50 deviation']
    changeInTapDF['90 deviation'] = tapDFrotated['90 deviation'] - tapDFaligned['90 deviation']
    changeInTapDF['130 deviation'] = tapDFrotated['130 deviation'] - tapDFaligned['130 deviation']
    changeInTapDF['type'] = tapDFrotated['type']
    changeInTapDF['participant'] = tapDFrotated['participant']
    #save to csv
    changeInTapDF.to_csv(group[0:5] + '_passiveTapData.csv', header= True, index= False) ## Save explicit stuff

    
#==============================================================================
#     if phase == 'rotated': 
#         tapDF.to_csv(group[0:5] + '_activeTapData_rotated.csv', header= True, index= False) ## Save explicit stuff
#     elif phase == 'aligned':
#         tapDF.to_csv(group[0:5] + '_activeTapData_aligned.csv', header= True, index= False) ## Save explicit stuff
# 
#     tapDF = pd.DataFrame()
# 
#     for part in listOfNames:
#         participant = (group + part + '/')
#         print(participant)
#         tapDF = pd.concat([tapDF, tapAngs(participant, 'passive', phase, per_pp = True)])
#         #tapDF = tapDF.append(tapAngs(participant)
#         
#     #Outlier removal
#     tapDF['50 deviation'] = [v if np.abs(v - np.nanmean(tapDF['50 deviation'])) <= (3*np.nanstd(tapDF['50 deviation'])) else np.nan for v in tapDF['50 deviation']]    
#     tapDF['90 deviation'] = [v if np.abs(v - np.nanmean(tapDF['90 deviation'])) <= (3*np.nanstd(tapDF['90 deviation'])) else np.nan for v in tapDF['90 deviation']]    
#     tapDF['130 deviation'] = [v if np.abs(v - np.nanmean(tapDF['130 deviation'])) <= (3*np.nanstd(tapDF['130 deviation'])) else np.nan for v in tapDF['130 deviation']]
#     if phase == 'rotated': 
#         tapDF.to_csv(group[0:5] + '_passiveTapData_rotated.csv', header= True, index= False) ## Save explicit stuff
#     elif phase == 'aligned':
#         tapDF.to_csv(group[0:5] + '_passiveTapData_aligned.csv', header= True, index= False) ## Save explicit stuff
#         
# 
#     
#==============================================================================
#==============================================================================
#     tapDFHalfProcessed = tapDF[np.abs(tapDF.passiveDeviation-tapDF.passiveDeviation.mean())<=(3*tapDF.passiveDeviation.std())] #keep only the ones that are within +3 to -3 standard deviations in the column 'passiveDeviation'.
#     tapDFProcessed = tapDFHalfProcessed[np.abs(tapDFHalfProcessed.activeDeviation-tapDFHalfProcessed.activeDeviation.mean())<=(3*tapDFHalfProcessed.activeDeviation.std())] #keep only the ones that are within +3 to -3 standard deviations in the column 'activeDeviation'.
#     
#     if len(tapDF['activeDeviation']) < 200:
#         if group == 'imp60/':
#             tapDF.to_csv('allImplicitTapData_perParticipant.csv', header= True, index= False) ## Save implicit stuff
#             tapDFProcessed.to_csv('processedImplicitTapData_perParticipant.csv', header= True, index= False) ## Save implicit stuff
#         elif group == 'exp60/':
#             tapDF.to_csv('allExplicitTapData_perParticipant.csv', header= True, index= False) ## Save explicit stuff
#             tapDFProcessed.to_csv('processedExplicitTapData_perParticipant.csv', header= True, index= False) ## Save explicit stuff
#     else:    
#         if group == 'imp60/':
#             tapDF.to_csv('allImplicitTapData.csv', header= True, index= False) ## Save implicit stuff
#             tapDFProcessed.to_csv('processedImplicitTapData.csv', header= True, index= False) ## Save implicit stuff
#         elif group == 'exp60/':
#             tapDF.to_csv('allExplicitTapData.csv', header= True, index= False) ## Save explicit stuff
#             tapDFProcessed.to_csv('processedExplicitTapData.csv', header= True, index= False) ## Save explicit stuff
#     
#     
#     ## rest is plotting and fitting
#     # calculate polynomial
#     z = np.polyfit(tapDFProcessed['activeReachAngle'], tapDFProcessed['activeDeviation'], 1)
#     f = np.poly1d(z)
#     print (f)
#     
#     # calculate new x's and y's
#     x_new = np.linspace(min(tapDFProcessed['activeReachAngle']), max(tapDFProcessed['activeReachAngle']), 50)
#     y_new = f(x_new)
#     
#     plt.plot(tapDFProcessed['activeReachAngle'], tapDFProcessed['activeDeviation'],'o', x_new, y_new)
#     pylab.title('Polynomial Fit Active Localization')
#     ax = plt.gca()
#     ax.set_facecolor((0.898, 0.898, 0.898))
#     # fig = plt.gcf()
#     # py.plot_mpl(fig, filename='polynomial-Fit-with-matplotlib')
#     plt.show()
#     
#     # calculate polynomial
#     z2 = np.polyfit(tapDFProcessed['passiveReachAngle'], tapDFProcessed['passiveDeviation'], 1)
#     f2 = np.poly1d(z2)
#     print (f2)
#     
#     # calculate new x's and y's
#     x_new2 = np.linspace(min(tapDFProcessed['passiveReachAngle']), max(tapDFProcessed['passiveReachAngle']), 50)
#     y_new2 = f(x_new2)
#     
#     plt.plot(tapDFProcessed['passiveReachAngle'], tapDFProcessed['passiveDeviation'],'o', x_new2, y_new2)
#     pylab.title('Polynomial Fit Passive Localization')
#     ax2 = plt.gca()
#     ax.set_facecolor((0.898, 0.898, 0.898))
#     
#     plt.show()
#     
#     
#     #Make plots
#     fig, (ax, ax2)  = plt.subplots(1, 2, sharey = True, facecolor = 'w', figsize = (16, 9))
#     
#     ax.scatter(tapDFProcessed['activeReachAngle'], tapDFProcessed['activeDeviation'])
#     ax2.scatter(tapDFProcessed['passiveReachAngle'], tapDFProcessed['passiveDeviation'])
#     
#     ax.set_title('Active\nLocalization')
#     ax2.set_title('Passive\nLocalization')
#     
#     #Y limits (remove these to see outliers and such)
#     ax.set_ylim(40, -40)
#     ax2.set_ylim(40, -40)
#     
#     plt.show()
# 
# 
#==============================================================================

#%%
#blocked learning curve data
def makeBlocked ():
    imp30Curves = pd.read_csv('imp30_curves.csv')
    exp30Curves = pd.read_csv('exp30_curves.csv')
    imp60Curves = pd.read_csv('imp60_curves.csv')
    exp60Curves = pd.read_csv('exp60_curves.csv')
    
    blockedCurves = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
    blockedCurvesIdx = 0
    blockedFinal = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
        
    for column in imp30Curves:
        #print (imp30Curves[column])
        blockedCurves.loc[blockedCurvesIdx] = ([imp30Curves.columns[blockedCurvesIdx], np.nanmean(imp30Curves[column][0:3]), np.nanmean(imp30Curves[column][3:6]), np.nanmean(imp30Curves[column][6:9]), np.nanmean(imp30Curves[column][9:12]), np.nanmean(imp30Curves[column][81:90]), 'non-instructed', '30'])
        blockedCurvesIdx += 1
    blockedFinal = pd.concat([blockedFinal, blockedCurves])
    
    blockedCurves = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
    blockedCurvesIdx = 0
    
    for column in exp30Curves:
        #print (imp30Curves[column])
        blockedCurves.loc[blockedCurvesIdx] = ([exp30Curves.columns[blockedCurvesIdx], np.nanmean(exp30Curves[column][0:3]), np.nanmean(exp30Curves[column][3:6]), np.nanmean(exp30Curves[column][6:9]), np.nanmean(exp30Curves[column][9:12]), np.nanmean(exp30Curves[column][81:90]), 'instructed', '30'])
        blockedCurvesIdx += 1
    blockedFinal = pd.concat([blockedFinal, blockedCurves])
    
    blockedCurves = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
    blockedCurvesIdx = 0
    
    for column in imp60Curves:
        #print (imp30Curves[column])
        blockedCurves.loc[blockedCurvesIdx] = ([imp60Curves.columns[blockedCurvesIdx], np.nanmean(imp60Curves[column][0:3]), np.nanmean(imp60Curves[column][3:6]), np.nanmean(imp60Curves[column][6:9]), np.nanmean(imp60Curves[column][9:12]), np.nanmean(imp60Curves[column][81:90]), 'non-instructed', '60'])
        blockedCurvesIdx += 1
    blockedFinal = pd.concat([blockedFinal, blockedCurves])
    
    blockedCurves = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
    blockedCurvesIdx = 0
    
    for column in exp60Curves:
        #print (imp30Curves[column])
        blockedCurves.loc[blockedCurvesIdx] = ([exp60Curves.columns[blockedCurvesIdx], np.nanmean(exp60Curves[column][0:3]), np.nanmean(exp60Curves[column][3:6]), np.nanmean(exp60Curves[column][6:9]), np.nanmean(exp60Curves[column][9:12]), np.nanmean(exp60Curves[column][81:90]), 'instructed', '60'])
        blockedCurvesIdx += 1
    blockedFinal = pd.concat([blockedFinal, blockedCurves])

    blockedFinal.to_csv('learningCurveAOVData.csv', header= True, index= False) ## Save learning curve data for AOV
    
    return blockedFinal

#%% normalized Curve Anova Data
def makeNormBlocked ():
    imp30Curves = pd.read_csv('imp30_curves.csv')
    exp30Curves = pd.read_csv('exp30_curves.csv')
    imp60Curves = pd.read_csv('imp60_curves.csv')
    exp60Curves = pd.read_csv('exp60_curves.csv')
    
    blockedCurves = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
    blockedCurvesIdx = 0
    blockedFinal = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
        
    for column in imp30Curves:
        #print (imp30Curves[column])
        blockedCurves.loc[blockedCurvesIdx] = ([imp30Curves.columns[blockedCurvesIdx], np.nanmean(imp30Curves[column][0:3])/30, np.nanmean(imp30Curves[column][3:6])/30, np.nanmean(imp30Curves[column][6:9])/30, np.nanmean(imp30Curves[column][9:12])/30, np.nanmean(imp30Curves[column][81:90])/30, 'non-instructed', '30'])
        blockedCurvesIdx += 1
    blockedFinal = pd.concat([blockedFinal, blockedCurves])
    
    blockedCurves = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
    blockedCurvesIdx = 0
    
    for column in exp30Curves:
        #print (imp30Curves[column])
        blockedCurves.loc[blockedCurvesIdx] = ([exp30Curves.columns[blockedCurvesIdx], np.nanmean(exp30Curves[column][0:3])/30, np.nanmean(exp30Curves[column][3:6])/30, np.nanmean(exp30Curves[column][6:9])/30, np.nanmean(exp30Curves[column][9:12])/30, np.nanmean(exp30Curves[column][81:90])/30, 'instructed', '30'])
        blockedCurvesIdx += 1
    blockedFinal = pd.concat([blockedFinal, blockedCurves])
    
    blockedCurves = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
    blockedCurvesIdx = 0
    
    for column in imp60Curves:
        #print (imp30Curves[column])
        blockedCurves.loc[blockedCurvesIdx] = ([imp60Curves.columns[blockedCurvesIdx], np.nanmean(imp60Curves[column][0:3])/60, np.nanmean(imp60Curves[column][3:6])/60, np.nanmean(imp60Curves[column][6:9])/60, np.nanmean(imp60Curves[column][9:12])/60, np.nanmean(imp60Curves[column][81:90])/60, 'non-instructed', '60'])
        blockedCurvesIdx += 1
    blockedFinal = pd.concat([blockedFinal, blockedCurves])
    
    blockedCurves = pd.DataFrame(columns = ['participant', 'block1mean', 'block2mean', 'block3mean', 'block4mean', 'finalblockmean', 'instruction', 'rotationSize'])
    blockedCurvesIdx = 0
    
    for column in exp60Curves:
        #print (imp30Curves[column])
        blockedCurves.loc[blockedCurvesIdx] = ([exp60Curves.columns[blockedCurvesIdx], np.nanmean(exp60Curves[column][0:3])/60, np.nanmean(exp60Curves[column][3:6])/60, np.nanmean(exp60Curves[column][6:9])/60, np.nanmean(exp60Curves[column][9:12])/60, np.nanmean(exp60Curves[column][81:90])/60, 'instructed', '60'])
        blockedCurvesIdx += 1
    blockedFinal = pd.concat([blockedFinal, blockedCurves])

    blockedFinal.to_csv('normLearningCurveAOVData.csv', header= True, index= False) ## Save learning curve data for AOV
    
    return blockedFinal


#%% Moke participant info csv (awareness scores, age, gender, etc.)
def makeAwarenessCSV (groups):
    rawInfoDF = pd.read_csv('participantInfo.csv')
    awarenessDF = pd.DataFrame()
    for group in groups:
        newInfoDF = rawInfoDF[rawInfoDF.filename.isin(names(group))][['filename', 'Age', 'Sex', 'group', 'version', 'Points']]
        awarenessDF = pd.concat([awarenessDF, newInfoDF])
    return awarenessDF    
        

def makeLocAwarenessCSV (group):
    
    infoDF = pd.read_csv('participantAwareness.csv')
    
    aeDF = pd.read_csv(group[0:5]+'_reachAEs_pp.csv')
    activeTapDF = pd.read_csv(group[0:5]+'_activeTapData.csv')
    passiveTapDF = pd.read_csv(group[0:5]+'_passiveTapData.csv')
    
    #add active_means
    aeDF['active_means']= activeTapDF[['50 deviation', '90 deviation', '130 deviation']].mean(1)
   
    #add prop_means
    aeDF['prop_means']= passiveTapDF[['50 deviation', '90 deviation', '130 deviation']].mean(1)

    #add pred_means
    aeDF['pred_means']= aeDF['active_means'] - aeDF['prop_means']
    
    awareness_score_ordered = []
    for participant in aeDF.participant:
        try:
            awareness_score_ordered.append(int(infoDF['Points'][infoDF.filename == participant]))
        except TypeError: 
            awareness_score_ordered.append(np.nan)

    
    aeDF['awareness_score'] = awareness_score_ordered
    #save CSV
    aeDF.to_csv(group[0:5] + '_locAwareness.csv', header= True, index= False) ## Save explicit stuff
    
#%% awareness CSV (doesn't neet to be redone unless changes to data files occur)

# makeAwarenessCSV(['imp30/', 'exp30/', 'imp60/', 'exp60/']).to_csv( 'participantAwareness.csv', header= True, index= False)
    
#%%testing

#==============================================================================
# participant = 'exp30/ca_0205/'
participant = 'imp30/bd_3105/'
group = 'imp30/'
# taskType = 'no_cursor'
# # np.array(trainAngMeans(readReachData(participant, '60', 'train'))) - np.array(baselineAngMeans(readReachData(participant, 'aligned', 'train'))) #average deviations for each target)
# # trainAngs(participant, 1, 91)
#==============================================================================

#for group in groups:
#    makeTrainingCSV(group)
#    makeTapCSVs(group)
#    makeAfterEffectCSV(group)
#    makeNonBLAfterEffectCSV(group)
#    makeLocAwarenessCSV(group)

#%% multiprocessed make csv files

groups = ['imp30/', 'exp30/', 'imp60/', 'exp60/']
group = 'imp30/'
#groups = ['cursorJump/']
blockedCurveData = makeBlocked()
normBlockedCurveData = makeNormBlocked() #need to be done first to make the awareness ratios

if __name__ == '__main__':
    __spec__ = None
    for group in groups:
        p1 = multiprocessing.Process(target= makeTrainingCSV, args=(group, ))
        p2 = multiprocessing.Process(target= makeTapCSVs, args=(group, ))
        p3 = multiprocessing.Process(target= makeAfterEffectCSV, args=(group, ))
        p4 = multiprocessing.Process(target= makeNonBLAfterEffectCSV, args=(group, ))
    
            
        p1.start()
        p2.start()
        p3.start()
        p4.start()       
            
        print ('Group {} is processing'.format(group))

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    for group in groups:
        p5 = multiprocessing.Process(target= makeLocAwarenessCSV, args=(group, ))
        p5.start()


    
#%% for blocked ANOVAs

#%% Making csv files

#==============================================================================
# #==============================================================================
# # groups = ['impAge/', 'expAge/']
# #==============================================================================
# for group in groups:
#     print(group)
#     makeTrainingCSV(group)
#     makeTapCSVs(group)
#     makeAfterEffectCSV(group)
# #blockedCurveData = makeBlocked()
# #normBlockedCurveData = makeNormBlocked()
# 
#==============================================================================


#%%Localization

#makeTapCSVs('exp30/')
# makeTapCSVs('exp60/')

#%%Localization Stats

# print('Implicit Passive Mean Deviation: ' + str(np.mean(pd.read_csv('processedImplicitTapData.csv')['passiveDeviation'])) + ' std: ' + str (pd.read_csv('processedImplicitTapData.csv')['passiveDeviation'].std()))
# print('Implicit Active Mean Deviation: ' + str(np.mean(pd.read_csv('processedImplicitTapData.csv')['activeDeviation'])) + ' std: ' + str (pd.read_csv('processedImplicitTapData.csv')['activeDeviation'].std()))
# print('Explicit Passive Mean Deviation: ' + str(np.mean(pd.read_csv('processedExplicitTapData.csv')['passiveDeviation'])) + ' std: ' + str (pd.read_csv('processedExplicitTapData.csv')['passiveDeviation'].std()))
# print('Explicit Active Mean Deviation: ' + str(np.mean(pd.read_csv('processedExplicitTapData.csv')['activeDeviation'])) + ' std: ' + str (pd.read_csv('processedExplicitTapData.csv')['activeDeviation'].std()))

# print('Passive t-test: ' + str(st.ttest_ind(pd.read_csv('processedImplicitTapData.csv')['passiveDeviation'], pd.read_csv('processedExplicitTapData.csv')['passiveDeviation'])))
# print('Active t-test: ' + str(st.ttest_ind(pd.read_csv('processedImplicitTapData.csv')['activeDeviation'], pd.read_csv('processedExplicitTapData.csv')['activeDeviation'])))

# #t-tests per participant
# print('Implicit Passive Mean Deviation (using means per participant): ' + str(np.mean(pd.read_csv('processedImplicitTapData_perParticipant.csv')['passiveDeviation'])) + ' std: ' + str (pd.read_csv('processedImplicitTapData_perParticipant.csv')['passiveDeviation'].std()))
# print('Implicit Active Mean Deviation (using means per participant): ' + str(np.mean(pd.read_csv('processedImplicitTapData_perParticipant.csv')['activeDeviation'])) + ' std: ' + str (pd.read_csv('processedImplicitTapData_perParticipant.csv')['activeDeviation'].std()))
# print('Explicit Passive Mean Deviation (using means per participant): ' + str(np.mean(pd.read_csv('processedExplicitTapData_perParticipant.csv')['passiveDeviation'])) + ' std: ' + str (pd.read_csv('processedExplicitTapData_perParticipant.csv')['passiveDeviation'].std()))
# print('Explicit Active Mean Deviation (using means per participant): ' + str(np.mean(pd.read_csv('processedExplicitTapData_perParticipant.csv')['activeDeviation'])) + ' std: ' + str (pd.read_csv('processedExplicitTapData_perParticipant.csv')['activeDeviation'].std()))

# print('Passive t-test (using means per partcipant): ' + str(st.ttest_ind(pd.read_csv('processedImplicitTapData_perParticipant.csv')['passiveDeviation'], pd.read_csv('processedExplicitTapData_perParticipant.csv')['passiveDeviation'])))
# print('Active t-test (using means per partcipant): ' + str(st.ttest_ind(pd.read_csv('processedImplicitTapData_perParticipant.csv')['activeDeviation'], pd.read_csv('processedExplicitTapData_perParticipant.csv')['activeDeviation'])))





