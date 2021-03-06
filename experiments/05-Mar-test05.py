{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/05-Mar-test05/',
'data_dirs' : ['../data/test/'],
'models' : [models.product_IRM]*5,
'model_params' : [{'D' : 1, 'alpha' : 1, 'symmetric' : True}, {'D' : 2, 'alpha' : 1, 'symmetric' : True}, {'D' : 3, 'alpha' : 1, 'symmetric' : True}, {'D' : 4, 'alpha' : 1, 'symmetric' : True}, {'D' : 5, 'alpha' : 1, 'symmetric' : True}],
'n_samples' : 1000,
'max_initial_run_time' : 60,
'max_burn_time' : 60,
'max_sample_time' : 120,
'intermediate_iter' : 1,
'core_type' : 'c1',
'cores_per_job' : 1,
'n_restarts' : 10
}
