from venture_engine_requirements import *
import venture_engine

import numpy as np
from utils.pyroc import ROCData
from utils import act
import scipy.io

def IRM_HighSchool(fold=1,burn=50,n_samples=100,mh_iter=100,verbose=True):

    # Create RIPL and clear any previous session
    MyRIPL = venture_engine
    MyRIPL.clear()

    # Load high school data set
    data = scipy.io.loadmat("../data/hs/hs_%dof5.mat" % fold, squeeze_me=True)
    observed = list(zip(data['train_i'].flat, data['train_j'].flat, data['train_v'].flat))
    missing  = list(zip(data['test_i'].flat,  data['test_j'].flat,  data['test_v'].flat))

    # Convenience functions
    MyRIPL.assume('min-2', parse('(lambda (x y) if (< x y) x y)'))
    MyRIPL.assume('max-2', parse('(lambda (x y) if (> x y) x y)'))
    # Instantiate CRP
    MyRIPL.assume('alpha', parse('(uniform-continuous 0.0001 2.0)'))
    MyRIPL.assume('cluster-crp', parse('(CRP/make alpha)'))
    # Create class assignment lookup function
    MyRIPL.assume('node->class', parse('(mem (lambda (nodes) (cluster-crp)))'))
    # Create class interaction probability lookup function
    MyRIPL.assume('classes->parameters', parse('(mem (lambda (class1 class2) (beta 0.5 0.5)))')) 
    MyRIPL.assume('classes->parameters-symmetric', parse('(lambda (class1 class2) (classes->parameters (min-2 class1 class2) (max-2 class1 class2)))')) 
    # Create relation evaluation function
    MyRIPL.assume('p-friends', parse('(lambda (node1 node2) (classes->parameters-symmetric (node->class node1) (node->class node2)))')) 
    MyRIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 

    # Tell Venture about observations
    for (i,j,v) in observed:
        if verbose:
            print 'Observing (%3d, %3d) = %d' % (i, j, v)
        if v:
            MyRIPL.observe(parse('(friends %d %d)' % (i, j)), 'true')
        else:
            MyRIPL.observe(parse('(friends %d %d)' % (i, j)), 'false')
                
    # Tell Venture that we want to predict P(unobserved link)
    truth = []
    missing_links = []
    for (i,j,v) in missing:
        if verbose:
            print 'Predicting (%3d, %3d) = %d' % (i, j, v)
        truth.append(int(v))
        missing_links.append(MyRIPL.predict(parse('(p-friends %d %d)' % (i, j))))

    # Perform inference
    for sample_number in range(burn):
        MyRIPL.infer(mh_iter)
        print 'Burn in sample %4d' % (sample_number + 1)
        roc_data = []
        for (true_link, (missing_link, _)) in zip(truth, missing_links):
            roc_data.append((true_link, MyRIPL.report_value(missing_link)))
        print ROCData(roc_data).auc()
    samples = np.zeros((len(truth), 0))
    #ess_samples = []
    for sample_number in range(n_samples):
        MyRIPL.infer(mh_iter)
        print 'Sample %4d' % (sample_number + 1)
        roc_data = []
        for (true_link, (missing_link, _)) in zip(truth, missing_links):
            roc_data.append((true_link, MyRIPL.report_value(missing_link)))
        samples = np.column_stack([samples, [roc_datum[1] for roc_datum in roc_data]])
        ess = (sample_number + 1) / act.batch_means(samples[0,:])
        print ess
        print ROCData(roc_data).auc()

    print 'Fold complete'
    predictions = list(samples.mean(axis=1))
    roc_data = []
    for (true_link, prediction) in zip(truth, predictions):
        roc_data.append((true_link, prediction))
    AUC = ROCData(roc_data).auc()
    print 'AUC = %f' % AUC
    
    return {'truth' : truth, 'predictions' : predictions, 'samples' : samples, 'AUC' : AUC}

folds = 5    
AUC_sum = 0
for fold in range(1,folds+1,1):
    print 'Fold %d' % fold
    AUC_sum = AUC_sum + IRM_HighSchool(fold=fold,burn=5,n_samples=100,mh_iter=10,verbose=False)['AUC']
print 'Average AUC = %f' % (AUC_sum / folds)
