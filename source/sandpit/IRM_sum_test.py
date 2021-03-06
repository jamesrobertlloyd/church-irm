# Pretend to be in different directory
import sys
sys.path.append('../')

from venture_engine_requirements import *
import venture_engine

import scipy.io
import time
import numpy as np

from utils.pyroc import ROCData
import sample

def IRM(fold=1,burn=50,n_samples=100,mh_iter=1000,D=1,verbose=True):

    # Start timing
    start = time.clock()

    # Create RIPL and clear any previous session
    MyRIPL = venture_engine
    MyRIPL.clear()

    # Load high school data set
    data = scipy.io.loadmat("../../data/hs/hs_%dof5.mat" % fold, squeeze_me=True)
    observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
    missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))

    
    MyRIPL.assume('sigma', parse('1'))
    MyRIPL.assume('bias', parse('(normal 0 2)'))
    MyRIPL.assume('logistic', parse('(lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x)))))'))
    for d in range(D):
        # Instantiate CRP
        MyRIPL.assume('alpha-%d' % d, parse('(uniform-continuous 0.0001 2.0)'))
        MyRIPL.assume('cluster-crp-%d' % d, parse('(CRP/make alpha-%d)' % d))
        # Create class assignment lookup function
        MyRIPL.assume('node->class-%d' % d, parse('(mem (lambda (nodes) (cluster-crp-%d)))' % d))
        # Create class interaction probability lookup function
        MyRIPL.assume('classes->weights-%d' % d, parse('(mem (lambda (class1 class2) (normal 0 sigma)))'))
     
    # Create relation probability function    
    MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (logistic (+ bias ' + ' '.join(['(classes->weights-%d (node->class-%d node1) (node->class-%d node2))' % (d,d,d) for d in range(D)]) + ')))')) 
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
    mcmc_output = sample.collect_n_samples(MyRIPL, n=n_samples, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], max_runtime=1800, verbose=verbose)
    # Collect samples
    mcmc_output = sample.collect_n_samples(MyRIPL, n=n_samples, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], max_runtime=1800, verbose=verbose)
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
    
    return {'truth' : truth, 'predictions' : predictions, 'samples' : samples, 'ess' : sample_ess, 'AUC' : AUC, 'runtime' : time.clock() - start}

for D in [1,2,3]:
    for fold in [1,2,3,4,5]:
        results = IRM(fold=fold,burn=500,n_samples=1000,mh_iter=100,D=D,verbose=False)     
        print 'D = %d, fold = %d, ess = %f, AUC = %f, Runtime = %f' % (D, fold, results['ess'], results['AUC'], results['runtime'])
