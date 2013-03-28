{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/28-Mar-test06/',
'data_dirs' : ['../data/50_nodes/'],
'models' : [models.var_product_IRM]*1,
'model_params' : [{'D' : '(uniform-discrete 1 4)', 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))'}],
'n_samples' : 100,
'max_initial_run_time' : 30,
'max_burn_time' : 60,
'max_sample_time' : 60,
'intermediate_iter' : 1,
'core_type' : 'f2',
'cores_per_job' : 1,
'n_restarts' : 5,
'local_computation' : False
}
