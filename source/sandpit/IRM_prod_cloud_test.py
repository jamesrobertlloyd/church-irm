# Pretend to be in source directory
import sys
sys.path.append('../')

from venture_engine_requirements import *
import cloud
import picloud_venture_credentials
cloud_environment = 'venture-2-6'

import scipy.io
import time
import numpy as np

from utils.pyroc import ROCData
import sample

# Parameters of experiment
D = 3
alpha = 1
fold = 1
max_runtime = 10 # In seconds - default 1800
n_samples = 1000 # Target - max_runtime wins in a dispute
mh_iter = 100 # Intermediate iterations between samples
verbose = False
local_computation = True # Test single threaded locally

repeats = 10 # Number of machines to map to
job_kill_time = 60 # Minutes before jobs are killed - to prevent large bills!
machine_type = 'c1' # The cheapest!
cores = 1 # Number of cores to string together - useful for high memory jobs

# Load data
data = scipy.io.loadmat("../../data/hs/hs_%dof5.mat" % fold, squeeze_me=True)
#data = scipy.io.loadmat("../../data/irm_synth/irm_synth_20.mat", squeeze_me=True)
observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))

def get_samples(void_argument):
    # TODO - does this import statement have to be here when using cloud?
    import venture_engine

    # Start timing
    start = time.clock()

    # Create RIPL and clear any previous session
    MyRIPL = venture_engine
    MyRIPL.clear()

    for d in range(D):
        # Instantiate CRP
        #MyRIPL.assume('alpha-%d' % d, parse('(uniform-continuous 0.0001 2.0)'))
        MyRIPL.assume('cluster-crp-%d' % d, parse('(CRP/make %f)' % alpha))
        # Create class assignment lookup function
        MyRIPL.assume('node->class-%d' % d, parse('(mem (lambda (nodes) (cluster-crp-%d)))' % d))
        # Create class interaction probability lookup function
        MyRIPL.assume('classes->parameters-%d' % d, parse('(mem (lambda (class1 class2) (beta 0.5 0.5)))')) 
     
    # Create relation probability function    
    MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (* ' + ' '.join(['(classes->parameters-%d (node->class-%d node1) (node->class-%d node2))' % (d,d,d) for d in range(D)]) + '))')) 
    # Create relation evaluation function
    MyRIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 

    # Tell Venture about observations - doubling up for symmetry without using min and max
    for (i,j,v) in observed:
        if verbose:
            print 'Observing (%3d, %3d) = %d' % (i, j, v)
        if v:
            MyRIPL.observe(parse('(friends %d %d)' % (i, j)), 'true')
            MyRIPL.observe(parse('(friends %d %d)' % (j, i)), 'true')
        else:
            MyRIPL.observe(parse('(friends %d %d)' % (i, j)), 'false')
            MyRIPL.observe(parse('(friends %d %d)' % (j, i)), 'false')
                
    # Tell Venture that we want to predict P(unobserved link)
    truth = []
    missing_links = []
    for (i,j,v) in missing:
        if verbose:
            print 'Predicting (%3d, %3d) = %d' % (i, j, v)
        truth.append(int(v))
        missing_links.append(MyRIPL.predict(parse('(p-friends %d %d)' % (i, j))))

    # Burn in
    sample.collect_n_samples(MyRIPL, n=n_samples, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], max_runtime=max_runtime/2, verbose=verbose)
    # Collect samples
    mcmc_output = sample.collect_n_samples(MyRIPL, n=n_samples, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], max_runtime=max_runtime/2, verbose=verbose)
    samples = mcmc_output['samples']
    sample_ess = mcmc_output['ess']

    if verbose:
        print 'Fold complete'
    predictions = list(samples.mean(axis=1))
    roc_data = []
    for (true_link, prediction) in zip(truth, predictions):
        roc_data.append((true_link, prediction))
    AUC = ROCData(roc_data).auc()
    if verbose:
        print 'AUC = %f' % AUC
    
    # FIXME - This need not return the truth nor the raw samples
    #return {'truth' : truth, 'predictions' : predictions, 'samples' : samples, 'ess' : sample_ess, 'AUC' : AUC, 'runtime' : time.clock() - start}
    return {'predictions' : predictions, 'ess' : sample_ess, 'AUC' : AUC, 'runtime' : time.clock() - start}

start = time.time()  
if not local_computation:  
    print 'Mapping'
    jids = cloud.map(get_samples, range(repeats), _env=cloud_environment, _type=machine_type, _cores=cores, _max_runtime=job_kill_time)

    print 'Waiting'
    results = cloud.result(jids)
else:
    results = []
    for unused in range(repeats):
        results.append(get_samples(unused))

# Results back - display raw output
job_time_sum = 0
ess_sum = 0
for (i, result) in enumerate(results):
    print 'D = %d, fold = %d, restart = %2d, ess = %f, AUC = %f, Runtime = %f' % (D, fold, i+1, result['ess'], result['AUC'], result['runtime'])
    if i == 0:
        samples = result['predictions']
    else:
        samples = np.column_stack([samples, result['predictions']])
    job_time_sum += result['runtime']
    ess_sum += result['ess']
print 'Total cpu time = %f hours' % (job_time_sum / 3600)
print 'Local time elapsed = %f hours' % ((time.time() - start) / 3600)

# Process results and compute overall AUC
# First construct the truth
truth = []
for (i,j,v) in missing:
    truth.append(int(v))
# Then average predictions
predictions = list(samples.mean(axis=1))
# Then compute AUC
roc_data = []
for (true_link, prediction) in zip(truth, predictions):
    roc_data.append((true_link, prediction))
AUC = ROCData(roc_data).auc()
print 'D = %d, fold = %d, restarts = %d, ess = %f, AUC = %f' % (D, fold, repeats, ess_sum, AUC)
