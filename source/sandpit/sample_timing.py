# Pretend to be in different directory
import sys
sys.path.append('../')

from venture_engine_requirements import *
import venture_engine

import scipy.io
import time
import numpy as np

from utils.pyroc import ROCData
from utils.memory import memory
import sample

def IRM(fold=1,burn=50,n_samples=100,mh_iter=10,verbose=True):

    # Start timing
    start = time.clock()

    # Create RIPL and clear any previous session
    MyRIPL = venture_engine
    MyRIPL.clear()

    # Load high school data set
    #data = scipy.io.loadmat("../../data/hs/hs_%dof5.mat" % fold, squeeze_me=True)
    data = scipy.io.loadmat("../../data/irm_synth/irm_synth_20.mat", squeeze_me=True)
    observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
    missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))
    #observed = [(1,2,1),(1,3,1),(1,4,1),(2,3,0),(2,5,1)]
    #missing  = [(1,5,1),(2,4,0),(3,4,1),(4,5,1)]

    # Convenience functions
    MyRIPL.assume('min-2', parse('(lambda (x y) (if (> x y) y x))'))
    MyRIPL.assume('max-2', parse('(lambda (x y) (if (> x y) x y))'))
    # Instantiate CRP
    MyRIPL.assume('alpha', parse('(uniform-continuous 0.0001 2.0)'))
    MyRIPL.assume('cluster-crp', parse('(CRP/make alpha)'))
    # Create class assignment lookup function
    MyRIPL.assume('node->class', parse('(mem (lambda (nodes) (cluster-crp)))'))
    # Create class interaction probability lookup function
    MyRIPL.assume('classes->parameters', parse('(mem (lambda (class1 class2) (beta 0.5 0.5)))')) 
    #MyRIPL.assume('classes->parameters-symmetric', parse('(lambda (class1 class2) (classes->parameters (min-2 class1 class2) (max-2 class1 class2)))')) 
    # Create relation evaluation function
    MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (classes->parameters (node->class node1) (node->class node2)))')) 
    MyRIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 

    # Tell Venture about observations
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

    for i in range(10, 501, 10):
        start_iter = time.clock()
        MyRIPL.infer(i)
        print time.clock() - start_iter

fold = 1
for n_samples in [500]:
    for mh_iter in [10]:
        data = IRM(fold=fold,burn=int(np.floor(n_samples/2)),n_samples=n_samples,mh_iter=mh_iter,verbose=True)
