{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/03-Apr-test11/',
'data_dirs' : ['../data/another_lastfm_cs_test/'],
'models' : [models.social_collab_add_IRM]*2,
'model_params' : [{'D' : 1, 'alpha' : '1'}, {'D' : 5, 'alpha' : '1'}, {'D' : 9, 'alpha' : '1'}],
'n_samples' : 10,
'max_initial_run_time' : 30,
'max_burn_time' : 30,
'max_sample_time' : 30,
'intermediate_iter' : 1,
'core_type' : 'f2',
'cores_per_job' : 1,
'n_restarts' : 3,
'local_computation' : True,
'use_realtime_cores' : False,
'thread_wait' : 0.1
}
