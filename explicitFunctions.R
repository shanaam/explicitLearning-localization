# set the working directory to wherever this file is located
this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

# read in raw data files
library(ez)
#library(gplots)

# Adaptation data
LoadReachData <- function() {
  curves <- read.csv('data/learningCurveAOVData.csv')
 
  curves$block3mean <- NULL
  curves$block4mean <- NULL
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(curves) <- c('participant', 'trialSet1.1', 'trialSet2.2', 'trialSetFinal.3', 'instruction', 'rotationSize')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  curves <- reshape(curves, direction="long", varying=c('trialSet1.1', 'trialSet2.2', 'trialSetFinal.3'), timevar='trialSet', v.names='meanDeviation', times=c('trialSet1', 'trialSet2', 'finaltrialSet'))
  
  # get rid of the id column and rownames after reshaping
  curves$id <- NULL
  rownames(curves) <- NULL
  
  #make the independent column a factor (see what factor does..)
  curves$trialSet <- factor(curves$trialSet, levels=c('trialSet1', 'trialSet2', 'finaltrialSet'))
  curves$instruction <- factor(curves$instruction, levels=c('instructed', 'non-instructed'))
  curves$rotationSize <- factor(curves$rotationSize, levels=c('30', '60'))

  return(curves)
}

LoadNormReachData <- function() {
  curves <- read.csv('data/normLearningCurveAOVData.csv')
  
  curves$block3mean <- NULL
  curves$block4mean <- NULL
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(curves) <- c('participant', 'trialSet1.1', 'trialSet2.2', 'trialSetFinal.3', 'instruction', 'rotationSize')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  curves <- reshape(curves, direction="long", varying=c('trialSet1.1', 'trialSet2.2', 'trialSetFinal.3'), timevar='trialSet', v.names='meanDeviation', times=c('trialSet1', 'trialSet2', 'finaltrialSet'))
  
  # get rid of the id column and rownames after reshaping
  curves$id <- NULL
  rownames(curves) <- NULL
  
  #make the independent column a factor (see what factor does..)
  curves$trialSet <- factor(curves$trialSet, levels=c('trialSet1', 'trialSet2', 'finaltrialSet'))
  curves$instruction <- factor(curves$instruction, levels=c('instructed', 'non-instructed'))
  curves$rotationSize <- factor(curves$rotationSize, levels=c('30', '60'))

  return(curves)
}


# Aftereffects data
LoadAEData <- function() {
  imp30AE <- read.csv('data/imp30_reachAEs_pp.csv')
  exp30AE <- read.csv('data/exp30_reachAEs_pp.csv')
  imp60AE <- read.csv('data/imp60_reachAEs_pp.csv')
  exp60AE <- read.csv('data/exp60_reachAEs_pp.csv')
    
  exp30AE$instruction <- 'instructed'
  imp30AE$instruction <- 'non-instructed'
  exp60AE$instruction <- 'instructed'
  imp60AE$instruction <- 'non-instructed'
  
  all30AE <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp30AE, exp30AE))
  all60AE <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp60AE, exp60AE))

  all30AE$rotationSize <- '30'
  all60AE$rotationSize <- '60'
  
  allAE <- Reduce(function(x, y) merge(x, y, all=TRUE), list(all30AE, all60AE))
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(allAE) <- c('participant', 'AEwithoutStrat.1', 'AEwithStrat.2', 'awarenessRatio', 'instruction', 'rotationSize')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  allAE <- reshape(allAE, direction="long", varying=c('AEwithoutStrat.1', 'AEwithStrat.2'), timevar='stratUse', v.names='reachAE', times=c('without','with'))
  
  # get rid of the id column and rownames after reshaping
  allAE$id <- NULL
  allAE$awarenessRatio <- NULL
  rownames(allAE) <- NULL
  
  #make the independent column a factor (see what factor does..)
  allAE$rotationSize <- factor(allAE$rotationSize, levels=c('30', '60'))
  allAE$instruction <- factor(allAE$instruction, levels=c('instructed', 'non-instructed'))
  allAE$stratUse <- factor(allAE$stratUse, levels=c('without', 'with'))

  return(allAE)
}

