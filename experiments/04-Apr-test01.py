{
'type' : 'cold_start',
'verbose' : False,
'results_dir' : '../results/04-Apr-test11/',
'data_dirs' : ['../data/last_fm_cs_20/'],
'models' : [models.social_collab_add_IRM]*1,
'model_params' : [{'D' : 5, 'alpha' : '1'}],
'n_samples' : 10,
'max_initial_run_time' : 20,
'max_burn_time' : 15,
'max_sample_time' : 15,
'intermediate_iter' : 1,
'core_type' : 'c1',
'cores_per_job' : 1,
'n_restarts' : 2,
'local_computation' : False,
'use_realtime_cores' : False,
'thread_wait' : 0.1
}
