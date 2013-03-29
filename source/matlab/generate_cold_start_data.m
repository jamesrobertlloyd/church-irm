%% Generate synthetic data from IRM style model for cold start problem

seed=0; % fixing the seed of the random generators
randn('state',seed);
rand('state',seed);

n = 20;
social_clusters = [1 * ones(n / 4, 1) ; 2 * ones(n / 4, 1); ...
            3 * ones(n / 4, 1) ; 4 * ones(n / 4, 1)];
social_obs_mask = rand(n, n) < 1.1;
W = betarnd(1*ones(4), 1*ones(4));
social_train_i = [];
social_train_j = [];
social_train_v = [];
social_test_i = [];
social_test_j = [];
social_test_v = [];
for i = 1:n
  for j = (i+1):n
    if social_obs_mask(i,j)
      social_train_i = [social_train_i; i];
      social_train_j = [social_train_j; j];
      social_train_v = [social_train_v; (W(social_clusters(i),social_clusters(j)) < rand) * 1];
    else
      social_test_i = [social_test_i; i];
      social_test_j = [social_test_j; j];
      social_test_v = [social_test_v; (W(social_clusters(i),social_clusters(j)) < rand) * 1];
    end
  end
end

m = 30;
item_clusters = [1 * ones(m / 2, 1) ; 2 * ones(m / 2, 1)];
item_obs_mask = rand(n, 1) < 0.8;
W = betarnd(1*ones(4, 2), 1*ones(4, 2));
collab_train_i = [];
collab_train_j = [];
collab_train_v = [];
collab_test_i = [];
collab_test_j = [];
collab_test_v = [];
for i = 1:n
  for j = 1:m
    if item_obs_mask(i)
      collab_train_i = [collab_train_i; i];
      collab_train_j = [collab_train_j; j];
      collab_train_v = [collab_train_v; (W(social_clusters(i),item_clusters(j)) < rand) * 1];
    else
      collab_test_i = [collab_test_i; i];
      collab_test_j = [collab_test_j; j];
      collab_test_v = [collab_test_v; (W(social_clusters(i),item_clusters(j)) < rand) * 1];
    end
  end
end

save('cold_start_synth.mat', 'social_train_i', 'social_train_j',...
     'social_train_v', 'social_test_i', 'social_test_j', 'social_test_v',...
     'collab_train_i', 'collab_train_j',...
     'collab_train_v', 'collab_test_i', 'collab_test_j', 'collab_test_v');
