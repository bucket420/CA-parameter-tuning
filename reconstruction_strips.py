# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 -s RAW2DIGI:RawToDigi_pixelOnly,RECO:reconstruction_pixelTrackingOnly,VALIDATION:@pixelTrackingOnlyValidation,DQM:@pixelTrackingOnlyDQM --conditions auto:phase1_2022_realistic --datatier GEN-SIM-RECO,DQMIO -n 100 --eventcontent RECOSIM,DQM --geometry DB:Extended --era Run3 --procModifiers pixelNtupletFit,gpu --filein file:step2.root --fileout file:step3.root --nThreads 8
import FWCore.ParameterSet.Config as cms
from utils import read_csv

from HeterogeneousCore.CUDACore.ProcessAcceleratorCUDA import ProcessAcceleratorCUDA
from HeterogeneousCore.CUDACore.SwitchProducerCUDA import SwitchProducerCUDA
from HeterogeneousCore.ROCmCore.ProcessAcceleratorROCm import ProcessAcceleratorROCm

from Configuration.Eras.Era_Run3_cff import Run3
from Configuration.ProcessModifiers.pixelNtupletFit_cff import pixelNtupletFit
from Configuration.ProcessModifiers.stripNtupletFit_cff import stripNtupletFit

process = cms.Process('RECO',Run3,pixelNtupletFit,stripNtupletFit)

# import VarParsing
from FWCore.ParameterSet.VarParsing import VarParsing

# VarParsing instance
options = VarParsing('analysis')

# Custom options
options.register('parametersFile',
              'checkpoint/selected_params.csv',
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

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.Validation_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load( 'HLTrigger.Timer.FastTimerService_cfi' )

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
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
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
    printDependencies = cms.untracked.bool(False),
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
process.GlobalTag = GlobalTag(process.GlobalTag, '130X_mcRun3_2022_realistic_v2', '')
process.FastTimerService.writeJSONSummary = cms.untracked.bool(True)
process.FastTimerService.jsonFileName = cms.untracked.string('temp/times.json')
process.TFileService = cms.Service('TFileService', fileName=cms.string(options.outputFile) 
                                   if cms.string(options.outputFile) else 'default.root')


# Create multiple reconstruction and validation objects with parameters in parameters.csv

# process.siStripRecHitSoAHostPhase1 = cms.EDProducer("SiStripRecHitSoAHostPhase1",
#     mightGet = cms.optional.untracked.vstring,
#     pixelRecHitSoASource = cms.InputTag("siPixelRecHitsPreSplittingCPU"),
#     stripRecHitSource = cms.InputTag("siStripMatchedRecHits","matchedRecHit")
# )

process.siStripRecHitSoAHostPhase1.pixelRecHitSoASource = cms.InputTag("siPixelRecHitsPreSplittingCPU")

process.siPixelRecHitsPreSplittingCPU = cms.EDProducer("SiPixelRecHitSoAFromLegacyPhase1",
    CPE = cms.string('PixelCPEFast'),
    beamSpot = cms.InputTag("offlineBeamSpot"),
    convertToLegacy = cms.bool(True),
    mightGet = cms.optional.untracked.vstring,
    src = cms.InputTag("siPixelClustersPreSplitting")
)

process.siPixelRecHitsPreSplittingSoA = SwitchProducerCUDA(
    cpu = cms.EDAlias(
        siPixelRecHitsPreSplittingCPU = cms.VPSet(
            cms.PSet(
                type = cms.string('pixelTopologyPhase1TrackingRecHitSoAHost')
            ),
            cms.PSet(
                type = cms.string('uintAsHostProduct')
            )
        )
    )
)

process.siPixelRecHitsPreSplitting = SwitchProducerCUDA(
    cpu = cms.EDAlias(
        siPixelRecHitsPreSplittingCPU = cms.VPSet(
            cms.PSet(
                type = cms.string('SiPixelRecHitedmNewDetSetVector')
            ),
            cms.PSet(
                type = cms.string('uintAsHostProduct')
            )
        )
    )
)

process.siPixelRecHitsPreSplittingTask = cms.Task(process.siPixelRecHitsPreSplitting, process.siPixelRecHitsPreSplittingCPU, process.siPixelRecHitsPreSplittingSoA)
process.pixeltrackerlocalrecoTask = cms.Task(process.siPixelClustersPreSplittingTask, process.siPixelRecHitsPreSplittingTask)
process.reconstruction_pixelTrackingOnlyTask = cms.Task(process.offlineBeamSpotTask, process.pixeltrackerlocalrecoTask, process.recopixelvertexingTask, process.siPixelClusterShapeCachePreSplitting)
process.reconstruction_pixelTrackingOnly = cms.Sequence(process.reconstruction_pixelTrackingOnlyTask)

params = read_csv(options.parametersFile)
totalTasks = len(params)
for i, row in enumerate(params):
    setattr(process, 'pixelTracksSoA' + str(i), cms.EDProducer('CAHitNtupletCUDAPhase1',
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
                int(row[21]), int(row[22]), int(row[23]), int(row[24]),
                int(row[25]), int(row[26]), int(row[27]), int(row[28]),
                int(row[29]), int(row[30]), int(row[31]), int(row[32]),
                int(row[33]), int(row[34]), int(row[35]), int(row[36]),
                int(row[37]), int(row[38]), int(row[39]), int(row[40])
            
            ),
            doClusterCut = cms.bool(True),
            doPtCut = cms.bool(True),
            doSharedHitCut = cms.bool(True),
            doZ0Cut = cms.bool(True),
            dupPassThrough = cms.bool(False),
            earlyFishbone = cms.bool(True),
            fillStatistics = cms.bool(False),
            fitNas4 = cms.bool(False),
            idealConditions = cms.bool(True),
            includeJumpingForwardDoublets = cms.bool(False),
            lateFishbone = cms.bool(False),
            maxNumberOfDoublets = cms.uint32(524288),
            mightGet = cms.optional.untracked.vstring,
            minHitsForSharingCut = cms.uint32(10),
            minHitsPerNtuplet = cms.uint32(4),
            onGPU = cms.bool(False),
            pixelRecHitSrc = cms.InputTag('siStripRecHitSoAHostPhase1'),
            ptCut = cms.double(0.5),
            ptmin = cms.double(0.8999999761581421),
            trackQualityCuts = cms.PSet(
                chi2MaxPt = cms.double( 10.0 ),
                tripletMaxTip = cms.double( 0.3 ),
                chi2Scale = cms.double( 1.8 ),
                quadrupletMaxTip = cms.double( 0.5 ),
                quadrupletMinPt = cms.double( 0.1 ),
                quadrupletMaxZip = cms.double( 12.0 ),
                tripletMaxZip = cms.double( 12.0 ),
                tripletMinPt = cms.double( 0.1 ),
                chi2Coeff = cms.vdouble( 0.9, 1.8 )
            ),
            useRiemannFit = cms.bool(False),
            useSimpleTripletCleaner = cms.bool(True)
        )
    )
    
    setattr(process, 'pixelTracks' + str(i), cms.EDProducer('PixelTrackProducerFromSoAPhase1',
            beamSpot = cms.InputTag('offlineBeamSpot'),
            mightGet = cms.optional.untracked.vstring,
            minNumberOfHits = cms.int32(0),
            minQuality = cms.string('loose'),
            useStripHits = cms.bool(True),
            hitModuleStartSrc = cms.InputTag("siStripRecHitSoAHostPhase1"),   
            stripRecHitLegacySrc = cms.InputTag("siStripMatchedRecHits","matchedRecHit"),
            pixelRecHitLegacySrc = cms.InputTag('siPixelRecHitsPreSplittingCPU'),
            trackSrc = cms.InputTag('pixelTracksSoA' + str(i))
        )
    )
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
            trackLabels = cms.VInputTag('pixelTracks' + str(i)),
            trackAssociator = cms.untracked.InputTag('quickTrackAssociatorByHits'),
            trackingParticles = cms.InputTag('mix', 'MergedTrackTruth')               
        )
    )

