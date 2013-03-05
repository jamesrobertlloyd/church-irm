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
import itertools

from venture_engine_requirements import *
import cloud
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
                'model_params' : [{'D' : 1, 'alpha' : 1, 'symmetric' : True}],
                'n_samples' : 1000,
                'max_initial_run_time' : 30,
                'max_burn_time' : 30,
                'max_sample_time' : 30,
                'intermediate_iter' : 1,
                'core_type' : 'c1',
                'cores_per_job' : 1,
                'n_restarts' : 5}
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

def network_cv_single_run(data, model_class, exp_params, model_params):
    '''Function to be sent to picloud'''
    start = time.clock()
    model = model_class(**model_params) # Create model
    model.create_RIPL()
    model.observe_data(data['observations']) # Observe data
    truth, missing_links =  model.set_predictions(data['missing'])
    # Burn in
    sample.collect_n_samples(model.RIPL, n=exp_params['n_samples'], mh_iter=exp_params['intermediate_iter'], \
                                         ids = missing_links, \
                                         max_runtime=exp_params['max_burn_time'], verbose=False)
    # Collect samples
    max_memory = memory()
    mcmc_output = sample.collect_n_samples(model.RIPL, n=exp_params['n_samples'], mh_iter=exp_params['intermediate_iter'], \
                                                       ids = missing_links, \
                                                       max_runtime=exp_params['max_sample_time'], verbose=False)
    samples = mcmc_output['samples']
    n_samples = samples.shape[1]
    sample_ess = mcmc_output['ess']
    max(max_memory, memory())
    # Score samples
    predictions = list(samples.mean(axis=1))
    roc_data = []
    for (true_link, prediction) in zip(truth, predictions):
        roc_data.append((true_link, prediction))
    AUC = ROCData(roc_data).auc()
    max_memory = max(max_memory, memory())
  
    return {'predictions' : predictions, 'ess' : sample_ess, 'AUC' : AUC, 'runtime' : time.clock() - start, 'max_memory' : max(max_memory, memory()), 'n_samples' : n_samples}

def network_cv_timing_run(data, model_class, exp_params, model_params):
    '''Function to be sent to picloud'''
    start = time.clock()
    model = model_class(**model_params) # Create model
    model.create_RIPL()
    model.observe_data(data['observations']) # Observe data
    truth, missing_links =  model.set_predictions(data['missing'])
    mcmc_output = sample.estimate_mh_time(model.RIPL, n=exp_params['n_samples'], \
                                                      initial_mh_iter=exp_params['intermediate_iter'], \
                                                      ids = missing_links, \
                                                      max_runtime=exp_params['max_initial_run_time'], \
                                                      verbose=True) 
    return {'time_per_mh_iter' : mcmc_output['time_per_mh_iter'], 'runtime' : time.clock() - start, 'max_memory' : mcmc_output['max_memory']}

def network_cv_fold(data_file, data_dir, model_class, exp_params, model_params):
    '''Performs a timing run and then sends random restarts to picloud'''
    # Load data
    data = scipy.io.loadmat(data_file, squeeze_me=True)
    observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
    missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))
    data = {'observations' : observed, 'missing' : missing}
    # Perform a timing run
    job_id = cloud.call(network_cv_timing_run, data, model_class, exp_params, model_params, \
                        _max_runtime=3*exp_params['max_initial_run_time']/60, _env=cloud_environment, _type=exp_params['core_type'], _cores=exp_params['cores_per_job'])
    time_per_mh_iter = cloud.result(job_id)['time_per_mh_iter']
    # Map random restarts to picloud
    exp_params['intermediate_iter'] = max(1, int(round(0.9 * exp_params['max_sample_time'] / (exp_params['n_samples'] * time_per_mh_iter))))
    job_ids = cloud.map(network_cv_single_run, itertools.repeat(data, exp_params['n_restarts']), \
                                               itertools.repeat(model_class, exp_params['n_restarts']), \
                                               itertools.repeat(exp_params, exp_params['n_restarts']), \
                                               itertools.repeat(model_params, exp_params['n_restarts']), \
                                               _max_runtime=2*(exp_params['max_burn_time']+exp_params['max_sample_time'])/60, _env=cloud_environment, \
                                               _type=exp_params['core_type'], _cores=exp_params['cores_per_job'])
    # Collate results and write to file
    results = cloud.result(job_ids)
    print results
    #### FINISH ME
            
def run_experiment_file(filename):
    '''Initiates a series of experiments specified by file'''
    
    # Load cloud credentials at entry point to prevent picloud attempting to load file
    execfile('picloud_venture_credentials.py')
    
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
                    threads.append(threading.Thread(target=network_cv_fold, args=(data_file, data_dir, model, exp_params, model_params)))
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
        if not all(threads_finished):
            time.sleep(30)
    
    # Potentially call a post processing routine
    pass
        
