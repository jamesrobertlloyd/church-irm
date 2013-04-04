from __future__ import division

import lastfm
import numpy as np
import os
import matplotlib
from pylab import *
import random
import pickle

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
            #x.append(ordering[j-1] / n)
            #y.append(1 - ordering[i-1] / n)
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
    

def egocentric_network_and_tags(username='abhin4v', max_out_degree=20, max_friend_check=200, deg_of_sep=2, max_tags=50, max_combined_tags=20):
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
    network = social_network(users=users, names=names, max_out_degree=max_friend_check) 
    # Pretty picture
    #imshow(network)
    # Save social network
    #file_name = 'lastfm_network_%s_%d_%d.csv' % (username, max_out_degree, deg_of_sep)
    #print 'Saving network to file %s' % os.path.abspath(file_name)
    #np.savetxt(file_name, network, delimiter=',')
    # Create tag network
    tag_network = user_tag_network(users=users, max_tags=max_tags)
    # Subset network
    tag_network = tag_network[:, range(max_combined_tags)]
    # Save tag network
    #file_name = 'lastfm_user_tag_%s_%d_%d_%d_%d.csv' % (username, max_out_degree, deg_of_sep, max_tags, max_combined_tags)
    #print 'Saving tag network to file %s' % os.path.abspath(file_name)
    #np.savetxt(file_name, tag_network, delimiter=',')  
    #file_name = 'lastfm_user_tag_bin_%s_%d_%d_%d_%d.csv' % (username, max_out_degree, deg_of_sep, max_tags, max_combined_tags)
    #print 'Saving binary tag network to file %s' % os.path.abspath(file_name)
    #np.savetxt(file_name, tag_network>0, delimiter=',') 
    return (users, names, network, tag_network)  
    
def social_random_walk(username='abhin4v', steps=5, max_out_degree=20):
    api = connect()
    user = api.get_user(username)
    print 'Starting at %s' % user.name
    for dummy in range(steps):
        user = random.choice(user.get_friends(limit=max_out_degree))
        print 'Jumped to %s' % user.name
    return user.name
    
#def full2sparse(array, symmetric):
#    if not symmetric:
#        return [(i,j,v) for ((i,j),v) in np.ndenumerate(array)]
#    else:
#        return [(i,j,v) for ((i,j),v) in np.ndenumerate(array) if j > i]
    
def main(max_out_degree=20, steps=10, deg_of_sep=1, max_tags=100, max_combined_tags=20):
    success = False
    while not success:
        username = social_random_walk(steps=steps)
        (users, names, network, tag_network) = egocentric_network_and_tags(username=username, max_out_degree = max_out_degree, deg_of_sep=deg_of_sep, max_tags=max_tags, max_combined_tags=max_combined_tags)
        # Binarise the tags
        tag_network = tag_network > 0
        # Check the size of the network
        if network.shape[0] < max_out_degree:
            print 'Too few friends :('
        elif tag_network.mean < 0.2:
            print 'Too few tags'
        else:
            data = {}
            ii = []
            jj = []
            vv = []
            print 'Creating sparse network'
            for i in range(network.shape[0]):
                for j in range(i+1, network.shape[1]):
                    ii.append(i)
                    jj.append(j)
                    vv.append(network[i,j])
            data['social_train_i'] = np.array(ii)
            data['social_train_j'] = np.array(jj)
            data['social_train_v'] = np.array(vv)
            train_ii = []
            train_jj = []
            train_vv = []
            test_ii  = []
            test_jj  = []
            test_vv  = []
            train_rows = set(np.random.permutation(range(tag_network.shape[0]))[:int(floor(0.8*tag_network.shape[0]))])
            print 'Creating sparse tag network'
            for i in range(tag_network.shape[0]):
                for j in range(i+1, tag_network.shape[1]):
                    if i in train_rows:
                        train_ii.append(i)
                        train_jj.append(j)
                        train_vv.append(tag_network[i,j])
                    else:
                        test_ii.append(i)
                        test_jj.append(j)
                        test_vv.append(tag_network[i,j])
            data['collab_train_i'] = np.array(train_ii)
            data['collab_train_j'] = np.array(train_jj)
            data['collab_train_v'] = np.array(train_vv)
            data['collab_test_i'] = np.array(test_ii)
            data['collab_test_j'] = np.array(test_jj)
            data['collab_test_v'] = np.array(test_vv)
            save_file_name = os.path.join('../data/last_fm_cs_%d' % max_out_degree, '%s_%d.pickle' % (username, max_out_degree))
            print 'Saving data to %s' % save_file_name
            save_file_dir = os.path.split(save_file_name)[0]
            if not os.path.isdir(save_file_dir):
                os.makedirs(save_file_dir)
            with open(save_file_name, 'wb') as save_file:
                pickle.dump(data, save_file, -1)
            success = True
            plot_network(network)
            figure()
            plot_network(tag_network)
        

if __name__ == "__main__":
    main()
