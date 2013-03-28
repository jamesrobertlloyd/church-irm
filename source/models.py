'''
Objects to create standard models and sample from them
'''

from venture_engine_requirements import *

class venture_model:
    '''For documentation purposes only'''
        
    def description(self):
        return 'Base model class'
    
    def create_RIPL(self):
        raise Exception('Not implemented')
        
    def observe_data(self, observations):
        raise Exception('Not implemented')
        
class product_IRM(venture_model):
    
    def __init__(self, D=1, alpha=1, beta=1, symmetric=True):
        self.D = D
        self.alpha = alpha
        self.beta = beta
        self.symmetric = symmetric
        
    def description(self):
        return 'Product_IRM_D=%s_alpha=%s_beta=%s_sym=%s' % (self.D, self.alpha, self.beta, self.symmetric)
        
    def create_RIPL(self):
        # Create RIPL and clear any previous session
        import venture_engine
        self.RIPL = venture_engine
        self.RIPL.clear()

        for d in range(self.D):
            # Instantiate CRP
            self.RIPL.assume('alpha-%d' % d, parse('%s' % self.alpha))
            self.RIPL.assume('cluster-crp-%d' % d, parse('(CRP/make alpha-%d)' % d))
            # Create class assignment lookup function
            self.RIPL.assume('node->class-%d' % d, parse('(mem (lambda (nodes) (cluster-crp-%d)))' % d))
            # Create class interaction probability lookup function
            #self.RIPL.assume('classes->parameters-%d' % d, parse('(mem (lambda (class1 class2) (beta %s %s)))' % (self.beta, self.beta))) 
            self.RIPL.assume('beta-a-%d' % d, parse('%s' % self.beta))
            self.RIPL.assume('beta-b-%d' % d, parse('%s' % self.beta))
            self.RIPL.assume('classes->parameters-%d' % d, parse('(mem (lambda (class1 class2) (beta beta-a-%d beta-b-%d)))' % (d, d))) 
         
        # Create relation probability function    
        self.RIPL.assume('p-friends', parse('(lambda (node1 node2) (* ' + ' '.join(['(classes->parameters-%d (node->class-%d node1) (node->class-%d node2))' % (d,d,d) for d in range(self.D)]) + '))')) 
        # Create relation evaluation function
        self.RIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 
       
    def observe_data(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        for (i,j,v) in observations:
            if v:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'true')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'true')
            else:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'false')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'false')
                    
    def set_predictions(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        truth = []
        missing_links = []
        for (i,j,v) in observations:
            truth.append(int(v))
            an_id = self.RIPL.predict(parse('(p-friends %d %d)' % (i, j)))[0]
            missing_links.append(an_id)
        return (truth, missing_links)
                    
class additive_IRM(venture_model):
    
    def __init__(self, D=1, alpha=1, bias='(normal 0 4)', sigma=1, symmetric=True):
        self.D = D
        self.alpha = alpha
        self.bias = bias
        self.sigma = sigma
        self.symmetric = symmetric
        
    def description(self):
        return 'Additive_IRM_D=%s_alpha=%s_bias=%s_sigma=%s_sym=%s' % (self.D, self.alpha, self.bias, self.sigma, self.symmetric)
        
    def create_RIPL(self):
        # Create RIPL and clear any previous session
        import venture_engine
        self.RIPL = venture_engine
        self.RIPL.clear()

        self.RIPL.assume('bias', parse('%s' % self.bias))
        self.RIPL.assume('logistic', parse('(lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x)))))')) #### TODO - replace me ASAP
        for d in range(self.D):
            # Instantiate CRP
            self.RIPL.assume('alpha-%d' % d, parse('%s' % self.alpha))
            self.RIPL.assume('cluster-crp-%d' % d, parse('(CRP/make alpha-%d)' % d))
            # Create class assignment lookup function
            self.RIPL.assume('node->class-%d' % d, parse('(mem (lambda (nodes) (cluster-crp-%d)))' % d))
            # Create class interaction probability lookup function
            #self.RIPL.assume('classes->parameters-%d' % d, parse('(mem (lambda (class1 class2) (normal 0 %s)))' % (self.sigma))) 
            self.RIPL.assume('sigma-%d' % d, parse('%s' % self.sigma))
            self.RIPL.assume('classes->parameters-%d' % d, parse('(mem (lambda (class1 class2) (normal 0 sigma-%d)))' % d)) 
         
        # Create relation probability function    
        self.RIPL.assume('p-friends', parse('(lambda (node1 node2) (logistic (+ bias ' + ' '.join(['(classes->parameters-%d (node->class-%d node1) (node->class-%d node2))' % (d,d,d) for d in range(self.D)]) + ')))')) 
        # Create relation evaluation function
        self.RIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 
       
    def observe_data(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        for (i,j,v) in observations:
            if v:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'true')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'true')
            else:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'false')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'false')
                    
    def set_predictions(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        truth = []
        missing_links = []
        for (i,j,v) in observations:
            truth.append(int(v))
            an_id = self.RIPL.predict(parse('(p-friends %d %d)' % (i, j)))[0]
            missing_links.append(an_id)
        return (truth, missing_links)
                    
class finite_LFRM(venture_model):
    
    def __init__(self, D=1, alpha=1, bias='(normal 0 4)', sigma=1, symmetric=True):
        self.D = D
        self.alpha = alpha
        self.bias = bias
        self.sigma = sigma
        self.symmetric = symmetric
        
    def description(self):
        return 'finite_LFRM_D=%s_alpha=%s_bias=%s_sigma=%s_sym=%s' % (self.D, self.alpha, self.bias, self.sigma, self.symmetric)
        
    def create_RIPL(self):
        # Create RIPL and clear any previous session
        import venture_engine
        self.RIPL = venture_engine
        self.RIPL.clear()

        self.RIPL.assume('bias', parse('%s' % self.bias))
        self.RIPL.assume('logistic', parse('(lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x)))))')) #### TODO - replace me ASAP
        self.RIPL.assume('alpha', parse('%s' % self.alpha))
        for d in range(self.D):
            # Instantiate feature probabilities
            self.RIPL.assume('theta-%d' % d, parse('(beta (/ alpha %d) 1)' % self.D))
            # Create feature assignment lookup function
            self.RIPL.assume('node->feature-%d' % d, parse('(mem (lambda (node) (bernoulli theta-%d)))' % d))
            
        # Create feature interaction probability lookup function
        self.RIPL.assume('sigma', parse('%s' % self.sigma))
        self.RIPL.assume('features->W', parse('(mem (lambda (feature1 feature2) (normal 0 sigma)))')) 
        # Create relation probability function - matrix multiplication with binary outer matrices   
        self.RIPL.assume('p-friends', parse('(lambda (node1 node2) (logistic (+ bias ' + \
                                                                                ' '.join(['(* (features->W %d %d) (node->feature-%d node1) (node->feature-%d node2))' \
                                                                                % (i,j,i,j) for i in range(self.D) for j in range(self.D)]) + ')))')) 
        # Create relation evaluation function
        self.RIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 
       
    def observe_data(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        for (i,j,v) in observations:
            if v:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'true')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'true')
            else:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'false')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'false')
                    
    def set_predictions(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        truth = []
        missing_links = []
        for (i,j,v) in observations:
            truth.append(int(v))
            an_id = self.RIPL.predict(parse('(p-friends %d %d)' % (i, j)))[0]
            missing_links.append(an_id)
        return (truth, missing_links)
                    
class var_finite_LFRM(venture_model):
    
    def __init__(self, D=1, alpha=1, bias='(normal 0 4)', sigma=1, symmetric=True):
        self.D = D
        self.alpha = alpha
        self.bias = bias
        self.sigma = sigma
        self.symmetric = symmetric
        
    def description(self):
        return 'var_finite_LFRM_D=%s_alpha=%s_bias=%s_sigma=%s_sym=%s' % (self.D, self.alpha, self.bias, self.sigma, self.symmetric)
        
    def create_RIPL(self):
        # Create RIPL and clear any previous session
        import venture_engine
        self.RIPL = venture_engine
        self.RIPL.clear()
        
        self.RIPL.assume('logistic', parse('(lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x)))))')) #### TODO - replace me ASAP
        self.RIPL.assume('list-sum', parse('(lambda (lst) (if (> (length lst) 1) (+ (first lst) (list-sum (rest lst))) (if (= (length lst) 1) (first lst) 0)))')) #### TODO - replace me if possible
        self.RIPL.assume('map', parse('(lambda (f lst) (if (empty? lst) (list) (cons (f (first lst)) (map f (rest lst)))))')) #### TODO - replace me if possible
        
        self.RIPL.assume('D', parse('%s' % self.D))
        self.RIPL.assume('alpha', parse('%s' % self.alpha))
        self.RIPL.assume('bias', parse('%s' % self.bias))
        self.RIPL.assume('sigma', parse('%s' % self.sigma))
        
        self.RIPL.assume('theta', parse('(mem (lambda (d) (beta (/ alpha D) 1)))'))
        self.RIPL.assume('w', parse('(mem (lambda (d1 d2) (normal 0 sigma)))'))
        
        self.RIPL.assume('build-Z', parse('(lambda (d) (if (= d 0) (list) (if (bernoulli (theta d)) (cons d (build-Z (- d 1))) (build-Z (- d 1)))))'))
        self.RIPL.assume('Z-n', parse('(mem (lambda (n) (build-Z D)))'))
        
        self.RIPL.assume('zwz', parse('(lambda (n1 n2) (list-sum (map (lambda (d1) (list-sum (map (lambda (d2) (w d1 d2)) (Z-n n2)))) (Z-n n1))))'))
        
        self.RIPL.assume('p-friends', parse('(lambda (n1 n2) (logistic (+ bias (zwz n1 n2))))'))
        self.RIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 
       
    def observe_data(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        for (i,j,v) in observations:
            if v:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'true')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'true')
            else:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'false')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'false')
                    
    def set_predictions(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        truth = []
        missing_links = []
        for (i,j,v) in observations:
            truth.append(int(v))
            an_id = self.RIPL.predict(parse('(p-friends %d %d)' % (i, j)))[0]
            missing_links.append(an_id)
        return (truth, missing_links)
        
class var_product_IRM(venture_model):
    
    def __init__(self, D=1, alpha=1, beta=1, symmetric=True):
        self.D = D
        self.alpha = alpha
        self.beta = beta
        self.symmetric = symmetric
        
    def description(self):
        return 'Product_IRM_D=%s_alpha=%s_beta=%s_sym=%s' % (self.D, self.alpha, self.beta, self.symmetric)
        
    def create_RIPL(self):
        # Create RIPL and clear any previous session
        import venture_engine
        self.RIPL = venture_engine
        self.RIPL.clear()
        
        self.RIPL.assume('logistic', parse('(lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x)))))')) #### TODO - replace me ASAP
        self.RIPL.assume('list-product', parse('(lambda (lst) (if (> (length lst) 1) (* (first lst) (list-product (rest lst))) (if (= (length lst) 1) (first lst) 1)))')) #### TODO - replace me if possible
        self.RIPL.assume('map', parse('(lambda (f lst) (if (empty? lst) (list) (cons (f (first lst)) (map f (rest lst)))))')) #### TODO - replace me if possible
        self.RIPL.assume('iota', parse('(lambda (n) (if (= n 0) (list) (cons n (iota (- n 1)))))')) #### TODO - replace me if possible
        
        self.RIPL.assume('D', parse('%s' % self.D))
        self.RIPL.assume('alpha', parse('(mem (lambda (d) %s))' % self.alpha))
        self.RIPL.assume('beta-a', parse('(mem (lambda (d) %s))' % self.beta))
        self.RIPL.assume('beta-b', parse('(mem (lambda (d) %s))' % self.beta))
        
        self.RIPL.assume('cluster-crp', parse('(mem (lambda (d) (CRP/make (alpha d))))'))
        
        self.RIPL.assume('node->class', parse('(mem (lambda (node d) ((cluster-crp d))))'))
        self.RIPL.assume('classes->parameters', parse('(mem (lambda (class1 class2 d) (beta (beta-a d) (beta-b d))))')) 
        self.RIPL.assume('nodes->parameters', parse('(lambda (node1 node2 d) (classes->parameters (node->class node1 d) (node->class node2 d) d))')) 
         
        # Create relation probability function    
        self.RIPL.assume('p-friends', parse('(lambda (node1 node2) (list-product (map (lambda (d) (nodes->parameters node1 node2 d)) (iota D))))'))
        # Create relation evaluation function
        self.RIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 
       
    def observe_data(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        for (i,j,v) in observations:
            if v:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'true')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'true')
            else:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'false')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'false')
                    
    def set_predictions(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        truth = []
        missing_links = []
        for (i,j,v) in observations:
            truth.append(int(v))
            an_id = self.RIPL.predict(parse('(p-friends %d %d)' % (i, j)))[0]
            missing_links.append(an_id)
        return (truth, missing_links)
                    
class finite_2class_ILA(venture_model):
    
    def __init__(self, D=1, alpha=1, bias='(normal 0 4)', sigma=1, symmetric=True):
        self.D = D
        self.alpha = alpha
        self.bias = bias
        self.sigma = sigma
        self.symmetric = symmetric
        
    def description(self):
        return 'finite_2class_ILA_D=%s_alpha=%s_bias=%s_sigma=%s_sym=%s' % (self.D, self.alpha, self.bias, self.sigma, self.symmetric)
        
    def create_RIPL(self):
        # Create RIPL and clear any previous session
        import venture_engine
        self.RIPL = venture_engine
        self.RIPL.clear()

        self.RIPL.assume('bias', parse('%s' % self.bias))
        self.RIPL.assume('logistic', parse('(lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x)))))')) #### TODO - replace me ASAP
        self.RIPL.assume('alpha', parse('%s' % self.alpha))
        for d in range(self.D):
            # Instantiate feature probabilities
            self.RIPL.assume('theta-%d' % d, parse('(beta (/ alpha %d) 1)' % self.D))
            # Create feature assignment lookup function
            self.RIPL.assume('node->feature-%d' % d, parse('(mem (lambda (node) (bernoulli theta-%d)))' % d))
            # Create class interaction probability lookup function
            self.RIPL.assume('sigma-%d' % d, parse('%s' % self.sigma))
            self.RIPL.assume('features->W-%d' % d, parse('(mem (lambda (feature1 feature2) (normal 0 sigma-%d)))' % d)) 
         
        # Create relation probability function    
        self.RIPL.assume('p-friends', parse('(lambda (node1 node2) (logistic (+ bias ' + ' '.join(['(features->W-%d (node->feature-%d node1) (node->feature-%d node2))' % (d,d,d) for d in range(self.D)]) + ')))')) 
        # Create relation evaluation function
        self.RIPL.assume('friends', parse('(lambda (node1 node2) (bernoulli (p-friends node1 node2)))')) 
       
    def observe_data(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        for (i,j,v) in observations:
            if v:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'true')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'true')
            else:
                self.RIPL.observe(parse('(friends %d %d)' % (i, j)), 'false')
                if self.symmetric:
                    self.RIPL.observe(parse('(friends %d %d)' % (j, i)), 'false')
                    
    def set_predictions(self, observations):
        '''Assumes triples of (i, j, v) for node i, node j and value v'''
        truth = []
        missing_links = []
        for (i,j,v) in observations:
            truth.append(int(v))
            an_id = self.RIPL.predict(parse('(p-friends %d %d)' % (i, j)))[0]
            missing_links.append(an_id)
        return (truth, missing_links)
