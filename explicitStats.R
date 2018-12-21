# set the working directory to wherever this file is located
this.dir <- dirname(parent.frame(2)$ofile)
setwd(this.dir)

# read in raw data files
library(ez)
#library(gplots)


loadTapData <- function() {
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
  colnames(all30Taps) <- c('deviation.50', 'deviation.90', 'deviation.130', 'reachType', 'participant', 'instruction')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  all30Taps <- reshape(all30Taps, direction="long", varying=c('deviation.50', 'deviation.90', 'deviation.130'), timevar='reachAngle', v.names='deviation', times=c('50', '90', '130'))
  
  # get rid of the id column and rownames after reshaping
  all30Taps$id <- NULL
  rownames(all30Taps) <- NULL
  
  #make the independent column a factor (see what factor does..)
  all30Taps$reachAngle <- factor(all30Taps$reachAngle, levels=c('50', '90', '130'))
  all30Taps$instruction <- factor(all30Taps$instruction, levels=c('instructed', 'non-instructed'))
  all30Taps$reachType <- factor(all30Taps$reachType, levels=c('active', 'passive'))
  
  
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
  colnames(all60Taps) <- c('deviation.50', 'deviation.90', 'deviation.130', 'reachType', 'participant', 'instruction')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  all60Taps <- reshape(all60Taps, direction="long", varying=c('deviation.50', 'deviation.90', 'deviation.130'), timevar='reachAngle', v.names='deviation', times=c('50', '90', '130'))
  
  # get rid of the id column and rownames after reshaping
  all60Taps$id <- NULL
  rownames(all60Taps) <- NULL
  
  #make the independent column a factor (see what factor does..)
  all60Taps$reachAngle <- factor(all60Taps$reachAngle, levels=c('50', '90', '130'))
  all60Taps$instruction <- factor(all60Taps$instruction, levels=c('instructed', 'non-instructed'))
  all60Taps$reachType <- factor(all60Taps$reachType, levels=c('active', 'passive'))
  
  #remove rows with Nans
  all30Taps <- all30Taps[complete.cases(all30Taps), ]
  all60Taps <- all60Taps[complete.cases(all60Taps), ]
  
  #Merging dataframes
  all30Taps$rotationSize <- '30'
  all60Taps$rotationSize <- '60'
  allTaps <- Reduce(function(x, y) merge(x, y, all=TRUE), list(all30Taps, all60Taps))
  

  allTaps$reachAngle <- factor(allTaps$reachAngle, levels=c('50', '90', '130'))
  allTaps$instruction <- factor(allTaps$instruction, levels=c('instructed', 'non-instructed'))
  allTaps$reachType <- factor(allTaps$reachType, levels=c('active', 'passive'))
  allTaps$rotationSize <- factor(allTaps$rotationSize, levels=c('30', '60'))
  # #ANOVA
  # all30AOV <- ezANOVA(data=all30Taps, dv=deviation, wid=participant, within=reachType, between=instruction, return_aov=TRUE, type=2)
  # print(all30AOV)
  # all60AOV <- ezANOVA(data=all60Taps, dv=deviation, wid=participant, within=reachType, between=instruction, return_aov=TRUE, type=2)
  # print(all60AOV)
  
  return(allTaps)
}

loadSessionTapData <- function() {
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
  colnames(allTaps) <- c('deviation.50', 'deviation.90', 'deviation.130', 'reachType', 'participant', 'instruction', 'session', 'rotationSize')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  allTaps <- reshape(allTaps, direction="long", varying=c('deviation.50', 'deviation.90', 'deviation.130'), timevar='reachAngle', v.names='deviation', times=c('50', '90', '130'))
  
  # get rid of the id column and rownames after reshaping
  allTaps$id <- NULL
  rownames(allTaps) <- NULL
  
  #make the independent column a factor (see what factor does..)
  allTaps$reachAngle <- factor(allTaps$reachAngle, levels=c('50', '90', '130'))
  allTaps$instruction <- factor(allTaps$instruction, levels=c('instructed', 'non-instructed'))
  allTaps$reachType <- factor(allTaps$reachType, levels=c('active', 'passive'))
  allTaps$rotationSize <- factor(allTaps$rotationSize, levels=c('30', '60'))
  allTaps$session <- factor(allTaps$session, levels=c('aligned', 'rotated'))

  
  return(allTaps)
}

