{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/28-Mar-test05/',
'data_dirs' : ['../data/test/'],
'models' : [models.var_product_IRM]*5,
'model_params' : [{'D' : 1}, {'D' : 2}, {'D' : 3}, {'D' : 4}, {'D' : 5}],
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
