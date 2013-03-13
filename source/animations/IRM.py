#!/usr/bin/python
"""
Attempting to draw samples from an IRM
"""

from __future__ import division

import sys
sys.path.append('../')

import matplotlib
matplotlib.use('module://mplh5canvas.backend_h5canvas')
from pylab import *
import time
import utils.data
import random

#### Plotting stuff

def permutation_indices(data):
     return sorted(range(len(data)), key = data.__getitem__)

def spy(data, ordering, plt_fn=plot):
    n = max(max(i, j) for (i, j, v) in data)
    x = []
    y = []
    for (i, j, v) in data:
        if v:
            x.append(ordering[i-1] / n)
            y.append(1 - ordering[j-1] / n)
            x.append(ordering[j-1] / n)
            y.append(1 - ordering[i-1] / n)
    plt_fn(x, y, 'ro')
    current_cluster = min(clusters)
    if count > 0:
        for (i, node) in enumerate(permutation_indices(ordering)):
            if not clusters[node] == current_cluster:
                # Class boundary
                ax.axvline((i+0.5) / n)
                ax.axhline(1 - (i+0.5) / n)
            current_cluster = clusters[node]

def refresh_data(ax):
    spy(data['observations'], ordering, ax.plot)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    print count
    
# Load high school data and concatenate
#data = utils.data.load_network_cv_data('../../data/50_nodes/HighSchool_50.mat')
data = utils.data.load_network_cv_data('../../data/50_nodes/dolphins_50.mat')
data['observations'] = data['observations'] + data['missing']

# Subset as necessary

data['observations'] = [(i,j,v) for (i,j,v) in data['observations'] if (i <= 50) and (j <= 50)]
n = max(max(i, j) for (i, j, v) in data['observations'])
print n
ordering = range(1, n+1)
clusters = [0] * len(ordering)
print ordering

count = 0
spy(data['observations'], ordering, plot)
title('Adjacency matrix - sorted')
f = gcf()
ax = f.gca()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

#f2 = figure()
#ax2 = f2.gca()
#ax2.set_xlim(0, 1)
#ax2.set_ylim(0, 1)
#spy(data['observations'], ordering, ax2.plot)
#title('Adjacency matrix - unsorted')

#### Venture stuff

import client
import lisp_parser

Port = 5024
MyRIPL = client.RemoteRIPL("http://ec2-54-235-201-199.compute-1.amazonaws.com:" + str(Port))

# Delete previous sessions data.
MyRIPL.clear()

# Instantiate CRP
#MyRIPL.assume('alpha', lisp_parser.parse('(uniform-continuous 0.0001 2.0)'))
MyRIPL.assume('cluster-crp', lisp_parser.parse('(CRP/make 1)'))
# Instantiate cluster memberships
nodes = [MyRIPL.assume('node-%03d' % i, lisp_parser.parse('(cluster-crp)'))[0] for i in range(1, n+1)]
# Create class assignment lookup function
MyRIPL.assume('node->class', lisp_parser.parse('(mem (lambda (nodes) (cluster-crp)))'))
# Create class interaction probability lookup function
MyRIPL.assume('classes->parameters', lisp_parser.parse('(mem (lambda (class1 class2) (beta 1 1)))'))

# Observe stuff
for (i,j,v) in data['observations']:
    print 'Observing (%3d, %3d) = %s' % (i, j, v)
    if v:
      MyRIPL.observe(lisp_parser.parse('(bernoulli (classes->parameters node-%03d node-%03d))' % (i, j)), 'true')
      MyRIPL.observe(lisp_parser.parse('(bernoulli (classes->parameters node-%03d node-%03d))' % (j, i)), 'true')
    else:
      MyRIPL.observe(lisp_parser.parse('(bernoulli (classes->parameters node-%03d node-%03d))' % (i, j)), 'false')
      MyRIPL.observe(lisp_parser.parse('(bernoulli (classes->parameters node-%03d node-%03d))' % (j, i)), 'false')

# Plotting loop

show(block=False)
 # show the figure manager but don't block script execution so animation works..
while True:
    print 'Telling Venture to infer'
    MyRIPL.infer(1000, rerun=False, threadsNumber=1)
    print 'Inference complete'
    clusters = [MyRIPL.report_value(node) for node in nodes]
    print clusters
    n_clusters = max(clusters) + 1
    ordering_count = 1
    for c in range(n_clusters):
        for (i, cluster) in random.sample(list(enumerate(clusters)), len(clusters)):
            if cluster == c:
                ordering[i] = ordering_count
                ordering_count += 1
    cla()
    refresh_data(ax)
    f.canvas.draw()
    count += 1
    time.sleep(0.5)