LoadAEData_NoBLCorr <- function() {
  imp30AE <- read.csv('data/imp30_sessionAEs_pp.csv')
  exp30AE <- read.csv('data/exp30_sessionAEs_pp.csv')
  imp60AE <- read.csv('data/imp60_sessionAEs_pp.csv')
  exp60AE <- read.csv('data/exp60_sessionAEs_pp.csv')
  
  exp30AE$instruction <- 'instructed'
  imp30AE$instruction <- 'non-instructed'
  exp60AE$instruction <- 'instructed'
  imp60AE$instruction <- 'non-instructed'
  
  all30AE <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp30AE, exp30AE))
  all60AE <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp60AE, exp60AE))
  
  all30AE$rotationSize <- '30'
  all60AE$rotationSize <- '60'
  
  allAE <- Reduce(function(x, y) merge(x, y, all=TRUE), list(all30AE, all60AE))
  
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(allAE) <- c('participant', 'AEaligned.1', 'AErotatedWithout.2', 'instruction', 'rotationSize')

  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  allAE <- reshape(allAE, direction="long", varying=c('AEaligned.1', 'AErotatedWithout.2'), timevar='session', v.names='reachAE', times=c('aligned','rotatedWithout'))

  # get rid of the id column and rownames after reshaping
  allAE$id <- NULL
  rownames(allAE) <- NULL

  #make the independent column a factor 
  allAE$rotationSize <- factor(allAE$rotationSize, levels=c('30', '60'))
  allAE$instruction <- factor(allAE$instruction, levels=c('instructed', 'non-instructed'))
  allAE$stratUse <- factor(allAE$session, levels=c('aligned', 'rotatedWithout'))
  
  return(allAE)
}


### What is this for???
LoadImplicitAEData <- function() {
  imp30AE <- read.csv('data/imp30_implicitAEs_pp.csv')
  exp30AE <- read.csv('data/exp30_implicitAEs_pp.csv')
  imp60AE <- read.csv('data/imp60_implicitAEs_pp.csv')
  exp60AE <- read.csv('data/exp60_implicitAEs_pp.csv')
  
  exp30AE$instruction <- 'instructed'
  imp30AE$instruction <- 'non-instructed'
  exp60AE$instruction <- 'instructed'
  imp60AE$instruction <- 'non-instructed'
  
  all30AE <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp30AE, exp30AE))
  all60AE <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp60AE, exp60AE))
  
  all30AE$rotationSize <- '30'
  all60AE$rotationSize <- '60'
  
  allAE <- Reduce(function(x, y) merge(x, y, all=TRUE), list(all30AE, all60AE))
  
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(allAE) <- c('participant', 'AEaligned.1', 'AErotated.2', 'instruction', 'rotationSize')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  allAE <- reshape(allAE, direction="long", varying=c('AEaligned.1', 'AErotated.2'), timevar='session', v.names='reachAE', times=c('aligned','rotated'))
  
  # get rid of the id column and rownames after reshaping
  allAE$id <- NULL
  rownames(allAE) <- NULL
  
  #make the independent column a factor (see what factor does..)
  allAE$rotationSize <- factor(allAE$rotationSize, levels=c('30', '60'))
  allAE$instruction <- factor(allAE$instruction, levels=c('instructed', 'non-instructed'))
  allAE$session <- factor(allAE$session, levels=c('aligned', 'rotated'))
  
  return(allAE)
}


