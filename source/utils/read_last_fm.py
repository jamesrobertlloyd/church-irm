from __future__ import division

import lastfm
import numpy as np
import os
import matplotlib
from pylab import *

def connect(api_key='fae2b5e3343b3051681261de9f4bdd06'):
    return lastfm.Api(api_key)
    
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

def plot_network(network):
    data = []
    for i in range(network.shape[1]):
        for j in range(network.shape[1]):
            data.append((i, j, network[i,j]))
    spy(data, range(network.shape[1]))
    
def social_network(users, names, max_out_degree=50):
    print 'Getting friends of users'
    for user in users:
        print 'Getting friends of %s' % user.name
        user.get_friends(limit=max_out_degree)
    print 'Building network'
    network = np.zeros((len(names), len(names)))
    for (i, user) in enumerate(users):
        for friend in user.get_friends(max_out_degree):
            if friend.name in names:
                # Find index of link
                j = names.index(friend.name)
                # Add friendship to network - enforce undirectedness
                network[i,j] = 1
                network[j,i] = 1
    plot_network(network)
    return network   
    
def user_tag_network(users, max_tags=50):
    print 'Getting tags'
    tags = []
    name_tags = []
    for user in users:
        print 'Getting tags of %s' % user.name
        tags.append(user.get_top_tags(limit=max_tags))
        name_tags = name_tags + [tag.name for tag in tags[-1]]
    name_tags = list(set(name_tags))
    print 'Building network'
    network = np.zeros((len(users), len(name_tags)))
    for (i, user) in enumerate(users):
        print 'Inputting data for user %s' % user.name
        for tag in tags[i]:
            # Find index of tag
            j = name_tags.index(tag.name)
            # Add count to network
            network[i,j] = tag.stats.count
    print 'Sorting network'
    counts = np.sum(network > 0, axis = 0)
    idx = list(reversed(list(counts.argsort()))) # Sorting map
    network = network[:,idx]
    return network
    

def egocentric_network_and_tags(username='abhin4v', max_out_degree=20, deg_of_sep=2, max_tags=50, max_combined_tags=20):
    api = connect()
    users = [api.get_user(username)]
    # Expand / collect network 
    for i in range(deg_of_sep):
        print '\nExpanding network to %d degree(s) of separation\n' % (i + 1)
        names = []
        for user in users:
            print 'Getting names of friends of %s' % user.name
            names = names + [user.name] + map(lambda friend: friend.name, user.get_friends(limit=max_out_degree))
        names = list(set(names)) # Could probably just always work with the set
        print '\nGetting users\n'
        users = [] # Inefficient but safe - I think lastfm does some caching so not too bad
        for name in names:
            print 'Getting %s' % name
            users = users + [api.get_user(name)]
    # Create social network
    network = social_network(users=users, names=names, max_out_degree=max_out_degree) 
    # Pretty picture
    #imshow(network)
    # Save social network
    file_name = 'lastfm_network_%s_%d_%d.csv' % (username, max_out_degree, deg_of_sep)
    print 'Saving network to file %s' % os.path.abspath(file_name)
    np.savetxt(file_name, network, delimiter=',')
    # Create tag network
    tag_network = user_tag_network(users=users, max_tags=max_tags)
    # Subset network
    tag_network = tag_network[:, range(max_combined_tags)]
    # Save tag network
    file_name = 'lastfm_user_tag_%s_%d_%d_%d_%d.csv' % (username, max_out_degree, deg_of_sep, max_tags, max_combined_tags)
    print 'Saving tag network to file %s' % os.path.abspath(file_name)
    np.savetxt(file_name, tag_network, delimiter=',')  
    file_name = 'lastfm_user_tag_bin_%s_%d_%d_%d_%d.csv' % (username, max_out_degree, deg_of_sep, max_tags, max_combined_tags)
    print 'Saving binary tag network to file %s' % os.path.abspath(file_name)
    np.savetxt(file_name, tag_network>0, delimiter=',') 
    return (users, names, network, tag_network)   
    
def main(max_out_degree=20, deg_of_sep=2):
    api = connect()
    users = [api.get_user('abhin4v')]
    # Expand / collect network 
    for i in range(deg_of_sep):
        print '\nExpanding network to %d degree(s) of separation\n' % (i + 1)
        names = []
        for user in users:
            print 'Getting names of friends of %s' % user.name
            names = names + [user.name] + map(lambda friend: friend.name, user.get_friends(limit=max_out_degree))
        names = list(set(names)) # Could probably just always work with the set
        print '\nGetting users\n'
        users = [] # Inefficient but safe - I think lastfm does some caching so not too bad
        for name in names:
            print 'Getting %s' % name
            users = users + [api.get_user(name)]
    # Create social network
    network = social_network(users=users, names=names, max_out_degree=max_out_degree) 

if __name__ == "__main__":
    print 'No main method - goodbye'
