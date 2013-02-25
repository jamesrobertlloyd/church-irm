from venture_engine_requirements import *
import cloud
import picloud_venture_credentials
cloud_environment = 'venture-2-6'

import time
import numpy as np

def get_samples_really_fast(void_argument):
    # Import the venture engine
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

    # Record some samples
    ids = [an_id for (an_id, _) in missing_links]
    samples = np.zeros((len(ids), 0))
    for unused in range(10):
        MyRIPL.infer(10)
        samples = np.column_stack([samples, [MyRIPL.report_value(an_id) for an_id in ids]])

    # Average samples
    predictions = list(samples.mean(axis=1))
    
    return {'truth' : truth, 'predictions' : predictions, 'samples' : samples, 'runtime' : time.clock() - start}

def get_samples_fast(void_argument):
    # Import the venture engine
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

    # Record some samples
    ids = [an_id for (an_id, _) in missing_links]
    samples = np.zeros((len(ids), 0))
    for unused in range(10):
        MyRIPL.infer(1000)
        samples = np.column_stack([samples, [MyRIPL.report_value(an_id) for an_id in ids]])

    # Average samples
    predictions = list(samples.mean(axis=1))
    
    return {'truth' : truth, 'predictions' : predictions, 'samples' : samples, 'runtime' : time.clock() - start}
    
print 'Mapping very fast jobs - should be successful'
jids = cloud.map(get_samples_really_fast, range(10), _env=cloud_environment, _type='c1')
print 'Waiting for results'
results = cloud.result(jids)
for result in results:
    print  'time = %f' % (result['runtime'])
    
print 'Mapping fairly fast jobs - will probably fail'
jids = cloud.map(get_samples_fast, range(10), _env=cloud_environment, _type='c1')
print 'Waiting for results'
results = cloud.result(jids)
for result in results:
    print  'time = %f' % (result['runtime'])