loadReachData <- function() {
  curves <- read.csv('data/learningCurveAOVData.csv')
 
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(curves) <- c('participant', 'block1.1', 'block2.2', 'block3.3', 'instruction', 'rotationSize')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  curves <- reshape(curves, direction="long", varying=c('block1.1', 'block2.2', 'block3.3'), timevar='block', v.names='meanDeviation', times=c('block1', 'block2', 'finalblock'))
  
  # get rid of the id column and rownames after reshaping
  curves$id <- NULL
  rownames(curves) <- NULL
  
  #make the independent column a factor (see what factor does..)
  curves$block <- factor(curves$block, levels=c('block1', 'block2', 'finalblock'))
  curves$instruction <- factor(curves$instruction, levels=c('instructed', 'non-instructed'))
  curves$rotationSize <- factor(curves$rotationSize, levels=c('30', '60'))

  return(curves)
}

loadNormReachData <- function() {
  curves <- read.csv('data/normLearningCurveAOVData.csv')
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(curves) <- c('participant', 'block1.1', 'block2.2', 'block3.3', 'instruction', 'rotationSize')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  curves <- reshape(curves, direction="long", varying=c('block1.1', 'block2.2', 'block3.3'), timevar='block', v.names='meanDeviation', times=c('block1', 'block2', 'finalblock'))
  
  # get rid of the id column and rownames after reshaping
  curves$id <- NULL
  rownames(curves) <- NULL
  
  #make the independent column a factor (see what factor does..)
  curves$block <- factor(curves$block, levels=c('block1', 'block2', 'finalblock'))
  curves$instruction <- factor(curves$instruction, levels=c('instructed', 'non-instructed'))
  curves$rotationSize <- factor(curves$rotationSize, levels=c('30', '60'))

  return(curves)
}

loadAEData <- function() {
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
  allAE$rotationSize <- factor(allAE$rotationSize, levels=c('30', '60'))

  return(allAE)
}

loadLocAwareData <- function() {
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
  
  #get rid of columns we aren't testing
  # allLA$exclusive <- NULL
  # allLA$inclusive <- NULL
  # allLA$active_means <- NULL
  # allLA$group <- NULL
  
  allLA$instruction <- factor(allLA$instruction, levels=c('instructed', 'non-instructed'))
  allLA$rotationSize <- factor(allLA$rotationSize, levels=c('30', '60'))
  
  
  return (allLA)
}
#I THINK THIS NEEDS MANUAL CHANGING IF I WANT TO LOOK AT EARLY STUFF!
loadEarlyReachData <- function() {
  curves <- read.csv('data/learningCurveAOVData.csv')
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(curves) <- c('participant', 'block1.1', 'block2.2', 'block3.3', 'instruction', 'rotationSize')
  curves$block3.3 <- NULL
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  curves <- reshape(curves, direction="long", varying=c('block1.1', 'block2.2'), timevar='block', v.names='meanDeviation', times=c('block1', 'block2'))
  
  # get rid of the id column and rownames after reshaping
  curves$id <- NULL
  rownames(curves) <- NULL
  
  #make the independent column a factor (see what factor does..)
  curves$block <- factor(curves$block, levels=c('block1', 'block2'))
  curves$instruction <- factor(curves$instruction, levels=c('instructed', 'non-instructed'))
  curves$rotationSize <- factor(curves$rotationSize, levels=c('30', '60'))
  
  return(curves)
}
loadEarlyNormReachData <- function() {
  curves <- read.csv('data/normLearningCurveAOVData.csv')
  
  # reshape needs funky column names in the form: characters.number, for columns that need to be merged::
  colnames(curves) <- c('participant', 'block1.1', 'block2.2', 'block3.3', 'instruction', 'rotationSize')
  
  # reshape the plots so that ALL dependent variables are in one column (deviation for Tap data)
  curves <- reshape(curves, direction="long", varying=c('block1.1', 'block2.2', 'block3.3'), timevar='block', v.names='meanDeviation', times=c('block1', 'block2', 'block3'))
  
  # get rid of the id column and rownames after reshaping
  curves$id <- NULL
  rownames(curves) <- NULL
  
  #make the independent column a factor (see what factor does..)
  curves$block <- factor(curves$block, levels=c('block1', 'block2', 'block3'))
  curves$instruction <- factor(curves$instruction, levels=c('instructed', 'non-instructed'))
  curves$rotationSize <- factor(curves$rotationSize, levels=c('30', '60'))
  
  return(curves)
}

