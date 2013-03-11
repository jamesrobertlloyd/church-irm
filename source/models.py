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
        return 'Product_IRM_D=%d_alpha=%s_beta=%s_sym=%s' % (self.D, self.alpha, self.beta, self.symmetric)
        
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
    
    def __init__(self, D=1, alpha=1, bias='(normal 0 2)', sigma=1, symmetric=True):
        self.D = D
        self.alpha = alpha
        self.bias = bias
        self.sigma = sigma
        self.symmetric = symmetric
        
    def description(self):
        return 'Additive_IRM_D=%d_alpha=%s_bias=%s_sigma=%s_sym=%s' % (self.D, self.alpha, self.bias, self.sigma, self.symmetric)
        
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
