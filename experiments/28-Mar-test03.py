{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/28-Mar-test03/',
'data_dirs' : ['../data/test/'],
'models' : [models.finite_LFRM_scheme]*1,
'model_params' : [{'D' : '(uniform-discrete 2 5)'}],
'n_samples' : 100,
'max_initial_run_time' : 30,
'max_burn_time' : 60,
'max_sample_time' : 60,
'intermediate_iter' : 1,
'core_type' : 'c2',
'cores_per_job' : 1,
'n_restarts' : 10,
'local_computation' : False
}
