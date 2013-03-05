'''Utilities relating to collecting samples'''

import time
import numpy as np

from utils import act
from utils.memory import memory

def collect_n_samples_before_timeout(RIPL, n, initial_mh_iter, ids, max_runtime=600, verbose=True):
    '''Alters the number of intermediate mh_iter to n samples in max_runtime'''
    #### FIXME - Dangerous - thinning depends on the state! - need to do a trial run!
    #### Maybe it does need linear regression to be awesome?
    #### TODO - start here
    samples = np.zeros((len(ids), 0))
    experiment_start = time.clock()
    start = time.clock()
    iteration = 0
    mh_iter = initial_mh_iter
    mh_sum = 0
    # For a maximum of n iterations
    for unused in range(n):
        if time.clock() - experiment_start < max_runtime:
            # Sample
            iteration += 1
            if (iteration > 10) and (iteration < n):
                # A few samples have been collected, adjust mh_iter to finish on time
                #### TODO - a filtering approach would be more adaptive
                now = time.clock()
                time_elapsed = now - start
                time_remaining = max_runtime - time_elapsed
                time_per_mh_iter = time_elapsed / mh_sum
                samples_remaining = n - iteration
                time_remaining_per_sample = time_remaining / samples_remaining
                mh_iter = max(1, int(round(time_remaining_per_sample / time_per_mh_iter)))
                if verbose:
                    print 'Time elapsed  ', time_elapsed
                    print 'Time remaining', time_remaining
                    print 'Time per mh   ', time_per_mh_iter
                    print 'Samples to go ', samples_remaining
                    print 'Time per samp.', time_remaining
                    print 'Remaining per.', time_remaining_per_sample
                    print 'mh_iter', mh_iter
            RIPL.infer(mh_iter)
            mh_sum += mh_iter
            if verbose:
                print 'Iteration %d' % iteration
            # Record sample
            samples = np.column_stack([samples, [RIPL.report_value(an_id) for an_id in ids]])
        else:
            break
    finish = time.clock()
    time_per_sample = max(finish - start, 0.01) / iteration
    if verbose:
        print '%d iterations : %f seconds : %f seconds per iteration' % (iteration, finish - start, time_per_sample)
    # Compute average ess
    start = time.clock()
    ess = np.mean([(samples.shape[1]) / act.batch_means(samples[i,:]) for i in range(samples.shape[0])])
    if np.isnan(ess) or np.isinf(ess):
        ess = 1
    finish = time.clock()
    time_to_compute_ess = max(finish - start, 0.01)
    if verbose:
        print 'ESS = %f : %f seconds' % (ess, time_to_compute_ess)
    else:
        #print 'ESS = %3.0f' % ess
        pass
    # Finished - return samples and ...TODO
    max_mem = memory()
    return {'samples' : samples, 'ess' : ess, 'max_memory' : max_mem}
    


def estimate_mh_time(RIPL, n, initial_mh_iter, ids, max_runtime=600, verbose=True):
    '''Uses a doubling strategy to try to estimate time per mh iter'''
    experiment_start = time.clock()
    start = time.clock()
    samples = np.zeros((len(ids), 0)) # These are recorded as normal for timing purposes
    iteration = 0
    mh_iter = initial_mh_iter
    mh_sum = 0
    max_mem = memory()
    while time.clock() - experiment_start < max_runtime:
        iteration += 1
        if verbose:
            print 'Sample %d : trying %d steps' % (iteration, mh_iter) 
        RIPL.infer(mh_iter)
        mh_sum += mh_iter
        samples = np.column_stack([samples, [RIPL.report_value(an_id) for an_id in ids]])
        if time.clock() - experiment_start < 10:
            # Not much time has passed - estimates will be unreliable - just double iterations
            mh_iter = mh_iter * 2
        else:
            # Some time has passed - make sure that next sample will not take too long
            now = time.clock()
            time_elapsed = now - start
            time_remaining = max_runtime - time_elapsed
            time_per_mh_iter = time_elapsed / mh_sum
            max_possible_iters = int(round(time_remaining / time_per_mh_iter))
            mh_iter = min(max(1, max_possible_iters), mh_iter * 2)
        max_mem = max(max_mem, memory())
    finish = time.clock()
    time_per_mh_iter = max(finish - start, 0.01) / mh_sum
    max_mem = max(max_mem, memory())
    return {'time_per_mh_iter' : time_per_mh_iter, 'max_memory' : max_mem}

