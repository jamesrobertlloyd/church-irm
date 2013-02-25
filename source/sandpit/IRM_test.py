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

def IRM(fold=1,burn=5,n_samples=10,mh_iter=100,verbose=True):

    # Start timing
    start = time.clock()

    # Create RIPL and clear any previous session
    MyRIPL = venture_engine
    MyRIPL.clear()

    # Load high school data set
    data = scipy.io.loadmat("../../data/hs/hs_%dof5.mat" % fold, squeeze_me=True)
    #data = scipy.io.loadmat("../../data/irm_synth/irm_synth_20.mat", squeeze_me=True)
    observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
    missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))

    class_prob_mode = 'logistic-3'

    # Helper functions
    #MyRIPL.assume('exp', parse('(lambda (x) (* (+ 1 (/ x 11)) (+ 1 (/ x 11)) (+ 1 (/ x 11)) (+ 1 (/ x 11)) (+ 1 (/ x 11)) (+ 1 (/ x 11)) (+ 1 (/ x 11)) (+ 1 (/ x 11)) (+ 1 (/ x 11)) (+ 1 (/ x 11)) (+ 1 (/ x 11))))'))
    #MyRIPL.assume('exp', parse('(lambda (x) (* (+ 1 (/ x 7)) (+ 1 (/ x 7)) (+ 1 (/ x 7)) (+ 1 (/ x 7)) (+ 1 (/ x 7)) (+ 1 (/ x 7)) (+ 1 (/ x 7))))'))
    #MyRIPL.assume('min-2', parse('(lambda (x y) (if (> x y) y x))'))
    #MyRIPL.assume('max-2', parse('(lambda (x y) (if (> x y) x y))'))
    #MyRIPL.assume('clip-p', parse('(lambda (x) (max-2 0.01 (min-2 0.99 x)))'))
    #MyRIPL.assume('exp', parse('(lambda (x) (expt 2.71828 x))'))
    MyRIPL.assume('logistic', parse('(lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x)))))'))
    #MyRIPL.assume('logistic-safe', parse('(lambda (x) (max-2 0.01 (min-2 0.99 (logistic x))))'))
    # Instantiate CRP
    MyRIPL.assume('alpha', parse('(uniform-continuous 0.0001 2.0)'))
    MyRIPL.assume('cluster-crp-1', parse('(CRP/make alpha)'))
    MyRIPL.assume('cluster-crp-2', parse('(CRP/make alpha)'))
    MyRIPL.assume('cluster-crp-3', parse('(CRP/make alpha)'))
    MyRIPL.assume('cluster-crp-4', parse('(CRP/make alpha)'))
    MyRIPL.assume('cluster-crp-5', parse('(CRP/make alpha)'))
    # Create class assignment lookup function
    MyRIPL.assume('node->class-1', parse('(mem (lambda (nodes) (cluster-crp-1)))'))
    MyRIPL.assume('node->class-2', parse('(mem (lambda (nodes) (cluster-crp-2)))'))
    MyRIPL.assume('node->class-3', parse('(mem (lambda (nodes) (cluster-crp-3)))'))
    MyRIPL.assume('node->class-4', parse('(mem (lambda (nodes) (cluster-crp-4)))'))
    MyRIPL.assume('node->class-5', parse('(mem (lambda (nodes) (cluster-crp-5)))'))
    # Create class interaction probability lookup function
    if class_prob_mode == 'beta':
        MyRIPL.assume('classes->parameters', parse('(mem (lambda (class1 class2) (beta 0.5 0.5)))')) 
        MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (classes->parameters (node->class-1 node1) (node->class-1 node2)))')) 
    elif class_prob_mode == 'logistic':
        #MyRIPL.assume('sigma-b', parse('(power 2.71828 (- 2 (uniform-continuous 0.001 4)))'))
        #MyRIPL.assume('bias', parse('(normal 0 (+ 0.5 (power 2.71828 (- 2 (uniform-continuous 0.001 4)))))'))
        MyRIPL.assume('bias', parse('(normal 0 2)'))
        #MyRIPL.assume('classes->weights', parse('(mem (lambda (class1 class2) (normal 0 1)))'))
        #MyRIPL.assume('classes->parameters', parse('(lambda (class1 class2) (logistic (+ bias (classes->weights class1 class2))))'))
        #MyRIPL.assume('sigma', parse('(+ 0.5 (power 2.71828 (- 2 (uniform-continuous 0.001 4))))'))
        MyRIPL.assume('sigma', parse('1'))
        MyRIPL.assume('classes->parameters', parse('(mem (lambda (class1 class2) (logistic (+ bias (normal 0 sigma)))))'))
        MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (classes->parameters (node->class-1 node1) (node->class-1 node2)))'))
    elif class_prob_mode == 'logistic-2':
        MyRIPL.assume('bias', parse('(normal 0 2)'))
        MyRIPL.assume('sigma-1', parse('1'))
        MyRIPL.assume('classes->weights-1', parse('(mem (lambda (class1 class2) (normal 0 sigma-1)))'))
        MyRIPL.assume('sigma-2', parse('1'))
        MyRIPL.assume('classes->weights-2', parse('(mem (lambda (class1 class2) (normal 0 sigma-2)))'))
        MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (logistic (+ bias (classes->weights-1 (node->class-1 node1) (node->class-1 node2)) (classes->weights-2 (node->class-2 node1) (node->class-2 node2)))))'))
    elif class_prob_mode == 'logistic-3':
        MyRIPL.assume('bias', parse('(normal 0 2)'))
        MyRIPL.assume('sigma-1', parse('1'))
        MyRIPL.assume('classes->weights-1', parse('(mem (lambda (class1 class2) (normal 0 sigma-1)))'))
        MyRIPL.assume('sigma-2', parse('1'))
        MyRIPL.assume('classes->weights-2', parse('(mem (lambda (class1 class2) (normal 0 sigma-2)))'))
        MyRIPL.assume('sigma-3', parse('1'))
        MyRIPL.assume('classes->weights-3', parse('(mem (lambda (class1 class2) (normal 0 sigma-3)))'))
        MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (logistic (+ bias (classes->weights-1 (node->class-1 node1) (node->class-1 node2)) (classes->weights-2 (node->class-2 node1) (node->class-2 node2)) (classes->weights-3 (node->class-3 node1) (node->class-3 node2)))))'))
    
    # Create relation evaluation function
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

    # Burn in
    #sample.collect_n_es(MyRIPL, n=burn, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], min_samples=n_samples*2, max_runtime=600, verbose=verbose)
    for unused in range(burn):
        mcmc_output = sample.collect_n_samples(MyRIPL, n=1, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], max_runtime=600, verbose=verbose)
        predictions = list(mcmc_output['samples'].mean(axis=1))
        roc_data = []
        for (true_link, prediction) in zip(truth, predictions):
            roc_data.append((true_link, prediction))
        print ROCData(roc_data).auc()
    # Collect samples
    #mcmc_output = sample.collect_n_es(MyRIPL, n=n_samples, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], min_samples=n_samples*2, max_runtime=300, verbose=verbose)
    #mcmc_output = sample.collect_n_samples(MyRIPL, n=n_samples, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], max_runtime=300, verbose=verbose)
    for unused in range(n_samples):
        mcmc_output = sample.collect_n_samples(MyRIPL, n=1, mh_iter=mh_iter, ids = [an_id for (an_id, _) in missing_links], max_runtime=600, verbose=verbose)
        predictions = list(mcmc_output['samples'].mean(axis=1))
        roc_data = []
        for (true_link, prediction) in zip(truth, predictions):
            roc_data.append((true_link, prediction))
        print ROCData(roc_data).auc()
    #samples = mcmc_output['samples']
    #sample_ess = mcmc_output['ess']

    if verbose:
        print 'Fold complete'
    #predictions = list(samples.mean(axis=1))
    #roc_data = []
    #for (true_link, prediction) in zip(truth, predictions):
    #    roc_data.append((true_link, prediction))
    #AUC = ROCData(roc_data).auc()
    #if verbose:
    #    print 'AUC = %f' % AUC
    
    #return {'truth' : truth, 'predictions' : predictions, 'samples' : samples, 'ess' : sample_ess, 'AUC' : AUC, 'runtime' : time.clock() - start}
    return 'Complete!'

data = IRM(fold=1,burn=0,n_samples=100,mh_iter=100,verbose=False)     
