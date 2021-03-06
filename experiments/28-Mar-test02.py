{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/28-Mar-test02/',
'data_dirs' : ['../data/50_nodes/'],
'models' : [models.finite_LFRM_scheme]*5,
'model_params' : [{'D' : 2, 'alpha' : '(uniform-continuous 0.0001 3.0)'}, {'D' : 4, 'alpha' : '(uniform-continuous 0.0001 3.0)'}, {'D' : 6, 'alpha' : '(uniform-continuous 0.0001 3.0)'}, {'D' : 8, 'alpha' : '(uniform-continuous 0.0001 3.0)'}, {'D' : 10, 'alpha' : '(uniform-continuous 0.0001 3.0)'}],
'n_samples' : 100,
'max_initial_run_time' : 30,
'max_burn_time' : 60,
'max_sample_time' : 60,
'intermediate_iter' : 1,
'core_type' : 'f2',
'cores_per_job' : 1,
'n_restarts' : 2,
'local_computation' : False
}
