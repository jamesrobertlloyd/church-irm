%% Generate synthetic data from IRM style models

seed=0; % fixing the seed of the random generators
randn('state',seed);
rand('state',seed);

n = 2 * 3 * 5 * 3;
obs_mask = rand(n, n) < 0.8;

%% Basic block model

clusters_1 = [1 * ones(n / 2, 1) ; 2 * ones(n / 2, 1)];
W_1 = betarnd(0.5*ones(2), 0.5*ones(2));
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
      train_v = [train_v; (W_1(clusters_1(i),clusters_1(j)) > rand) * 1];
    else
      test_i = [test_i; i];
      test_j = [test_j; j];
      test_v = [test_v; (W_1(clusters_1(i),clusters_1(j)) > rand) * 1];
    end
  end
end

save('prod_irm_1_synth.mat', 'train_i', 'train_j', 'train_v', 'test_i', 'test_j', 'test_v');

%% Block model squared

clusters_2 = [1 * ones(n / 3, 1) ; 2 * ones(n / 3, 1);
              3 * ones(n / 3, 1)];
W_2 = betarnd(1.0*ones(3), 0.5*ones(3));
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
      train_v = [train_v; (W_1(clusters_1(i),clusters_1(j)) * W_2(clusters_2(i),clusters_2(j)) > rand) * 1];
    else
      test_i = [test_i; i];
      test_j = [test_j; j];
      test_v = [test_v; (W_1(clusters_1(i),clusters_1(j)) * W_2(clusters_2(i),clusters_2(j)) > rand) * 1];
    end
  end
end

save('prod_irm_2_synth.mat', 'train_i', 'train_j', 'train_v', 'test_i', 'test_j', 'test_v');

%% Block model cubed

clusters_3 = [1 * ones(n / 5, 1) ; 2 * ones(n / 5, 1);
              3 * ones(n / 5, 1) ; 4 * ones(n / 5, 1);
              5 * ones(n / 5, 1)];
W_3 = betarnd(3.0*ones(5), 1.0*ones(5));
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
      train_v = [train_v; (W_1(clusters_1(i),clusters_1(j)) * W_2(clusters_2(i),clusters_2(j)) * W_3(clusters_3(i),clusters_3(j)) > rand) * 1];
    else
      test_i = [test_i; i];
      test_j = [test_j; j];
      test_v = [test_v; (W_1(clusters_1(i),clusters_1(j)) * W_2(clusters_2(i),clusters_2(j)) * W_3(clusters_3(i),clusters_3(j)) > rand) * 1];
    end
  end
end

save('prod_irm_3_synth.mat', 'train_i', 'train_j', 'train_v', 'test_i', 'test_j', 'test_v');
