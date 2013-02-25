# Pretend to be in different directory
import sys
sys.path.append('../')

from venture_engine_requirements import *
import cloud
import picloud_venture_credentials
cloud_environment = 'venture-2-6'

import time
import numpy as np
import scipy.io

# Load data
data = scipy.io.loadmat("../../data/irm_synth/irm_synth_20.mat", squeeze_me=True)
observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))

def get_samples(void_argument):
    # Import the venture engine
    import venture_engine
    
    # Start timing
    start = time.time()

    # Create RIPL and clear any previous session
    MyRIPL = venture_engine
    MyRIPL.clear()

    # Instantiate CRP
    #MyRIPL.assume('alpha', parse('(uniform-continuous 0.0001 2.0)'))
    MyRIPL.assume('cluster-crp', parse('(CRP/make 1)'))
    # Create class assignment lookup function
    MyRIPL.assume('node->class', parse('(mem (lambda (nodes) (cluster-crp)))'))
    # Create class interaction probability lookup function
    MyRIPL.assume('classes->parameters', parse('(mem (lambda (class1 class2) (beta 0.5 0.5)))')) 
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

    # Record some samples
    ids = [an_id for (an_id, _) in missing_links]
    samples = np.zeros((len(ids), 0))
    for unused in range(100):
        MyRIPL.infer(1000)
        samples = np.column_stack([samples, [MyRIPL.report_value(an_id) for an_id in ids]])

    # Average samples
    predictions = list(samples.mean(axis=1))
    
    return {'truth' : truth, 'predictions' : predictions, 'samples' : samples, 'runtime' : time.time() - start}

start = time.time()    
print 'Mapping'
jids = cloud.map(get_samples, range(10), _env=cloud_environment, _type='c1', _max_runtime=1)
print 'Waiting'
results = cloud.result(jids)
job_time_sum = 0
for result in results:
    print  'time = %f' % (result['runtime'])
    job_time_sum += result['runtime']
print 'Total wall-clock time = %f hours' % (job_time_sum / 3600)
duration = time.time() - start
cluster_factor = job_time_sum / duration
print 'Cluster factor of %f' % cluster_factor