# Localization data
LoadLocData <- function() {
  exp30actTap <- read.csv('data/exp30_activeTapData.csv')
  imp30actTap <- read.csv('data/imp30_activeTapData.csv')
  exp30passTap <- read.csv('data/exp30_passiveTapData.csv')
  imp30passTap <- read.csv('data/imp30_passiveTapData.csv')
  
  exp30Taps <- Reduce(function(x, y) merge(x, y, all=TRUE), list(exp30actTap, exp30passTap))
  # exp30Taps <- exp30passTap #this line is ONLY a fix for passive loc. data.
  exp30Taps$instruction <- 'instructed'
  imp30Taps <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp30actTap, imp30passTap))
  # imp30Taps <- imp30passTap #this line is ONLY a fix for passive loc. data.
  imp30Taps$instruction <- 'non-instructed'
  
  all30Taps <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp30Taps, exp30Taps))
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(all30Taps) <- c('deviation.50', 'deviation.90', 'deviation.130', 'movementType', 'participant', 'instruction')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  all30Taps <- reshape(all30Taps, direction="long", varying=c('deviation.50', 'deviation.90', 'deviation.130'), timevar='reachAngle', v.names='deviation', times=c('50', '90', '130'))
  
  # get rid of the id column and rownames after reshaping
  all30Taps$id <- NULL
  rownames(all30Taps) <- NULL
  
  #make the independent column a factor (see what factor does..)
  all30Taps$reachAngle <- factor(all30Taps$reachAngle, levels=c('50', '90', '130'))
  all30Taps$instruction <- factor(all30Taps$instruction, levels=c('instructed', 'non-instructed'))
  all30Taps$movementType <- factor(all30Taps$movementType, levels=c('active', 'passive'))
  
  
  #load 60
  exp60actTap <- read.csv('data/exp60_activeTapData.csv')
  imp60actTap <- read.csv('data/imp60_activeTapData.csv')
  exp60passTap <- read.csv('data/exp60_passiveTapData.csv')
  imp60passTap <- read.csv('data/imp60_passiveTapData.csv')
  
  exp60Taps <- Reduce(function(x, y) merge(x, y, all=TRUE), list(exp60actTap, exp60passTap))
  # exp60Taps <- exp60passTap #this line is ONLY a fix for passive loc. data.
  exp60Taps$instruction <- 'instructed'
  imp60Taps <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp60actTap, imp60passTap))
  # imp60Taps <- imp60passTap #this line is ONLY a fix for passive loc. data.
  imp60Taps$instruction <- 'non-instructed'
  
  all60Taps <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp60Taps, exp60Taps))
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(all60Taps) <- c('deviation.50', 'deviation.90', 'deviation.130', 'movementType', 'participant', 'instruction')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  all60Taps <- reshape(all60Taps, direction="long", varying=c('deviation.50', 'deviation.90', 'deviation.130'), timevar='reachAngle', v.names='deviation', times=c('50', '90', '130'))
  
  # get rid of the id column and rownames after reshaping
  all60Taps$id <- NULL
  rownames(all60Taps) <- NULL
  
  #make the independent column a factor (see what factor does..)
  all60Taps$reachAngle <- factor(all60Taps$reachAngle, levels=c('50', '90', '130'))
  all60Taps$instruction <- factor(all60Taps$instruction, levels=c('instructed', 'non-instructed'))
  all60Taps$movementType <- factor(all60Taps$movementType, levels=c('active', 'passive'))
  
  #remove rows with Nans
  all30Taps <- all30Taps[complete.cases(all30Taps), ]
  all60Taps <- all60Taps[complete.cases(all60Taps), ]
  
  #Merging dataframes
  all30Taps$rotationSize <- '30'
  all60Taps$rotationSize <- '60'
  allTaps <- Reduce(function(x, y) merge(x, y, all=TRUE), list(all30Taps, all60Taps))
  
  
  allTaps$reachAngle <- factor(allTaps$reachAngle, levels=c('50', '90', '130'))
  allTaps$instruction <- factor(allTaps$instruction, levels=c('instructed', 'non-instructed'))
  allTaps$movementType <- factor(allTaps$movementType, levels=c('active', 'passive'))
  allTaps$rotationSize <- factor(allTaps$rotationSize, levels=c('30', '60'))
  # #ANOVA
  # all30AOV <- ezANOVA(data=all30Taps, dv=deviation, wid=participant, within=movementType, between=instruction, return_aov=TRUE, type=2)
  # print(all30AOV)
  # all60AOV <- ezANOVA(data=all60Taps, dv=deviation, wid=participant, within=movementType, between=instruction, return_aov=TRUE, type=2)
  # print(all60AOV)
  
  return(allTaps)
}

