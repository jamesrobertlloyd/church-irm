{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/03-Apr-cs/',
'data_dirs' : ['../data/lastfm_cs_5'],
'models' : [models.social_collab_add_IRM]*2 + [models.social_collab_prod_IRM]*2,
'model_params' : [{'D' : 1, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}, {'D' : 7, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}, {'D' : 1, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))'}, {'D' : 7, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))'}],
'n_samples' : 1000,
'max_initial_run_time' : 120,
'max_burn_time' : 600,
'max_sample_time' : 600,
'intermediate_iter' : 1,
'core_type' : 'f2',
'cores_per_job' : 1,
'n_restarts' : 20,
'local_computation' : False,
'use_realtime_cores' : False,
'thread_wait' : 5
}
