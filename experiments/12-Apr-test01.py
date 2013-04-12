{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/12-Apr-test01/',
'data_dirs' : ['../data/lastfm_cs/'],
'models' : [models.social_collab_add_IRM]*2,
'model_params' : [{'D' : 1, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}, {'D' : 10, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}],
'n_samples' : 100,
'max_initial_run_time' : 300,
'max_burn_time' : 300,
'max_sample_time' : 300,
'intermediate_iter' : 1,
'core_type' : 'f2',
'cores_per_job' : 1,
'n_restarts' : 10,
'local_computation' : True
}
