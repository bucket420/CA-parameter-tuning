# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 -s RAW2DIGI:RawToDigi_pixelOnly,RECO:reconstruction_pixelTrackingOnly,VALIDATION:@pixelTrackingOnlyValidation,DQM:@pixelTrackingOnlyDQM --conditions auto:phase1_2022_realistic --datatier GEN-SIM-RECO,DQMIO -n 100 --eventcontent RECOSIM,DQM --geometry DB:Extended --era Run3 --procModifiers pixelNtupletFit,gpu --filein file:step2.root --fileout file:step3.root --nThreads 8
import FWCore.ParameterSet.Config as cms
from utils import read_csv,new_names

from Configuration.Eras.Era_Run3_pp_on_PbPb_cff import Run3_pp_on_PbPb
from Configuration.ProcessModifiers.pixelNtupletFit_cff import pixelNtupletFit
from Configuration.ProcessModifiers.gpu_cff import gpu

# import VarParsing
from FWCore.ParameterSet.VarParsing import VarParsing

# VarParsing instance
options = VarParsing('analysis')

# Custom options
options.register('parametersFile',
              'default/default_params.csv',
              VarParsing.multiplicity.singleton,
              VarParsing.varType.string,
              'Name of parameters file')

options.register('nEvents',
              100,
              VarParsing.multiplicity.singleton,
              VarParsing.varType.int,
              'Number of events')

# options.register('inputFile',
#               'file:input/step2.root',
#               VarParsing.multiplicity.singleton,
#               VarParsing.varType.string,
#               'Name of input file')

options.parseArguments()

process = cms.Process('RECOX',Run3_pp_on_PbPb,pixelNtupletFit,gpu)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
#process.load('Configuration.StandardSequences.RawToDigi_cff')
#process.load('Configuration.StandardSequences.Reconstruction_cff')
#process.load('Configuration.StandardSequences.Validation_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load( 'HLTrigger.Timer.FastTimerService_cfi' )
# process.load('HLTrigger.Configuration.HLT_2023v12_cff') #no doublet recovery
process.load('HLTrigger.Configuration.HLT_FULL_cff') #with doublet recovery



## All the modules excepted the pixel tracks (that we want to tune) 
## ONLY FOR GPU
process.HLTIterativeTrackingWithDoubletRecovery = cms.Sequence( 
    process.hltPixelTracksGPU + 
    process.hltPixelTracksFromGPU + 
    process.hltPixelTracks + 
    process.hltPixelTracksTrackingRegions +
    process.hltPixelVerticesGPU + 
    process.hltPixelVerticesFromGPU + 
    process.hltPixelVertices + 
    process.hltTrimmedPixelVertices + 
    process.hltIter0PFLowPixelSeedsFromPixelTracks + 
    process.hltIter0PFlowCkfTrackCandidates + 
    process.hltIter0PFlowCtfWithMaterialTracks + 
    process.hltIter0PFlowTrackCutClassifier + 
    process.hltIter0PFlowTrackSelectionHighPurity +
    process.hltDoubletRecoveryClustersRefRemoval + 
    process.hltDoubletRecoveryMaskedMeasurementTrackerEvent + 
    process.hltDoubletRecoveryPixelLayersAndRegions + 
    process.hltDoubletRecoveryPFlowPixelClusterCheck + 
    process.hltDoubletRecoveryPFlowPixelHitDoublets + 
    process.hltDoubletRecoveryPFlowPixelSeeds + 
    process.hltDoubletRecoveryPFlowCkfTrackCandidates + 
    process.hltDoubletRecoveryPFlowCtfWithMaterialTracks + 
    process.hltDoubletRecoveryPFlowTrackCutClassifier + 
    process.hltDoubletRecoveryPFlowTrackSelectionHighPurity +
    process.hltMergedTracks 
    )

process.hltPixelTracks.trackSrc = "hltPixelTracksFromGPU" 
process.hltPixelVertices.src = "hltPixelVerticesFromGPU" 

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.nEvents),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(options.inputFiles),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(True),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:' + str(options.nEvents)),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
process.mix.playback = True
process.mix.digitizers = cms.PSet()
for a in process.aliases: delattr(process, a)
process.RandomNumberGeneratorService.restoreStateLabel=cms.untracked.string('randomEngineStateProducer')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '130X_mcRun3_2023_realistic_relvals2023D_v2', '')
process.FastTimerService.writeJSONSummary = cms.untracked.bool(True)
process.FastTimerService.jsonFileName = cms.untracked.string('temp/times.json')
process.TFileService = cms.Service('TFileService', fileName=cms.string(options.outputFile) 
                                   if cms.string(options.outputFile) else 'default.root')


# Create multiple reconstruction and validation objects with parameters in parameters.csv
params = read_csv(options.parametersFile)
totalTasks = len(params)

taskList = []

theModulesToRun = list(process.HLTIterativeTrackingWithDoubletRecovery.moduleNames())
theModuleToTune = ["hltPixelTracksGPU"]
print(theModulesToRun)


