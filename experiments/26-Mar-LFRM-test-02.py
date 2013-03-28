{
'comment' : 'Second test of LFRM',
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/26-Mar-LFRM-02/',
'data_dirs' : ['../data/50_nodes/'],
'models' : [models.finite_LFRM] * 2,
'model_params' : [{'D' : 3}, {'D' : 4}, {'D' : 5}],
'n_samples' : 1000,
'max_initial_run_time' : 300,
'max_burn_time' : 1200,
'max_sample_time' : 1200,
'intermediate_iter' : 1,
'core_type' : 'c2',
'cores_per_job' : 1,
'n_restarts' : 10,
'use_realtime_cores' : False,
'n_realtime_cores' : 25,
'max_realtime_time' : 1,
'release_realtime_cores' : False,
'local_computation' : False
}