seed=1; % fixing the seed of the random generators
randn('state',seed);
rand('state',seed);

network_file = '../../data/raw/lastfm_network_abhin4v_10_2.csv';
file_list = {'../../data/raw/lastfm_user_tag_bin_abhin4v_10_2_50_20_01of05_r.mat',...
             '../../data/raw/lastfm_user_tag_bin_abhin4v_10_2_50_20_02of05_r.mat',...
             '../../data/raw/lastfm_user_tag_bin_abhin4v_10_2_50_20_03of05_r.mat',...
             '../../data/raw/lastfm_user_tag_bin_abhin4v_10_2_50_20_04of05_r.mat',...
             '../../data/raw/lastfm_user_tag_bin_abhin4v_10_2_50_20_05of05_r.mat'};
         
A = csvread(network_file);
[n, m] = size(A);

social_train_i = [];
social_train_j = [];
social_train_v = [];

for ii = 1:n
    for jj = (ii+1):m
        social_train_i = [social_train_i; ii];
        social_train_j = [social_train_j; jj];
        social_train_v = [social_train_v; A(ii,jj)];
    end
end

for i = 1:length(file_list)
    data = load(file_list{i});
    collab_train_i = data.data.train_X_i{1};
    collab_train_j = data.data.train_X_j{1};
    collab_train_v = data.data.train_X_v{1};
    collab_test_i  = data.data.test_X_i{1};
    collab_test_j  = data.data.test_X_j{1};
    collab_test_v  = data.data.test_X_v{1};
    save([int2str(i) '.mat'], ...
         'social_train_i', 'social_train_j', 'social_train_v', ...
         'collab_train_i', 'collab_train_j', 'collab_train_v', ...
         'collab_test_i', 'collab_test_j', 'collab_test_v');
end