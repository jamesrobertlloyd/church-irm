{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/28-Mar-LFRM/',
'data_dirs' : ['../data/50_nodes/'],
'models' : [models.var_finite_LFRM],
'model_params' : [{'D' : '(uniform-discrete 2 8)', 'alpha' : '(uniform-continuous 0.0001 3.0)'}],
'n_samples' : 100,
'max_initial_run_time' : 300,
'max_burn_time' : 1200,
'max_sample_time' : 1200,
'intermediate_iter' : 1,
'core_type' : 'f2',
'cores_per_job' : 1,
'n_restarts' : 10,
'local_computation' : False
}
