{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/29-Mar-test02/',
'data_dirs' : ['../data/lastfm_cs/'],
'models' : [models.social_collab_IRM]*1,
'model_params' : [{'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))'}],
'n_samples' : 100,
'max_initial_run_time' : 30,
'max_burn_time' : 60,
'max_sample_time' : 60,
'intermediate_iter' : 1,
'core_type' : 'c1',
'cores_per_job' : 1,
'n_restarts' : 1,
'local_computation' : True
}
