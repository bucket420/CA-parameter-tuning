#! /usr/bin/env python3
from optimizer.mopso import MOPSO
import subprocess
from utils import get_metrics, write_csv
from graphs import convert_to_graph, from_modules_to_module
import numpy as np
import uproot
import argparse
import os
import sys
import imp

import FWCore.ParameterSet.Config as cms

# parsing argument
parser = argparse.ArgumentParser()
parser.add_argument('config')
parser.add_argument('-c', '--continuing', type=int, action='store')
parser.add_argument('-d', '--default', action='store_true')
parser.add_argument('-t','--tune', nargs='+', help='modules to tune', required=True)
parser.add_argument('-v','--validate', type=str, help='target module to validate', required=True)
#parser.add_argument('-pn','--par_names', nargs='+', help='modules to tune', required=True)
parser.add_argument('-p', '--num_particles', default=200, type=int, action='store')
parser.add_argument('-i', '--num_iterations', default=20, type=int, action='store')
parser.add_argument('-e', '--num_events', default=100, type=int, action='store')
parser.add_argument('-j', '--num_threads', default=8, type=int, action='store')
parser.add_argument('-f', '--input_file', default="file:step2.root", type=str)

args = parser.parse_args()




def parseProcess(filename): 
  # from https://github.com/cms-patatrack/patatrack-scripts/blob/master/multirun.py
  # parse the given configuration file and return the `process` object it define
  # the import logic is taken from edmConfigDump
  try:
    handle = open(filename, 'r')
  except:
    print("Failed to open %s: %s" % (filename, sys.exc_info()[1]))
    sys.exit(1)

  # make the behaviour consistent with 'cmsRun file.py'
  sys.path.append(os.getcwd())
  try:
    pycfg = imp.load_source('pycfg', filename, handle)
    process = pycfg.process
  except:
    print("Failed to parse %s: %s" % (filename, sys.exc_info()[1]))
    sys.exit(1)

  handle.close()
  return process

# run pixel reconstruction and simple validation
def reco_and_validate(params):
    if not os.path.exists('temp'):
        os.mkdir('temp')
    write_csv('temp/parameters.csv', params)
    validation_result = 'temp/simple_validation.root'
    subprocess.run(['cmsRun', config, 'inputFiles=file:' + input_file, 'nEvents=' + str(args.num_events),
                     'parametersFile=temp/parameters.csv', 'outputFile=' + validation_result])
    num_particles = len(params)
    with uproot.open(validation_result) as uproot_file:
        population_fitness = [get_metrics(uproot_file, i) for i in range(num_particles)]
    return population_fitness

phi0p05 = 522
phi0p06 = 626
phi0p07 = 730
phi0p09 = 900

# get default metrics
if args.default: ##TODO USE NPAAIRS FOR PHI
    if args.phase2:
        default_params = [[0.0020000000949949026, 0.003000000026077032, 0.15000000596046448, 0.25, 0.03284072249589491, 7.5,
                           phi0p05, phi0p05, phi0p05, phi0p06, phi0p07, phi0p07, phi0p06, phi0p07, phi0p07, phi0p05, phi0p05,
                           phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05,
                           phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p07, phi0p07, phi0p07, phi0p07,
                           phi0p07, phi0p07, phi0p07, phi0p07, phi0p07, phi0p07, phi0p07, phi0p07, phi0p07, phi0p07, phi0p07,
                           phi0p07, phi0p07, phi0p07, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05]]
    else:
        default_params = [[0.0020000000949949026, 0.003000000026077032, 0.15000000596046448, 0.25, 0.03284072249589491, 
                           12.0, phi0p05, phi0p07, phi0p07, phi0p05, phi0p06, phi0p06, phi0p05, phi0p05, phi0p06, 
                           phi0p06, phi0p06, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05, phi0p05]]
        
    default_metrics = reco_and_validate(default_params)
    write_csv('checkpoint/default.csv', [np.concatenate([default_params[0], default_metrics[0]])])

        
# # create the PSO object
# if not args.continuing:
#     #os.system('rm history/*')
#     pso = MOPSO(objective_functions=[reco_and_validate],lower_bounds=lb, upper_bounds=ub, 
#                 num_objectives=2, num_particles=args.num_particles, num_iterations=args.num_iterations,  
#                 max_iter_no_improv=None, optimization_mode='global')
# else:
#     pso = MOPSO(objective_functions=[reco_and_validate],lower_bounds=lb, upper_bounds=ub, 
#                 num_iterations=args.continuing, checkpoint_dir='checkpoint')

if __name__ == "__main__":

    input_file = args.input_file
    config_to_run = args.config
    dot_to_run = config_to_run.replace("py","dot")
    process_zero = parseProcess(config_to_run)
    process_to_run = parseProcess(config_to_run)
    ## This is just to get the dependecy graph
    process_zero.source = cms.Source("EmptySource",
        numberEventsInRun = cms.untracked.uint32(0),
        firstRun = cms.untracked.uint32(0)
    )
    
    process_zero.DependencyGraph = cms.Service("DependencyGraph")
    process_zero.DependencyGraph.fileName = cms.untracked.string(dot_to_run)
    process_zero.maxEvents.input = 0

    with open("process_zero.py",'w') as f:     
        f.write(process_zero.dumpPython() )
        f.write('\n' )
    
    #subprocess.run(['cmsRun', "process_zero.py"])
    
    process_graph = convert_to_graph(dot_to_run)
    modules_to_modify = from_modules_to_module(process_graph,args.tune,args.validate)
    #for the moment let's restrict to 0
    module_to_tune = args.tune[0]
    #print(process_to_run.moduleNames())
    
    with open('process_to_run.py', 'w') as new:
        with open('header.py') as add:
            new.write(add.read())
        with open(config_to_run) as add:
            new.write(add.read())
        with open('footer.py') as add:
            new.write('tune = %s\n'%repr(module_to_tune))
            new.write('chain = %s\n'%repr(modules_to_modify))
            new.write('target = %s\n'%repr(args.validate))
            new.write(add.read())

    
    # with open("common_header.py",'r') as f:     
    #     f.write(process_zero.dumpPython() )
    #     f.write('\n' )
    #process.consumer = cms.EDAnalyzer('GenericConsumer', eventProducts = cms.untracked.vstring('tracksValidation'))

    process_to_run.options.numberOfThreads = args.num_threads
    
# run the optimization algorithm
#pso.optimize(history_dir='history', checkpoint_dir='checkpoint')

