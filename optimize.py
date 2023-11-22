from optimizer.mopso import MOPSO
import subprocess
from utils import get_metrics, write_csv
import numpy as np
import uproot
import argparse
import os
from functools import partial

# parsing argument
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--continuing', type=int, action='store')
parser.add_argument('-d', '--default', action='store_true')
parser.add_argument('-s', '--strips', action='store_true')
parser.add_argument('-p2','--phase2', action='store_true')
parser.add_argument('-hlt','--hlt', action='store_true')
parser.add_argument('-p', '--num_particles', default=200, type=int, action='store')
parser.add_argument('-i', '--num_iterations', default=20, type=int, action='store')
parser.add_argument('-e', '--num_events', default=100, type=int, action='store')
args = parser.parse_args()

# define the lower and upper bounds
if args.phase2:
    lb = [0.0, 0.0, 0.0, 0.0, 1.0 / 3.8 / 0.9, 5.0,
          400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 
          400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400,
          400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400,
          400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400,
          400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400]

    ub = [0.006, 0.03, 0.2, 1.0, 1.0 / 3.8 / 0.3, 20.0,
          1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
          1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
          1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
          1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
          1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
    
    config = 'reconstruction_phase2.py'
    #config = 'reconstruction_phase2_hlt.py'
    input_file = 'file:../023b71b9-1d38-4891-b5e6-d584032d2cc4.root'
        #'file:/gpu_data/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_131X_mcRun4_realistic_v5-v1/b75e209e-741d-4561-8516-9d63339bc0b7.root',
       # 'file:/gpu_data/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_131X_mcRun4_realistic_v5-v1/ba603e93-3ee7-4e53-ab37-335d6ff55d3d.root
elif args.strips:
    lb = [0.0, 0.0, 0.0, 0.0, 1.0 / 3.8 / 0.9, 5.0] + 42 * [500]
    ub = [0.006, 0.03, 0.2, 1.0, 1.0 / 3.8 / 0.3, 20.0] + 42*[900]

    config = 'reconstruction_strips.py'
    input_file = "file:/data/user/adiflori/ttbar_2023/2023D/00930c1c-4923-410a-8394-a0eea37a4114.root"
elif args.hlt:

    lb = [0.0, 0.0, 0.0, 0.0, 1.0 / 3.8 / 0.9, 5.0, 400, 
          400, 400, 400, 400, 400, 400, 400, 400, 400, 
          400, 400, 400, 400, 400, 400, 400, 400, 400]

    ub = [0.006, 0.03, 0.2, 1.0, 1.0 / 3.8 / 0.3, 20.0, 900,
          900, 900, 900, 900, 900, 900, 900, 900, 900, 
          900, 900, 900, 900, 900, 900, 900, 900, 900]
    
    config = 'reconstruction_2023_hlt.py'
    #config = 'reconstruction_2022_hlt.py'
    input_file = "file:/data/user/adiflori/ttbar_2023/2023D/404d4977-faf2-45d4-8a01-7fdeed9cf611.root" #'input/step2.root'
    #input_file = "file:/data/user/adiflori/ttbar_2023/2023C/7056f9b8-115d-4b49-ab5b-6c5d7056ca22.root"

else:
    lb = [0.0, 0.0, 0.0, 0.0, 1.0 / 3.8 / 0.9, 5.0, 400, 
          400, 400, 400, 400, 400, 400, 400, 400, 400, 
          400, 400, 400, 400, 400, 400, 400, 400, 400]

    ub = [0.006, 0.03, 0.2, 1.0, 1.0 / 3.8 / 0.3, 20.0, 900,
          900, 900, 900, 900, 900, 900, 900, 900, 900, 
          900, 900, 900, 900, 900, 900, 900, 900, 900]
    
    config = 'reconstruction_hion_offline.py'
    input_file = "../RAWHydjet2023Official/59e7e816-23bd-4488-86bf-d8521c36e330.root" #'input/step2.root'

# run pixel reconstruction and simple validation
def reco_and_validate(params,config,**kwargs):
    if not os.path.exists('temp'):
        os.mkdir('temp')
    print(params)
    write_csv('temp/parameters.csv', params)

    validation_result = 'temp/simple_validation.root'
    subprocess.run(['cmsRun', config, 'inputFiles=file:' + input_file, 'nEvents=' + str(args.num_events),
                     'parametersFile=temp/parameters.csv', 'outputFile=' + validation_result])
    num_particles = len(params)
    print(num_particles)
    print(params)
    #print(bdsihcs)
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

    print(len(default_params))  
    print(default_params)
    default_metrics = reco_and_validate(default_params,config)
    write_csv('checkpoint/default.csv', [np.concatenate([default_params[0], default_metrics[0]])])

objective = partial(reco_and_validate, config=config)

# create the PSO object
if not args.continuing:
    #os.system('rm history/*')
    pso = MOPSO(objective_functions=[objective],lower_bounds=lb, upper_bounds=ub, 
                num_objectives=2, num_particles=args.num_particles, num_iterations=args.num_iterations,  
                max_iter_no_improv=None, optimization_mode='global')
else:
    pso = MOPSO(objective_functions=[objective],lower_bounds=lb, upper_bounds=ub, 
                num_iterations=args.continuing, checkpoint_dir='checkpoint')

# run the optimization algorithm
pso.optimize(history_dir='history', checkpoint_dir='checkpoint')

