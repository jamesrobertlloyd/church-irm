{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/03-Apr-test06/',
'data_dirs' : ['../data/another_lastfm_cs_test/'],
'models' : [models.social_collab_add_IRM]*1,
'model_params' : [{'D' : 5, 'alpha' : '(uniform-continuous 0.0001 2.0)'}],
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
'thread_wait' : 5
}
