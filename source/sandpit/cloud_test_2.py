import sys
sys.path.append('../')

import cloud
import picloud_venture_credentials
cloud_environment = 'venture-2-6'
from venture_engine_requirements import *
import time

IntermediateMHIterations = 10

def sample_once(void_argument):
    import venture_engine
    # Create RIPL and clear any previous session
    MyRIPL = venture_engine
    MyRIPL.clear()

    # Load data
    observed = [(1,2,1),(1,3,1),(1,4,1),(2,3,0),(2,5,1)]
    missing  = [(1,5,1),(2,4,0),(3,4,1),(4,5,1)]

    # Instantiate CRP
    #MyRIPL.assume('alpha', parse('(uniform-continuous 0.0001 2.0)'))
    MyRIPL.assume('cluster-crp', parse('(CRP/make 1)'))
    # Create class assignment lookup function
    MyRIPL.assume('node->class', parse('(mem (lambda (nodes) (cluster-crp)))'))
    # Create class interaction probability lookup function
    MyRIPL.assume('classes->parameters', parse('(mem (lambda (class1 class2) (beta 0.1 0.1)))')) 
    # Create relation evaluation function
    MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (classes->parameters (node->class node1) (node->class node2)))')) 
    MyRIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 

    MyRIPL.observe(parse('(friends %d %d)' % (1, 2)), 'true')
    # Tell Venture about observations
    #for (i,j,v) in observed:
    #    if v:
    #        MyRIPL.observe(parse('(friends %d %d)' % (i, j)), 'true')
    #        MyRIPL.observe(parse('(friends %d %d)' % (j, i)), 'true')
    #    else:
    #        MyRIPL.observe(parse('(friends %d %d)' % (i, j)), 'false')
    #        MyRIPL.observe(parse('(friends %d %d)' % (j, i)), 'false')
                
    # Tell Venture that we want to predict P(unobserved link)
    #truth = []
    #missing_links = []
    #for (i,j,v) in missing:
    #    truth.append(int(v))
    #    missing_links.append(MyRIPL.predict(parse('(p-friends %d %d)' % (i, j))))
        
    #MyRIPL.infer(IntermediateMHIterations)
    return 'Complete'

start_time = time.time()
print 'Mapping'
jids = cloud.map(sample_once, range(1), _env=cloud_environment, _type='c1')
print 'Waiting'
results = cloud.result(jids)
print results
print 'Success'
