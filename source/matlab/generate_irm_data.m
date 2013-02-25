%% Generate synthetic data from IRM style model

seed=0; % fixing the seed of the random generators
randn('state',seed);
rand('state',seed);

n = 20;
clusters = [1 * ones(n / 4, 1) ; 2 * ones(n / 4, 1); ...
            3 * ones(n / 4, 1) ; 4 * ones(n / 4, 1)];
obs_mask = rand(n, n) < 0.8;
W = betarnd(0.5*ones(4), 0.5*ones(4));
train_i = [];
train_j = [];
train_v = [];
test_i = [];
test_j = [];
test_v = [];
for i = 1:n
  for j = (i+1):n
    if obs_mask(i,j)
      train_i = [train_i; i];
      train_j = [train_j; j];
      train_v = [train_v; (W(clusters(i),clusters(j)) < rand) * 1];
    else
      test_i = [test_i; i];
      test_j = [test_j; j];
      test_v = [test_v; (W(clusters(i),clusters(j)) < rand) * 1];
    end
  end
end

save('irm_synth.mat', 'train_i', 'train_j', 'train_v', 'test_i', 'test_j', 'test_v');
