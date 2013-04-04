seed=1; % fixing the seed of the random generators
randn('state',seed);
rand('state',seed);

directory = '../../data/temp/';

%n = 50;
fold_directory = '../../data/full_networks/';

prop_observed = 1.0;
file_list = dir(directory);

%n_obs = n * (n - 1) / 2;

for i = 1:length(file_list)
    
    randn('state',seed);
    rand('state',seed);
    
    a_file = file_list(i);
    if ~a_file.isdir
        A = csvread([directory a_file.name]);
        
        n = size(A, 1);
        n_obs = n * (n - 1) / 2;
        
        perm = randperm(n_obs);
        mask = zeros(n_obs, 1);
        for ii = 1:(n_obs*prop_observed)
            mask(perm(ii)) = 1;
        end
        
        train_i = [];
        train_j = [];
        train_v = [];
        test_i = [];
        test_j = [];
        test_v = [];
        count = 1;
        for ii = 1:n
            for jj = (ii+1):n
                if mask(count)
                    train_i = [train_i; ii];
                    train_j = [train_j; jj];
                    train_v = [train_v; A(ii,jj)];
                else
                    test_i = [test_i; ii];
                    test_j = [test_j; jj];
                    test_v = [test_v; A(ii,jj)];
                end
                count = count + 1;
            end
        end
        
        [~, data_name, ~] = fileparts(a_file.name);
        save_file_name = [fold_directory, data_name, '.mat'];
        save(save_file_name, 'train_i', 'train_j', 'train_v', 'test_i', 'test_j', 'test_v');
    end
end