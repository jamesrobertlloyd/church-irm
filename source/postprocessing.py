'''Collation of results and related routines'''

import os
import pickle

import models

def print_basic_summary(results_dir):
    # Loop over model folders
    total_runtime = 0
    for model in sorted(os.listdir(results_dir)):
        for result in sorted(os.listdir(os.path.join(results_dir, model))):
            pickle_file = open(os.path.join(results_dir, model, result), 'rb')
            saved_results = pickle.load(pickle_file)
            pickle_file.close()
            print model, os.path.splitext(result)[0], 'ess = %04.f' % saved_results['ess'], 'AUC = %0.4f' % saved_results['AUC'], 'Memory = %04.f' % (saved_results['max_memory'] / (1024 * 1024))
            total_runtime += saved_results['runtime']
    print 'Total cpu time = %03.1f hours' % (total_runtime / 3600)

def print_stats(results_dir, fields=['ess', 'AUC']):
    # Loop over model folders
    total_runtime = 0
    for model in sorted(os.listdir(results_dir)):
        for result in sorted(os.listdir(os.path.join(results_dir, model))):
            pickle_file = open(os.path.join(results_dir, model, result), 'rb')
            saved_results = pickle.load(pickle_file)
            pickle_file.close()
            print model, os.path.splitext(result)[0],
            for field in fields:
                print '%s = %s' % (field, saved_results[field]),
            print
            total_runtime += saved_results['runtime']
    print 'Total cpu time = %03.1f hours' % (total_runtime / 3600)
