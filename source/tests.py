'''Misc testing routines - will become a messy file'''

import scipy.io
import cloud
cloud_environment = 'venture-2-6'

import experiment
import models

def timing_run_local():
    exp_params = experiment.exp_param_defaults({})
    exp_params['intermediate_iter'] = 1
    exp_params['max_initial_run_time'] = 30
    print experiment.exp_params_to_str(exp_params)
    
    data = scipy.io.loadmat("../data/irm_synth/irm_synth_20.mat", squeeze_me=True)
    observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
    missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))
    data = {'observations' : observed, 'missing' : missing}
    
    model = models.product_IRM
    model_params = {'D' : 1, 'alpha' : 1, 'symmetric' : True}
    print experiment.network_cv_timing_run(data, model, exp_params, model_params)

def timing_run_cloud():
    execfile('picloud_venture_credentials.py')
    exp_params = experiment.exp_param_defaults({})
    exp_params['intermediate_iter'] = 1
    exp_params['max_initial_run_time'] = 30
    print experiment.exp_params_to_str(exp_params)
    
    data = scipy.io.loadmat("../data/irm_synth/irm_synth_20.mat", squeeze_me=True)
    observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
    missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))
    data = {'observations' : observed, 'missing' : missing}
    
    model = models.product_IRM
    model_params = {'D' : 1, 'alpha' : 1, 'symmetric' : True}
    job_id = cloud.call(experiment.network_cv_timing_run, data, model, exp_params, model_params, _max_runtime=5, _env=cloud_environment)
    cloud.join(job_id)
    print cloud.result(job_id)
    
def timing_triple_local():
    exp_params = experiment.exp_param_defaults({})
    exp_params['intermediate_iter'] = 1
    exp_params['max_initial_run_time'] = 30
    exp_params['max_burn_time'] = 30
    exp_params['max_sample_time'] = 30
    exp_params['n_samples'] = 25
    print experiment.exp_params_to_str(exp_params)
    
    data = scipy.io.loadmat("../data/irm_synth/irm_synth_20.mat", squeeze_me=True)
    observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
    missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))
    data = {'observations' : observed, 'missing' : missing}
    
    model = models.product_IRM
    model_params = {'D' : 1, 'alpha' : 1, 'symmetric' : True}
    
    # Timing run
    time_per_mh_iter = experiment.network_cv_timing_run(data, model, exp_params, model_params)['time_per_mh_iter']
    
    # Live run
    exp_params['intermediate_iter'] = max(1, int(round(0.9 * exp_params['max_sample_time'] / (exp_params['n_samples'] * time_per_mh_iter))))
    print experiment.network_cv_single_run(data, model, exp_params, model_params)
    
def timing_triple_cloud():
    execfile('picloud_venture_credentials.py')
    exp_params = experiment.exp_param_defaults({})
    exp_params['intermediate_iter'] = 1
    exp_params['max_initial_run_time'] = 30
    exp_params['max_burn_time'] = 30
    exp_params['max_sample_time'] = 30
    exp_params['n_samples'] = 25
    print experiment.exp_params_to_str(exp_params)
    
    data = scipy.io.loadmat("../data/irm_synth/irm_synth_20.mat", squeeze_me=True)
    observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
    missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))
    data = {'observations' : observed, 'missing' : missing}
    
    model = models.product_IRM
    model_params = {'D' : 1, 'alpha' : 1, 'symmetric' : True}
    
    # Timing run
    print 'Timing'
    job_id = cloud.call(experiment.network_cv_timing_run, data, model, exp_params, model_params, _max_runtime=5, _env=cloud_environment)
    time_per_mh_iter = cloud.result(job_id)['time_per_mh_iter']
    
    # Live run
    print 'Live'
    exp_params['intermediate_iter'] = max(1, int(round(0.9 * exp_params['max_sample_time'] / (exp_params['n_samples'] * time_per_mh_iter))))
    job_id = cloud.call(experiment.network_cv_single_run, data, model, exp_params, model_params, _max_runtime=5, _env=cloud_environment)
    cloud.join(job_id)
    print cloud.result(job_id)
