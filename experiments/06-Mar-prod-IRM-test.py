{
'type' : 'network_cv',
'verbose' : False,
'results_dir' : '../results/06-Mar-prod-IRM-test/',
'data_dirs' : ['../data/irm_prod_synth/'],
'models' : [models.product_IRM]*10,
'model_params' : [{'D' : 1, 'alpha' : 1, 'beta' : 0.5, 'symmetric' : True}, \
                  {'D' : 2, 'alpha' : 1, 'beta' : 0.5, 'symmetric' : True}, \
                  {'D' : 3, 'alpha' : 1, 'beta' : 0.5, 'symmetric' : True}, \
                  {'D' : 4, 'alpha' : 1, 'beta' : 0.5, 'symmetric' : True}, \
                  {'D' : 5, 'alpha' : 1, 'beta' : 0.5, 'symmetric' : True}, \
                  {'D' : 1, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))', 'symmetric' : True}, \
                  {'D' : 2, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))', 'symmetric' : True}, \
                  {'D' : 3, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))', 'symmetric' : True}, \
                  {'D' : 4, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))', 'symmetric' : True}, \
                  {'D' : 5, 'alpha' : '(uniform-continuous 0.0001 2.0)', 'beta' : '(+ 0.5 (gamma 1.0 1.0))', 'symmetric' : True}],
'n_samples' : 500,
'max_initial_run_time' : 30,
'max_burn_time' : 30,
'max_sample_time' : 60,
'intermediate_iter' : 1,
'core_type' : 'c1',
'cores_per_job' : 1,
'n_restarts' : 10
}