LoadSessionLocData <- function() {
  #load 30 aligned
  exp30actTap_a <- read.csv('data/exp30_activeTapData_aligned.csv')
  imp30actTap_a <- read.csv('data/imp30_activeTapData_aligned.csv')
  exp30passTap_a <- read.csv('data/exp30_passiveTapData_aligned.csv')
  imp30passTap_a <- read.csv('data/imp30_passiveTapData_aligned.csv')
  
  exp30Taps_a <- Reduce(function(x, y) merge(x, y, all=TRUE), list(exp30actTap_a, exp30passTap_a))
  # exp30Taps <- exp30passTap #this line is ONLY a fix for passive loc. data.
  exp30Taps_a$instruction <- 'instructed'
  imp30Taps_a <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp30actTap_a, imp30passTap_a))
  # imp30Taps <- imp30passTap #this line is ONLY a fix for passive loc. data.
  imp30Taps_a$instruction <- 'non-instructed'
  
  all30Taps_a <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp30Taps_a, exp30Taps_a))
  all30Taps_a$session <- 'aligned'
  
  #load 30 rotated
  exp30actTap_r <- read.csv('data/exp30_activeTapData_rotated.csv')
  imp30actTap_r <- read.csv('data/imp30_activeTapData_rotated.csv')
  exp30passTap_r <- read.csv('data/exp30_passiveTapData_rotated.csv')
  imp30passTap_r <- read.csv('data/imp30_passiveTapData_rotated.csv')
  
  exp30Taps_r <- Reduce(function(x, y) merge(x, y, all=TRUE), list(exp30actTap_r, exp30passTap_r))
  # exp30Taps <- exp30passTap #this line is ONLY a fix for passive loc. data.
  exp30Taps_r$instruction <- 'instructed'
  imp30Taps_r <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp30actTap_r, imp30passTap_r))
  # imp30Taps <- imp30passTap #this line is ONLY a fix for passive loc. data.
  imp30Taps_r$instruction <- 'non-instructed'
  
  all30Taps_r <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp30Taps_r, exp30Taps_r))
  all30Taps_r$session <- 'rotated'
  
  #load 60 aligned
  exp60actTap_a <- read.csv('data/exp60_activeTapData_aligned.csv')
  imp60actTap_a <- read.csv('data/imp60_activeTapData_aligned.csv')
  exp60passTap_a <- read.csv('data/exp60_passiveTapData_aligned.csv')
  imp60passTap_a <- read.csv('data/imp60_passiveTapData_aligned.csv')
  
  exp60Taps_a <- Reduce(function(x, y) merge(x, y, all=TRUE), list(exp60actTap_a, exp60passTap_a))
  # exp60Taps <- exp60passTap #this line is ONLY a fix for passive loc. data.
  exp60Taps_a$instruction <- 'instructed'
  imp60Taps_a <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp60actTap_a, imp60passTap_a))
  # imp60Taps <- imp60passTap #this line is ONLY a fix for passive loc. data.
  imp60Taps_a$instruction <- 'non-instructed'
  
  all60Taps_a <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp60Taps_a, exp60Taps_a))
  all60Taps_a$session <- 'aligned'
  
  #load 60 rotated
  exp60actTap_r <- read.csv('data/exp60_activeTapData_rotated.csv')
  imp60actTap_r <- read.csv('data/imp60_activeTapData_rotated.csv')
  exp60passTap_r <- read.csv('data/exp60_passiveTapData_rotated.csv')
  imp60passTap_r <- read.csv('data/imp60_passiveTapData_rotated.csv')
  
  exp60Taps_r <- Reduce(function(x, y) merge(x, y, all=TRUE), list(exp60actTap_r, exp60passTap_r))
  # exp60Taps <- exp60passTap #this line is ONLY a fix for passive loc. data.
  exp60Taps_r$instruction <- 'instructed'
  imp60Taps_r <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp60actTap_r, imp60passTap_r))
  # imp60Taps <- imp60passTap #this line is ONLY a fix for passive loc. data.
  imp60Taps_r$instruction <- 'non-instructed'
  
  all60Taps_r <- Reduce(function(x, y) merge(x, y, all=TRUE), list(imp60Taps_r, exp60Taps_r))
  all60Taps_r$session <- 'rotated'
  
  
  #Merging dataframes
  all30Taps_a$rotationSize <- '30'
  all60Taps_a$rotationSize <- '60'
  all30Taps_r$rotationSize <- '30'
  all60Taps_r$rotationSize <- '60'
  
  allTaps <- Reduce(function(x, y) merge(x, y, all=TRUE), list(all30Taps_a, all60Taps_a, all30Taps_r, all60Taps_r))
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(allTaps) <- c('deviation.50', 'deviation.90', 'deviation.130', 'movementType', 'participant', 'instruction', 'session', 'rotationSize')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  allTaps <- reshape(allTaps, direction="long", varying=c('deviation.50', 'deviation.90', 'deviation.130'), timevar='reachAngle', v.names='deviation', times=c('50', '90', '130'))
  
  # get rid of the id column and rownames after reshaping
  allTaps$id <- NULL
  rownames(allTaps) <- NULL
  
  #make the independent column a factor (see what factor does..)
  allTaps$reachAngle <- factor(allTaps$reachAngle, levels=c('50', '90', '130'))
  allTaps$instruction <- factor(allTaps$instruction, levels=c('instructed', 'non-instructed'))
  allTaps$movementType <- factor(allTaps$movementType, levels=c('active', 'passive'))
  allTaps$rotationSize <- factor(allTaps$rotationSize, levels=c('30', '60'))
  allTaps$session <- factor(allTaps$session, levels=c('aligned', 'rotated'))
  
  
  return(allTaps)
}