loadimplicitAEData <- function() {
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

#ANOVAS ----
allTaps <- loadTapData()
allAEs <- loadAEData()
allReaches <- loadReachData()
allNormReaches <- loadNormReachData()
allEarlyReaches <- loadEarlyReachData()
allEarlyNormReaches <- loadEarlyNormReachData()


#ANOVAs
tapsAOV <- ezANOVA(data=allTaps, dv=deviation, wid=participant, within=reachType, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
AEAOV <- ezANOVA(data=allAEs, dv=reachAE, wid=participant, within=stratUse, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
reachAOV <- ezANOVA(data=allReaches, dv=meanDeviation, wid=participant, within=block, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
normReachAOV <- ezANOVA(data=allNormReaches, dv=meanDeviation, wid=participant, within=block, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
earlyReachAOV <- ezANOVA(data=allEarlyReaches, dv=meanDeviation, wid=participant, within=block, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
earlyNormReachAOV <- ezANOVA(data=allEarlyNormReaches, dv=meanDeviation, wid=participant, within=block, between=.(instruction, rotationSize), return_aov=TRUE, type=3)


print(tapsAOV)
print(AEAOV)
print(reachAOV)
print(normReachAOV)
print(earlyReachAOV)
print(earlyNormReachAOV)

#Print the ANOVAs
tapsAOV$ANOVA$p <-format(round(tapsAOV$ANOVA$p, 3), nsmall = 2)
AEAOV$ANOVA$p <-format(round(AEAOV$ANOVA$p, 3), nsmall = 2)
reachAOV$ANOVA$p <-format(round(reachAOV$ANOVA$p, 3), nsmall = 2)
normReachAOV$ANOVA$p <-format(round(normReachAOV$ANOVA$p, 3), nsmall = 2)
earlyReachAOV$ANOVA$p <-format(round(earlyReachAOV$ANOVA$p, 3), nsmall = 2)
earlyNormReachAOV$ANOVA$p <-format(round(earlyNormReachAOV$ANOVA$p, 3), nsmall = 2)

print(tapsAOV$ANOVA)
print(AEAOV$ANOVA)
print(reachAOV$ANOVA)
print(normReachAOV$ANOVA)
print(earlyReachAOV$ANOVA)
print(earlyNormReachAOV$ANOVA)

#ANOVA on session tap data ----
sessionTaps <- loadSessionTapData()
sessionTapsAOV <- ezANOVA(data=sessionTaps, dv=deviation, wid=participant, within=.(reachType, session), return_aov=TRUE, type=3)
sessionTapsAOV$ANOVA$p <-format(round(sessionTapsAOV$ANOVA$p, 3), nsmall = 2)
sessionTapsAOV$ANOVA$F <-format(round(sessionTapsAOV$ANOVA$F, 4), nsmall = 2)
print(sessionTapsAOV$ANOVA)

#ANOVA on implicitAE data ----
implicitAEs <- loadimplicitAEData()
implicitAEAOV <- ezANOVA(data=implicitAEs, dv=reachAE, wid=participant, within=.(session), between=.(instruction, rotationSize), return_aov=TRUE, type=3)
implicitAEAOV$ANOVA$p <-format(round(implicitAEAOV$ANOVA$p, 3), nsmall = 2)
implicitAEAOV$ANOVA$F <-format(round(implicitAEAOV$ANOVA$F, 4), nsmall = 2)
print(implicitAEAOV$ANOVA)

#localization compared with awareness stuff----
allLA <- loadLocAwareData()
curves <- read.csv('data/learningCurveAOVData.csv')


#percentage/proportion of learning evoked in inclusive PDP reaches
#I30
paste('NI30 ', mean(allLA[allLA$rotationSize == '30' & allLA$instruction == 'non-instructed',]$inclusive)/mean(curves[curves$rotationSize == '30' & curves$instruction == 'non-instructed',]$finalblockmean))
paste('I30 ', mean(allLA[allLA$rotationSize == '30' & allLA$instruction == 'instructed',]$inclusive)/mean(curves[curves$rotationSize == '30' & curves$instruction == 'instructed',]$finalblockmean))
paste('NI60 ', mean(allLA[allLA$rotationSize == '60' & allLA$instruction == 'non-instructed',]$inclusive)/mean(curves[curves$rotationSize == '60' & curves$instruction == 'non-instructed',]$finalblockmean))
paste('I60 ', mean(allLA[allLA$rotationSize == '60' & allLA$instruction == 'instructed',]$inclusive)/mean(curves[curves$rotationSize == '60' & curves$instruction == 'instructed',]$finalblockmean))


#One-sample t-tests 
t.test(allLA[allLA$rotationSize == '30' & allLA$instruction == 'non-instructed',]$awarenessRatio, alternative="greater", mu=0.5)
t.test(allLA[allLA$rotationSize == '30' & allLA$instruction == 'instructed',]$awarenessRatio, alternative="greater", mu=0.5)
t.test(allLA[allLA$rotationSize == '60' & allLA$instruction == 'non-instructed',]$awarenessRatio, alternative="greater", mu=0.5)
t.test(allLA[allLA$rotationSize == '60' & allLA$instruction == 'instructed',]$awarenessRatio, alternative="greater", mu=0.5)

sd(allLA[allLA$rotationSize == '30' & allLA$instruction == 'non-instructed',]$awarenessRatio)
sd(allLA[allLA$rotationSize == '30' & allLA$instruction == 'instructed',]$awarenessRatio)
sd(allLA[allLA$rotationSize == '60' & allLA$instruction == 'non-instructed',]$awarenessRatio)
sd(allLA[allLA$rotationSize == '60' & allLA$instruction == 'instructed',]$awarenessRatio)

#ANOVA for awareness ratio
awarenessRatioAOV <- ezANOVA(data=allLA, dv=awarenessRatio, wid=participant, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
awarenessRatioAOV$ANOVA$p <-format(round(awarenessRatioAOV$ANOVA$p, 3), nsmall = 2)
print(awarenessRatioAOV$ANOVA)

#means and sd (and t-test??)
mean(allLA[allLA$instruction == 'instructed',]$awarenessRatio)
sd(allLA[allLA$instruction == 'instructed',]$awarenessRatio)
mean(allLA[allLA$instruction == 'non-instructed',]$awarenessRatio)
sd(allLA[allLA$instruction == 'non-instructed',]$awarenessRatio)
t.test(allLA[allLA$instruction == 'instructed',]$awarenessRatio, allLA[allLA$instruction == 'non-instructed',]$awarenessRatio)

mean(allLA[allLA$rotationSize == '30',]$awarenessRatio)
sd(allLA[allLA$rotationSize == '30',]$awarenessRatio)
mean(allLA[allLA$rotationSize == '60',]$awarenessRatio)
sd(allLA[allLA$rotationSize == '60',]$awarenessRatio)
t.test(allLA[allLA$rotationSize == '30',]$awarenessRatio, allLA[allLA$rotationSize == '60',]$awarenessRatio)



#correlations for awareness ratio and scores
cor.test(allLA$awareness_score, allLA$prop_means, method= "spearman") #spearman ranks data. better for ordinal data
plot(allLA$awareness_score, allLA$prop_means, main="Scatterplot",
     xlab="Awareness Score ", ylab="Proprioceptive Recalibration ") 
abline(lm(allLA$prop_means~allLA$awareness_score), col="red") #y~x

cor.test(allLA$awareness_score, allLA$pred_means, method= "spearman")
plot(allLA$awareness_score, allLA$pred_means, main="Scatterplot",
     xlab="Awareness Score ", ylab="Efferent Based Changes in Localization ") 
abline(lm(allLA$pred_means~allLA$awareness_score), col="red") #y~x


cor.test(allLA$awarenessRatio, allLA$prop_means)
plot(allLA$awarenessRatio, allLA$prop_means, main="Scatterplot",
     xlab="Awareness Ratio ", ylab="Proprioceptive Recalibration ") 
abline(lm(allLA$prop_means~allLA$awarenessRatio), col="red") #y~x

cor.test(allLA$awarenessRatio, allLA$pred_means)
plot(allLA$awarenessRatio, allLA$pred_means, main="Scatterplot",
     xlab="Awareness Ratio ", ylab="Efferent Based Changes in Localization ") 
abline(lm(allLA$pred_means~allLA$awarenessRatio), col="red") #y~x


#awareness within all participants
print('awareness in all participants')
cor.test(allLA$awarenessRatio, allLA$awareness_score, method= "spearman")
plot(allLA$awarenessRatio, allLA$awareness_score, main="Scatterplot",
     xlab="Strategy Use Ratio", ylab="Questionnaire Score") 
abline(lm(allLA$awareness_score~allLA$awarenessRatio), col="red") #y~x

#awareness within groups
print('Within group awareness')
cor.test(allLA[allLA$rotationSize == '30'& allLA$instruction == 'non-instructed' ,]$awarenessRatio, allLA[allLA$rotationSize == '30'& allLA$instruction == 'non-instructed',]$awareness_score, method= "spearman")
plot(allLA[allLA$rotationSize == '30'& allLA$instruction == 'non-instructed' ,]$awarenessRatio, allLA[allLA$rotationSize == '30'& allLA$instruction == 'non-instructed' ,]$awareness_score, main="Scatterplot",
     xlab="Strategy Use Ratio", ylab="Questionnaire Score") 
abline(lm(allLA[allLA$rotationSize == '30'& allLA$instruction == 'non-instructed' ,]$awareness_score~allLA[allLA$rotationSize == '30'& allLA$instruction == 'non-instructed' ,]$awarenessRatio), col="red") #y~x

cor.test(allLA[allLA$rotationSize == '30'& allLA$instruction == 'instructed' ,]$awarenessRatio, allLA[allLA$rotationSize == '30'& allLA$instruction == 'instructed',]$awareness_score, method= "spearman")
plot(allLA[allLA$rotationSize == '30'& allLA$instruction == 'instructed' ,]$awarenessRatio, allLA[allLA$rotationSize == '30'& allLA$instruction == 'instructed' ,]$awareness_score, main="Scatterplot",
     xlab="Strategy Use Ratio", ylab="Questionnaire Score") 
abline(lm(allLA[allLA$rotationSize == '30'& allLA$instruction == 'instructed' ,]$awareness_score~allLA[allLA$rotationSize == '30'& allLA$instruction == 'instructed' ,]$awarenessRatio), col="red") #y~x

cor.test(allLA[allLA$rotationSize == '60'& allLA$instruction == 'non-instructed' ,]$awarenessRatio, allLA[allLA$rotationSize == '60'& allLA$instruction == 'non-instructed',]$awareness_score, method= "spearman")
plot(allLA[allLA$rotationSize == '60'& allLA$instruction == 'non-instructed' ,]$awarenessRatio, allLA[allLA$rotationSize == '60'& allLA$instruction == 'non-instructed' ,]$awareness_score, main="Scatterplot",
     xlab="Strategy Use Ratio", ylab="Questionnaire Score") 
abline(lm(allLA[allLA$rotationSize == '60'& allLA$instruction == 'non-instructed' ,]$awareness_score~allLA[allLA$rotationSize == '60'& allLA$instruction == 'non-instructed' ,]$awarenessRatio), col="red") #y~x

cor.test(allLA[allLA$rotationSize == '60'& allLA$instruction == 'instructed' ,]$awarenessRatio, allLA[allLA$rotationSize == '60'& allLA$instruction == 'instructed',]$awareness_score, method= "spearman")
plot(allLA[allLA$rotationSize == '60'& allLA$instruction == 'instructed' ,]$awarenessRatio, allLA[allLA$rotationSize == '60'& allLA$instruction == 'instructed' ,]$awareness_score, main="Scatterplot",
     xlab="Strategy Use Ratio", ylab="Questionnaire Score") 
abline(lm(allLA[allLA$rotationSize == '60'& allLA$instruction == 'instructed' ,]$awareness_score~allLA[allLA$rotationSize == '60'& allLA$instruction == 'instructed' ,]$awarenessRatio), col="red") #y~x


cor.test(allLA$inclusive, allLA$prop_means)
cor.test(allLA$inclusive, allLA$pred_means)

cor.test(allLA$exclusive, allLA$prop_means)
cor.test(allLA$exclusive, allLA$pred_means)

plot(allLA$exclusive, allLA$prop_means, main="Scatterplot",
     xlab="Aftereffects w/o Strategy ", ylab="Proprioceptive Recalibration ") 
abline(lm(allLA$prop_means~allLA$exclusive), col="red") #y~x

# #trying some outlier removal
# allLA <- allLA[-c(23), ]   


library(Hmisc)
rc1 <- rcorr(allLA$awareness_score, allLA$prop_means, type="pearson")
print (rc1$r, digits = 10)
rc1

rc2 <- rcorr(allLA$awareness_score, allLA$pred_means, type="pearson")
print (rc2$r, digits = 10)
rc2

rc3 <- rcorr(allLA$awarenessRatio, allLA$prop_means, type="pearson")
print (rc3$r, digits = 10)
rc3

rc4 <- rcorr(allLA$awarenessRatio, allLA$pred_means, type="pearson")
print (rc4$r, digits = 10)
rc4


#2x2 ANOVA for blocks----
#block 1
curves <- read.csv('data/normLearningCurveAOVData.csv')
# reshape needs funky column names in the form: characters.number, for columns that need to be merged::

curves$instruction <- factor(curves$instruction, levels=c('instructed', 'non-instructed'))
curves$rotationSize <- factor(curves$rotationSize, levels=c('30', '60'))

block1AOV <- ezANOVA(data=curves, dv=block1mean, wid=participant, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
block1AOV$ANOVA$p <-format(round(block1AOV$ANOVA$p, 3), nsmall = 2)

block2AOV <- ezANOVA(data=curves, dv=block2mean, wid=participant, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
block2AOV$ANOVA$p <-format(round(block2AOV$ANOVA$p, 3), nsmall = 2)

block3AOV <- ezANOVA(data=curves, dv=block3mean, wid=participant, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
block3AOV$ANOVA$p <-format(round(block3AOV$ANOVA$p, 3), nsmall = 2)

block4AOV <- ezANOVA(data=curves, dv=block4mean, wid=participant, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
block4AOV$ANOVA$p <-format(round(block4AOV$ANOVA$p, 3), nsmall = 2)

finalblockAOV <- ezANOVA(data=curves, dv=finalblockmean, wid=participant, between=.(instruction, rotationSize), return_aov=TRUE, type=3)
finalblockAOV$ANOVA$p <-format(round(finalblockAOV$ANOVA$p, 3), nsmall = 2)


#print all 2x2 learning curve ANOVAs
print(block1AOV$ANOVA)
print(block2AOV$ANOVA)
print(block3AOV$ANOVA)
print(block4AOV$ANOVA)
print(finalblockAOV$ANOVA)

#Cohen's D for blocks between instructed and non-instructed
library(effsize)

cohen.d(curves$block1mean, f=curves$instruction, na.rm=TRUE)
cohen.d(curves$block2mean, f=curves$instruction, na.rm=TRUE)
cohen.d(curves$finalblockmean, f=curves$instruction, na.rm=TRUE)

#means for localization/taps----

allActiveTaps <- allTaps[allTaps$reachType == 'active',]
allPassiveTaps <- allTaps[allTaps$reachType == 'passive',]

mean(allActiveTaps$deviation)
mean(allPassiveTaps$deviation)
mean(allActiveTaps$deviation) - mean(allPassiveTaps$deviation)

sd(allActiveTaps$deviation)
sd(allPassiveTaps$deviation)
sd(allActiveTaps$deviation) - sd(allPassiveTaps$deviation)