# Prevalidation
process.tpClusterProducer = cms.EDProducer('ClusterTPAssociationProducer',
    mightGet = cms.optional.untracked.vstring,
    phase2OTClusterSrc = cms.InputTag('siPhase2Clusters'),
    phase2OTSimLinkSrc = cms.InputTag('simSiPixelDigis','Tracker'),
    pixelClusterSrc = cms.InputTag('siPixelClustersPreSplitting'),
    pixelSimLinkSrc = cms.InputTag('simSiPixelDigis'),
    simTrackSrc = cms.InputTag('g4SimHits'),
    stripClusterSrc = cms.InputTag('siStripClusters'),
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
#taskListCUDA = [getattr(process, 'pixelTracksCUDA'+str(i)) for i in range(totalTasks)]
taskListSoA = [getattr(process, 'pixelTracksSoA'+str(i)) for i in range(totalTasks)]
taskList = [getattr(process, 'pixelTracks'+str(i)) for i in range(totalTasks)]
taskListVal = [getattr(process, 'simpleValidation'+str(i)) for i in range(totalTasks)]

taskStripList = [process.siStripRecHitSoAHostPhase1, process.striptrackerlocalrecoTask]
# Tasks and sequences
process.stripTask = cms.Task(*taskStripList)
process.pixelTracksTask = cms.Task(*taskListSoA, *taskList)


process.pixelTracksSeq = cms.Sequence(process.pixelTracksTask)
process.preValidation = cms.Sequence(process.tpClusterProducer + process.quickTrackAssociatorByHits)
process.simpleValSeq = cms.Sequence(sum(taskListVal[1:],taskListVal[0]))
process.consumer = cms.EDAnalyzer('GenericConsumer', eventProducts = cms.untracked.vstring(["pixelTracks" + str(i) for i in range(totalTasks)]))

process.strip_seq = cms.Sequence(process.stripTask)
# Path and EndPath definitions

process.raw2digi_step = cms.Path(process.RawToDigi_trackerOnly)
process.reconstruction_step = cms.Path(process.reconstruction_pixelTrackingOnly)
process.pixel_tracks_step = cms.Path(process.pixelTracksTask)
process.pre_validation_step = cms.Path(process.preValidation)
process.validation_step = cms.Path(process.simpleValSeq)
process.consume_step = cms.EndPath(process.consumer)
process.strip_step = cms.Path(process.strip_seq)
# process.strip_hits = cms.Path(process.striptrackerlocalreco)

# Schedule definition
process.schedule = cms.Schedule(
    process.raw2digi_step,
    # process.strip_hits,
    process.strip_step,
    process.reconstruction_step,
    process.pixel_tracks_step,
    process.pre_validation_step,
    process.validation_step,
    process.consume_step
    )

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads = 16
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
