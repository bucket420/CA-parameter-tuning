import numpy as np
from inspect import getmro
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.Mixins import _Parameterizable 

# calculate the metrics from validation results
def get_metrics(uproot_file, id):
    tree = uproot_file['simpleValidation' + str(id)]['output']
    total_rec = tree['rt'].array()[0]
    total_ass = tree['at'].array()[0]
    total_ass_sim = tree['ast'].array()[0]
    total_dup = tree['dt'].array()[0]
    total_sim = tree['st'].array()[0]
    
    if not total_ass or not total_rec or not total_sim or not total_ass_sim:
        return [1.0] * 2
    
    return [1 - total_ass_sim / total_sim, (total_rec - total_ass + total_dup) / total_rec]

# read a csv file, return a matrix
def read_csv(filename):
    matrix = np.genfromtxt(filename, delimiter=",", dtype=float)
    if matrix.ndim == 2:
        return np.genfromtxt(filename, delimiter=",", dtype=float)
    return np.array([matrix])
    
# write a matrix to a csv file
def write_csv(filename, matrix):
    np.savetxt(filename, matrix, fmt='%.18f', delimiter=',')

def has_params(typ):
    return _Parameterizable in getmro(typ)

def new_names(names,inputs,i):
    new_names_for_module = {}
    # print(names)
    for p in names:
        
        thisParam = names[p]
        thisType = type(thisParam)

        if has_params(thisType): #if has params go recursive! This is a PSet
            # print(p," has params")
            old_names_for_param = thisParam.parameters_()
            new_names_for_param = new_names(old_names_for_param,inputs,i)
            new_names_for_module[p] = cms.PSet()
            new_names_for_module[p].setValue(new_names_for_param)
        else: #this is simple, either an InputTag or VInputTag
            if thisType == type(cms.InputTag("")):
                # print(p," normal ")
                for mod in inputs:
                    if mod == thisParam.value().split(":")[0]: ## check needed for complex InputTags
                        new_val = thisParam.value().replace(mod,mod+str(i))
                        new_names_for_module[p] = cms.InputTag(new_val)
            elif thisType == type(cms.VInputTag("")):
                vinput = [v + str(i) if v in inputs else v for v in names[p].value()]
                new_names_for_module[p] = cms.VInputTag(vinput)
            else:
                # print(p, "the same")
                new_names_for_module[p] = names[p]
    return new_names_for_module