def collect_n_samples(RIPL, n, mh_iter, ids, max_runtime=600, verbose=True):
    '''Tries to collect n samples before timeout'''
    samples = np.zeros((len(ids), 0))
    experiment_start = time.clock()
    start = time.clock()
    iteration = 0
    for unused in range(n):
        if time.clock() - experiment_start < max_runtime:
            # Sample
            iteration += 1
            RIPL.infer(mh_iter)
            if verbose:
                print 'Iteration %d' % iteration
            # Record sample
            samples = np.column_stack([samples, [RIPL.report_value(an_id) for an_id in ids]])
        else:
            break
    finish = time.clock()
    time_per_sample = max(finish - start, 0.01) / iteration
    if verbose:
        print '%d iterations : %f seconds : %f seconds per iteration' % (iteration, finish - start, time_per_sample)
    # Compute average ess
    start = time.clock()
    ess = np.mean([(samples.shape[1]) / act.batch_means(samples[i,:]) for i in range(samples.shape[0])])
    if np.isnan(ess) or np.isinf(ess):
        ess = 1
    finish = time.clock()
    time_to_compute_ess = max(finish - start, 0.01)
    if verbose:
        print 'ESS = %f : %f seconds' % (ess, time_to_compute_ess)
    else:
        #print 'ESS = %3.0f' % ess
        pass
    # Finished - return samples and ...TODO
    return {'samples' : samples, 'ess' : ess, 'runtime' : time.clock() - start}

def collect_n_es(RIPL, n, mh_iter, ids, min_samples=None, max_runtime=600, verbose=True):
    '''Tries to collect enough samples of ids to have an ess > n'''
    #### TODO - Note the min time of 0.01 and the 1 percent computation heuristic of 100
    ess = 0
    samples = np.zeros((len(ids), 0))
    trial_iterations = max(n, min_samples)
    experiment_start = time.clock()
    # While samples not large enough and not timed out
    while (np.floor(ess) + 1 < n) and (time.clock() - experiment_start < max_runtime):
        # Perform some iterations, recording how fast the sampler is running
        start = time.clock()
        iteration = 0
        for unused in range(trial_iterations):
            if time.clock() - experiment_start < max_runtime:
                # Sample
                iteration += 1
                RIPL.infer(mh_iter)
                # Record sample
                samples = np.column_stack([samples, [RIPL.report_value(an_id) for an_id in ids]])
        finish = time.clock()
        time_per_sample = max(finish - start, 0.01) / iteration
        if verbose:
            print '%d iterations : %f seconds : %f seconds per iteration' % (iteration, finish - start, time_per_sample)
        # Compute average ess
        start = time.clock()
        ess = np.mean([(samples.shape[1]) / act.batch_means(samples[i,:]) for i in range(samples.shape[0])])
        if np.isnan(ess) or np.isinf(ess):
            ess = 1
        finish = time.clock()
        time_to_compute_ess = max(finish - start, 0.01)
        if verbose:
            print 'ESS = %f : %f seconds' % (ess, time_to_compute_ess)
        else:
            #print 'ESS = %3.0f' % ess
            pass
        # Decide how long to sample for
        samples_per_effective_sample = samples.shape[1] / ess
        estimated_samples_required = samples_per_effective_sample * (n - ess)
        if np.isnan(estimated_samples_required) or np.isinf(estimated_samples_required):
            estimated_samples_required = 1
        else:
            estimated_samples_required = int(np.floor(estimated_samples_required))
        if verbose:
            print 'Estimated samples required %d' % estimated_samples_required
        balance_computation_samples = int(np.floor(100 * time_to_compute_ess / time_per_sample))
        if verbose:
            print '1%% samples %d' % balance_computation_samples
        trial_iterations = min(estimated_samples_required, balance_computation_samples)
        if verbose:
            print 'Sampling for %d' % trial_iterations
    # Finished - return samples and ...TODO
    return {'samples' : samples, 'ess' : ess}
        
        
