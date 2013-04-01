{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/01-Apr-test04/',
'data_dirs' : ['../data/lastfm_cs/'],
'models' : [models.social_collab_add_IRM]*2,
'model_params' : [{'D' : 1, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}, {'D' : 10, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}],
'n_samples' : 100,
'max_initial_run_time' : 60,
'max_burn_time' : 60,
'max_sample_time' : 60,
'intermediate_iter' : 1,
'core_type' : 'f2',
'cores_per_job' : 1,
'n_restarts' : 100,
'local_computation' : False
}
