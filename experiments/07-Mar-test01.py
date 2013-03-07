{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/07-Mar-test01/',
'data_dirs' : ['../data/test/'],
'models' : [models.product_IRM]*3,
'model_params' : [{'D' : 1, 'alpha' : 1, 'symmetric' : True}, {'D' : 1, 'alpha' : 1, 'symmetric' : True}, {'D' : 1, 'alpha' : 1, 'symmetric' : True}],
'n_samples' : 100,
'max_initial_run_time' : 30,
'max_burn_time' : 30,
'max_sample_time' : 30,
'intermediate_iter' : 1,
'core_type' : 'c1',
'cores_per_job' : 1,
'n_restarts' : 10,
'use_realtime_cores' : True,
'n_realtime_cores' : 10,
'max_realtime_time' : 0.1
}
