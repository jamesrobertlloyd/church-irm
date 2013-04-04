{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/03-Apr-test12/',
'data_dirs' : ['../data/last_fm_cs_20/'],
'models' : [models.social_collab_add_IRM]*3,
'model_params' : [{'D' : 1, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}, {'D' : 3, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}, {'D' : 5, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}],
'n_samples' : 100,
'max_initial_run_time' : 20,
'max_burn_time' : 300,
'max_sample_time' : 300,
'intermediate_iter' : 1,
'n_restarts' : 5,
'local_computation' : True,
'use_realtime_cores' : False,
'thread_wait' : 0.1
}
