# Pretend to be in different directory
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

# Load high school data set
#data = scipy.io.loadmat("../../data/hs/hs_%dof5.mat" % fold, squeeze_me=True)
#data = scipy.io.loadmat("../../data/irm_synth/irm_synth_20.mat", squeeze_me=True)
#observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
#missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))

def get_samples(void_argument):
    # Import the venture engine FIXME - does this statement have to be wrapped like this?
    import venture_engine
    
    # Start timing
    start = time.clock()

    # Create RIPL and clear any previous session
    MyRIPL = venture_engine
    MyRIPL.clear()
    
    # Load data
    observed = [(1,2,1),(1,3,1),(1,4,1),(2,3,0),(2,5,1)]
    missing  = [(1,5,1),(2,4,0),(3,4,1),(4,5,1)]

    # Instantiate CRP
    MyRIPL.assume('cluster-crp', parse('(CRP/make 1)'))
    # Create class assignment lookup function
    MyRIPL.assume('node->class', parse('(mem (lambda (nodes) (cluster-crp)))'))
    # Create class interaction probability lookup function
    MyRIPL.assume('classes->parameters', parse('(mem (lambda (class1 class2) (beta 0.1 0.1)))')) 
    # Create relation evaluation function
    MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (classes->parameters (node->class node1) (node->class node2)))')) 
    MyRIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 

    # Tell Venture about observations
    for (i,j,v) in observed:
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
        truth.append(int(v))
        missing_links.append(MyRIPL.predict(parse('(p-friends %d %d)' % (i, j))))

    # Burn in
    #sample.collect_n_es(MyRIPL, n=burn, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], min_samples=n_samples*2, max_runtime=600, verbose=verbose)
    #sample.collect_n_samples(MyRIPL, n=burn, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], max_runtime=60, verbose=verbose)
    # Collect samples
    #mcmc_output = sample.collect_n_es(MyRIPL, n=n_samples, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], min_samples=n_samples*2, max_runtime=300, verbose=verbose)
    #mcmc_output = sample.collect_n_samples(MyRIPL, n=n_samples, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], max_runtime=60, verbose=verbose)
    #samples = mcmc_output['samples']
    #sample_ess = mcmc_output['ess']
    
    ids = [an_id for (an_id, _) in missing_links]
    samples = np.zeros((len(ids), 0))
    iter_start = time.clock()
    for unused in range(100):
        MyRIPL.infer(10)
        samples = np.column_stack([samples, [MyRIPL.report_value(an_id) for an_id in ids]])
        
    #ess = np.mean([(samples.shape[1]) / act.batch_means(samples[i,:]) for i in range(samples.shape[0])])
    #ess = -1

    predictions = list(samples.mean(axis=1))
    
    #roc_data = []
    #for (true_link, prediction) in zip(truth, predictions):
    #    roc_data.append((true_link, prediction))
    #AUC = ROCData(roc_data).auc()
    
    return {'truth' : truth, 'predictions' : predictions, 'samples' : samples, 'runtime' : time.clock() - start}
    #return {'truth' : truth, 'predictions' : predictions, 'samples' : samples, 'ess' : -1, 'AUC' : AUC, 'runtime' : time.clock() - start}
    
print 'Mapping jobs'
jids = cloud.map(get_samples, range(10), _env=cloud_environment, _type='c1')
print 'Waiting for results'
results = cloud.result(jids)
for result in results:
    #print result
    roc_data = []
    for (true_link, prediction) in zip(result['truth'], result['predictions']):
        roc_data.append((true_link, prediction))
    AUC = ROCData(roc_data).auc()
    #print  'time = %f' % (result['runtime'])
    print  'AUC = %f : time = %f' % (AUC, result['runtime'])
    #print  'ess = %f, AUC = %f : time = %f' % (results['ess'], result['AUC'], result['runtime'])
