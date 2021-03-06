{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/08-Mar-prod-IRM-size-test/',
'data_dirs' : ['../data/irm_prod_synth_size_test/'],
'models' : [models.product_IRM]*1,
'model_params' : [{'D' : 2, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))', 'symmetric' : True}],
'n_samples' : 1000,
'max_initial_run_time' : 300,
'max_burn_time' : 1800,
'max_sample_time' : 1800,
'intermediate_iter' : 1,
'core_type' : 'c2',
'cores_per_job' : 1,
'n_restarts' : 10,
'use_realtime_cores' : False,
'n_realtime_cores' : 1,
'max_realtime_time' : 0,
'release_realtime_cores' : True
}
