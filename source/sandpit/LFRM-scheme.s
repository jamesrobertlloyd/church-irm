self.RIPL.assume('bias', parse('%s' % self.bias))
self.RIPL.assume('logistic', parse('(lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x)))))')) #### TODO - replace me ASAP
for d in range(self.D):
    # Instantiate feature probabilities
    #### FIXME - move alpha out of loop!
    self.RIPL.assume('alpha-%d' % d, parse('%s' % self.alpha))
    self.RIPL.assume('theta-%d' % d, parse('(beta (/ alpha-%d %d) 1)' % (d, self.D)))
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

####

(ASSUME bias (normal 0 1))
(ASSUME logistic (lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x))))))
(ASSUME alpha (unif 0 2))
(ASSUME sigma 1)

(ASSUME D 5)

(ASSUME iota (lambda (n)
                     (if (= n 0)
                         '()
                         (cons n (iota (- n 1))) ) ))

(ASSUME theta (mem (lambda (d) (beta (/ alpha D) 1))) ; Better parameterisation for changing D?
(ASSUME w (mem (lambda (d1 d2) (normal 0 sigma)))) ; What is the scaling of variance with D and N?
(ASSUME z (mem (lambda (n d) (bernoulli (theta d)))))
(ASSUME zwz (lambda (n1 n2) (apply +
                                   (map (lambda (d1)
                                                (apply +
                                                       (map (lambda (d2)
                                                                    (* (z n1 d1)
                                                                       (z n2 d2)
                                                                       (w d1 d2) ) )
                                                            (iota D) ) ) )
                                         (iota D) ) )) ; Can we exploit the sparsity of the calculation?
(ASSUME p (lambda (n1 n2) (logistic (+ bias (zwz n1 n2)))))
(ASSUME link (lambda (n1 n2) (bernoulli (p n1 n2))))

(OBSERVE (link 1 5) False)
...

####

(ASSUME bias (normal 0 1))
(ASSUME logistic (lambda (x) (/ 1 (+ 1 (power 2.71828 (- 0 x))))))
(ASSUME alpha (unif 0 2))
(ASSUME sigma 1)

(ASSUME D 5)

(ASSUME theta (mem (lambda (d) (beta (/ alpha D) 1))) ; Better parameterisation for changing D?
(ASSUME w (mem (lambda (d1 d2) (normal 0 sigma)))) ; What is the scaling of variance with D and N?
(ASSUME build-Z (lambda (d)
                        (if (= d 0)
                            '()
                            (if (bernoulli (theta d))
                                (cons d (build-Z (- d 1)))
                                (build-Z (- d 1)) ) ) ))
(ASSUME Z-n (mem (lambda (n) (build-Z D))))
(ASSUME zwz (lambda (n1 n2) (apply +
                                   (map (lambda (d1)
                                                (apply +
                                                       (map (lambda (d2)
                                                                    (w d1 d2) )
                                                            (Z-n n2) ) ) )
                                         (Z-n n1) ) )) ; Does this exploit sparsity?
(ASSUME p (lambda (n1 n2) (logistic (+ bias (zwz n1 n2)))))
(ASSUME link (lambda (n1 n2) (bernoulli (p n1 n2))))

(OBSERVE (link 1 5) False)
...
