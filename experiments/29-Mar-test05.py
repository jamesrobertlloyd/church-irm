{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/29-Mar-test05/',
'data_dirs' : ['../data/lastfm_cs/'],
'models' : [models.social_collab_IRM]*3,
'model_params' : [{'D' : 1, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))'}, {'D' : 3, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))', {'D' : 5, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))'}],
'n_samples' : 100,
'max_initial_run_time' : 300,
'max_burn_time' : 600,
'max_sample_time' : 600,
'intermediate_iter' : 1,
'core_type' : 'f2',
'cores_per_job' : 1,
'n_restarts' : 10,
'local_computation' : False
}