# Means and such
LoadLocAwareData <- function() {
  imp30LA <- read.csv('data/imp30_locAwareness.csv')
  exp30LA <- read.csv('data/exp30_locAwareness.csv')
  imp60LA <- read.csv('data/imp60_locAwareness.csv')
  exp60LA <- read.csv('data/exp60_locAwareness.csv')
  
  imp30LA$instruction <- 'non-instructed' #might want to split these up. for now, I am not going to care about the groups
  exp30LA$instruction <- 'instructed'
  imp60LA$instruction <- 'non-instructed'
  exp60LA$instruction <- 'instructed'
  
  imp30LA$rotationSize <- '30' #might want to split these up. for now, I am not going to care about the groups
  exp30LA$rotationSize <- '30'
  imp60LA$rotationSize <- '60'
  exp60LA$rotationSize <- '60'

  all30LA <- Reduce(function(a, b) merge(a, b, all=TRUE), list(imp30LA, exp30LA))
  all60LA <- Reduce(function(a, b) merge(a, b, all=TRUE), list(imp60LA, exp60LA))
  allLA <- Reduce(function(a, b) merge(a, b, all=TRUE), list(all30LA, all60LA))
  
  # correct the scores for 3 outcomes (0,1,3 --> 0, 1, 2)
  allLA$awareness_score[allLA$awareness_score == 3] <- 2
  
  #get rid of columns we aren't testing
  # allLA$exclusive <- NULL
  # allLA$inclusive <- NULL
  # allLA$active_means <- NULL
  # allLA$group <- NULL
  
  allLA$instruction <- factor(allLA$instruction, levels=c('instructed', 'non-instructed'))
  allLA <- within(allLA, instruction <- relevel(instruction, ref = 'non-instructed'))
  allLA$rotationSize <- factor(allLA$rotationSize, levels=c('30', '60'))
  allLA <- within(allLA, rotationSize <- relevel(rotationSize, ref = '30'))
  allLA$awareness_score <- factor(allLA$awareness_score, levels=c('0', '1', '2'))

  
  return (allLA)
}
