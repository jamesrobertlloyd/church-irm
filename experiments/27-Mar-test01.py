{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/27-Mar-test01/',
'data_dirs' : ['../data/test/'],
'models' : [models.finite_LFRM_scheme]*5,
'model_params' : [{'D' : 1, 'alpha' : '(uniform-continuous 0.0001 3.0)'}, {'D' : 2, 'alpha' : '(uniform-continuous 0.0001 3.0)'}, {'D' : 3, 'alpha' : '(uniform-continuous 0.0001 3.0)'}, {'D' : 4, 'alpha' : '(uniform-continuous 0.0001 3.0)'}, {'D' : 5, 'alpha' : '(uniform-continuous 0.0001 3.0)'}],
'n_samples' : 100,
'max_initial_run_time' : 30,
'max_burn_time' : 60,
'max_sample_time' : 60,
'intermediate_iter' : 1,
'core_type' : 'c1',
'cores_per_job' : 1,
'n_restarts' : 3,
'local_computation' : False
}
