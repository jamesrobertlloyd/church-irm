'''Collation of results and related routines'''

import os
import pickle

import models

def print_all_AUCs(results_dir):
    # Loop over model folders
    for model in sorted(os.listdir(results_dir)):
        for result in sorted(os.listdir(os.path.join(results_dir, model))):
            pickle_file = open(os.path.join(results_dir, model, result), 'rb')
            saved_results = pickle.load(pickle_file)
            pickle_file.close()
            print model, os.path.splitext(result)[0], 'ess = %04.f' % saved_results['ess'], 'AUC = %0.4f' % saved_results['AUC'], 'Memory = %04.f' % (saved_results['max_memory'] / (1024 * 1024))
            for raw_result in saved_results['raw_results']:
                print '  %0.4f' % raw_result['AUC']

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
    
def latex_AUC_table(results_dir):
    # Create a dictionary indexed by models and data sets - the produce latex table
    models = sorted(os.listdir(results_dir))
    data_sets = []
    data = {}
    for model in sorted(os.listdir(results_dir)):
        data[model] = {}
        local_data_sets = sorted(os.listdir(os.path.join(results_dir, model)))
        data_sets = sorted(list(set(data_sets) | set(local_data_sets)))
        for data_set in local_data_sets:
            pickle_file = open(os.path.join(results_dir, model, data_set), 'rb')
            saved_results = pickle.load(pickle_file)
            pickle_file.close()
            data[model][data_set] = saved_results['AUC']
    # Dictionary is created, now produce LaTeX string
    latex_string = 'Model & %s \\\\\n\\hline\n' % ' & '.join(data_sets)
    print '          Model ',
    print ' '.join(['%s' % data_set[:10].ljust(10) for data_set in data_sets])
    for model in models:
        print '%s  %s' % (model[:15].ljust(15), ' '.join(['     %0.3f' % data[model][data_set] for data_set in data_sets]))
        latex_string = latex_string + model[:15] + ' & ' + ' & '.join(['%0.3f' % data[model][data_set] for data_set in data_sets]) + ' \\\\\n'
    print latex_string
