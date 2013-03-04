'''
Code to coordinate experiments

@authors: James Robert Lloyd (jrl44@cam.ac.uk)
          
Created March 2013          
'''

import os
import threading
import time
import scipy.io
import numpy as np

from venture_engine_requirements import *
import cloud
import picloud_venture_credentials
cloud_environment = 'venture-2-6'

import models
import sample
from utils.pyroc import ROCData
from utils.memory import memory

#### Utilities

def exp_param_defaults(exp_params):
    '''Sets all missing parameters to their default values'''
    defaults = {'type' : 'network_cv',
                'verbose' : True,
                'results_dir' : '../results/temp/',
                'data_dirs' : ['../data/test/'],
                'models' : [models.product_IRM],
                'model_params' : [{D=1, alpha=1, symmetric=True}],
                'n_samples' : 1000,
                'max_initial_run_time' : 120,
                'max_burn_time' : 1800,
                'max_sample_time' : 1800,
                'intermediate_iter' : 10}
    # Iterate through default key-value pairs, setting all unset keys
    for key, value in defaults.iteritems():
        if not key in exp_params:
            exp_params[key] = value
    return exp_params
    
def exp_params_to_str(exp_params):
    result = "Running experiment:\n"
    for key, value in exp_params.iteritems():
        result += "%s = %s,\n" % (key, value)
    return result
    
def mat_files(data_dir):
    """Produces list of all .mat files in a directory - returns absolute paths"""
    return [file_name for file_name in map(os.path.abspath, os.listdir(data_dir)) if file_name[-4:-1] == '.mat']
    
#### Experiment coordinators

def network_cv_single_run(data, model_class, exp_params, **model_params):
    '''Function to be sent to picloud'''
    start = time.clock()
    model = model_class(**model_params) # Create model
    model.observe_data(data['observations']) # Observe data
    # Setup values to be predicted
    #### TODO - can this be sensibly encapsulated?
    truth = []
    missing_links = []
    for (i,j,v) in data['missing']:
        truth.append(int(v))
        missing_links.append(model.RIPL.predict(parse('(p-friends %d %d)' % (i, j))))
    # Burn in
    sample.collect_n_samples(model.RIPL, n=exp_params['n_samples'], mh_iter=exp_params['intermediate_iter'], \
                                         ids = [an_id for (an_id, _) in missing_links], \
                                         max_runtime=exp_params['max_burn_time'], verbose=False)
    # Collect samples
    max_memory = memory()
    mcmc_output = sample.collect_n_samples(model.RIPL, n=exp_params['n_samples'], mh_iter=exp_params['intermediate_iter'], \
                                                       ids = [an_id for (an_id, _) in missing_links], \
                                                       max_runtime=exp_params['max_sample_time'], verbose=False)
    samples = mcmc_output['samples']
    sample_ess = mcmc_output['ess']
    max(max_memory, memory())
    # Score samples
    predictions = list(samples.mean(axis=1))
    roc_data = []
    for (true_link, prediction) in zip(truth, predictions):
        roc_data.append((true_link, prediction))
    AUC = ROCData(roc_data).auc()
    max_memory = max(max_memory, memory())
  
    return {'predictions' : predictions, 'ess' : sample_ess, 'AUC' : AUC, 'runtime' : time.clock() - start, 'max_memory' : max(max_memory, memory())}

def network_cv_timing_run(data, model_class, exp_params, **model_params):
    '''Function to be sent to picloud'''
    start = time.clock()
    model = model_class(**model_params) # Create model
    model.observe_data(data['observations']) # Observe data
    # Setup values to be predicted
    #### TODO - can this be sensibly encapsulated?
    truth = []
    missing_links = []
    for (i,j,v) in data['missing']:
        truth.append(int(v))
        missing_links.append(model.RIPL.predict(parse('(p-friends %d %d)' % (i, j))))
    # Sample
    mcmc_output = sample.collect_n_samples(model.RIPL, n=exp_params['n_samples'], mh_iter=exp_params['intermediate_iter'], \
                                                       ids = [an_id for (an_id, _) in missing_links], \
                                                       max_runtime=exp_params['max_initial_run_time'], verbose=False)                          
    samples = mcmc_output['samples']
    time_per_mh_iter = mcmc_output['runtime'] / samples.shape[1] * exp_params['intermediate_iter'] 
  
    return {'time_per_mh_iter' : time_per_mh_iter, 'runtime' : time.clock() - start}

def network_cv_fold(data_file, model_class, exp_params, **model_params):
    '''Performs a timing run and then sends random restarts to picloud'''
    file_list = mat_files(data_dir)
    # Use the first file as a timing run
    pass
    # Loop over folds
    # Wait for threads to finish
    # Collate results and write to file
            
def run_experiment_file(filename):
    '''Initiates a series of experiments specified by file'''
    
    # Load experiment parameters
    with open(filename, 'r') as exp_file:
        exp_params = exp_param_defaults(eval(exp_file.read()))
    print exp_params_to_str(exp_params)
    
    # Create results directory if it doesn't exist.
    if not os.path.isdir(exp_params.results_dir):
        os.makedirs(exp_params.results_dir)
        
    # Loop through data directories and model classes - starting threads
    threads = []
    for data_dir in exp_params.data_dirs:
        for data_file in mat_files(data_dir):
            for model, model_params in zip(exp_params.models, exp_params.model_params):
                if exp_params['type'] == 'network_cv':
                    threads.append(threading.Thread(target=network_cv_fold, args=(data_file, model, exp_params), kwargs=model_params))
                    threads[-1].start()
            
    # Wait for threads to complete
    time.sleep(10) # Avoid race conditions
    threads_finished = [False] * len(threads)
    while not all(threads_finished):
        for i, thread in enumerate(threads):
            if not threads_finished[i]:
                if not thread.is_alive():
                    threads_finished[i] = True
        print '%d of %d threads complete' % (sum(threads_finished), len(threads_finished))
        time.sleep(30)
    
    # Potentially call a post processing routine
    pass
        