for i, row in enumerate(params):

    setattr(process, theModuleToTune[0] + str(i), process.hltPixelTracksGPU.clone(
        CAThetaCutBarrel = cms.double(float(row[0])),
        CAThetaCutForward = cms.double(float(row[1])),
        dcaCutInnerTriplet = cms.double(float(row[2])),
        dcaCutOuterTriplet = cms.double(float(row[3])),
        hardCurvCut = cms.double(float(row[4])),
        z0Cut = cms.double(float(row[5])),
        phiCuts = cms.vint32(
            int(row[6]), int(row[7]), int(row[8]), int(row[9]), int(row[10]),
            int(row[11]), int(row[12]), int(row[13]), int(row[14]), int(row[15]),
            int(row[16]), int(row[17]), int(row[18]), int(row[19]), int(row[20]),
            int(row[21]), int(row[22]), int(row[23]), int(row[24])
        ),
    ))
    

    for f in theModulesToRun:
        if isinstance(getattr(process,f), cms.EDProducer):
            module = getattr(process,f)
            params = module.parameters_()

            new_name = f + str(i)
            new_params = cms.PSet()
            new_params.setValue(new_names(params,theModulesToRun + theModuleToTune,i))

            setattr(process, new_name, module.clone(new_params)) 
            taskList.append(getattr(process, new_name))
    
    setattr(process, 'simpleValidation' + str(i), cms.EDAnalyzer('SimpleValidation',
            chargedOnlyTP = cms.bool(True),
            intimeOnlyTP = cms.bool(False),
            invertRapidityCutTP = cms.bool(False),
            lipTP = cms.double(30.0),
            maxPhi = cms.double(3.2),
            maxRapidityTP = cms.double(2.5),
            minHitTP = cms.int32(0),
            minPhi = cms.double(-3.2),
            minRapidityTP = cms.double(-2.5),
            pdgIdTP = cms.vint32(),
            ptMaxTP = cms.double(1e+100),
            ptMinTP = cms.double(0.9),
            signalOnlyTP = cms.bool(True),
            stableOnlyTP = cms.bool(False),
            tipTP = cms.double(3.5),
            trackLabels = cms.VInputTag('hltMergedTracks' + str(i)),
            trackAssociator = cms.untracked.InputTag('quickTrackAssociatorByHits'),
            trackingParticles = cms.InputTag('mix', 'MergedTrackTruth')               
        )
    )

# Prevalidation
process.tpClusterProducer = cms.EDProducer('ClusterTPAssociationProducer',
    mightGet = cms.optional.untracked.vstring,
    phase2OTClusterSrc = cms.InputTag('siPhase2Clusters'),
    phase2OTSimLinkSrc = cms.InputTag('simSiPixelDigis','Tracker'),
    pixelClusterSrc = cms.InputTag('hltSiPixelClusters'),
    pixelSimLinkSrc = cms.InputTag('simSiPixelDigis'),
    simTrackSrc = cms.InputTag('g4SimHits'),
    stripClusterSrc = cms.InputTag('hltSiStripRawToClustersFacility'),
    stripSimLinkSrc = cms.InputTag('simSiStripDigis'),
    throwOnMissingCollections = cms.bool(True),
    trackingParticleSrc = cms.InputTag('mix','MergedTrackTruth')
)

process.quickTrackAssociatorByHits = cms.EDProducer('QuickTrackAssociatorByHitsProducer',
    AbsoluteNumberOfHits = cms.bool(False),
    Cut_RecoToSim = cms.double(0.75),
    PixelHitWeight = cms.double(1.0),
    Purity_SimToReco = cms.double(0.75),
    Quality_SimToReco = cms.double(0.5),
    SimToRecoDenominator = cms.string('reco'),
    ThreeHitTracksAreSpecial = cms.bool(True),
    cluster2TPSrc = cms.InputTag('tpClusterProducer'),
    useClusterTPAssociation = cms.bool(True)
)

# Lists of tasks
taskListVal = [getattr(process, 'simpleValidation'+str(i)) for i in range(totalTasks)]

process.HLTDoLocalPixelSequence = cms.Sequence( process.HLTDoLocalPixelTask )
process.raw2digi_step = cms.Path(process.HLTDoLocalStripSequence + process.HLTDoLocalPixelSequence)#process.RawToDigi_pixelOnly)

# Tasks and sequences
process.hltTracksTask = cms.Task(*taskList)
process.hlt_step = cms.Path(process.hltTracksTask)

process.preValidation = cms.Sequence(process.tpClusterProducer + process.quickTrackAssociatorByHits)
process.simpleValSeq = cms.Sequence(sum(taskListVal[1:],taskListVal[0]))

process.pre_validation_step = cms.Path(process.preValidation)
process.validation_step = cms.Path(process.simpleValSeq)
# process.consume_step = cms.EndPath(process.consumer)


# Schedule definition
process.schedule = cms.Schedule(
    process.raw2digi_step,
    # process.reconstruction_step,
    process.hlt_step,
    process.pre_validation_step,
    process.validation_step
    # process.consume_step
    )

# # print(process._itemsInDependencyOrder(process.tasks))
# print()
# from FWCore.ParameterSet.SequenceTypes import TaskVisitor
# for v in process.tasks:
#     print(v)
#     containedItems = []
#     V = TaskVisitor(containedItems)
#     process.tasks[v].visit(V)
#     print(containedItems)
#     for c in containedItems:
#         print(c)
#     print(process._itemsInDependencyOrder(process.tasks[v]))
# print(process._itemsInDependencyOrder(process.conditionaltasks))
# print(process._itemsInDependencyOrder(process.sequences))


# print(dada)

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads = 8
process.options.numberOfStreams = 0

# customisation of the process.

# Automatic addition of the customisation function from SimGeneral.MixingModule.fullMixCustomize_cff
from SimGeneral.MixingModule.fullMixCustomize_cff import setCrossingFrameOn 

#call to customisation function setCrossingFrameOn imported from SimGeneral.MixingModule.fullMixCustomize_cff
process = setCrossingFrameOn(process)

# End of customisation functions


# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
