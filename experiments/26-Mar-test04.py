{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/26-Mar-test04/',
'data_dirs' : ['../data/test/'],
'models' : [models.finite_LFRM]*5,
'model_params' : [{'D' : 1}, {'D' : 2}, {'D' : 3}, {'D' : 4}, {'D' : 5}],
'n_samples' : 100,
'max_initial_run_time' : 60,
'max_burn_time' : 300,
'max_sample_time' : 300,
'intermediate_iter' : 1,
'core_type' : 'c1',
'cores_per_job' : 1,
'n_restarts' : 10,
'local_computation' : False
}
