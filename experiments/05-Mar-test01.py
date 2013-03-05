{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/05-Mar-test01/',
'data_dirs' : ['../data/test/'],
'models' : [models.product_IRM],
'model_params' : [{'D' : 1, 'alpha' : 1, 'symmetric' : True}],
'n_samples' : 100,
'max_initial_run_time' : 30,
'max_burn_time' : 30,
'max_sample_time' : 30,
'intermediate_iter' : 1,
'core_type' : 'c1',
'cores_per_job' : 1,
'n_restarts' : 3
}
