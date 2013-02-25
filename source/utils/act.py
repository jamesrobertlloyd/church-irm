'''Routines for estimating auto correlation times'''

import numpy as np

def batch_means(X, batch_size=None):
    '''Computes ACT of X (assumed to be 1d np.array) using batch means method'''
    # Convert to array
    X = np.array(X)
    if batch_size == None:
        # Use default of n**(1/2)
        #### FIXME - Heuristic based on Radford Neal via Madeleine Thompson is n**(2/3) but this seems really high variance
        batch_size = np.floor(X.size ** (1.0 / 2.0))
    # Compute sample variance and sample variance of batch means
    sample_variance = np.std(X) ** 2
    sample_variance_batch_means = np.std([np.mean(X[(batch*batch_size):((batch+1)*batch_size - 1)]) for batch in range(int(np.floor(X.size / batch_size)))]) ** 2
    # Estimate ACT
    return batch_size * sample_variance_batch_means / sample_variance
    

