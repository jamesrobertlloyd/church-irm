{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/03-Apr-test01/',
'data_dirs' : ['../data/another_lastfm_cs_test/','../data/lastfm_cs/'],
'models' : [models.social_collab_add_IRM],
'model_params' : [{'D' : 1, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'sigma' : '(+ 0.01 (gamma 1 1))'}],
'n_samples' : 10,
'max_initial_run_time' : 30,
'max_burn_time' : 30,
'max_sample_time' : 30,
'intermediate_iter' : 1,
'core_type' : 'f2',
'cores_per_job' : 1,
'n_restarts' : 2,
'local_computation' : False,
'use_realtime_cores' : False,
'thread_wait' : 10
}
