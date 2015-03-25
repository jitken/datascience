function idx = findClosestCentroids(X, centroids)
%FINDCLOSESTCENTROIDS computes the centroid memberships for every example
%   idx = FINDCLOSESTCENTROIDS (X, centroids) returns the closest centroids
%   in idx for a dataset X where each row is a single example. idx = m x 1 
%   vector of centroid assignments (i.e. each entry in range [1..K])
%

% Set K
K = size(centroids, 1);

% You need to return the following variables correctly.
idx = zeros(size(X,1), 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Go over every example, find its closest centroid, and store
%               the index inside idx at the appropriate location.
%               Concretely, idx(i) should contain the index of the centroid
%               closest to example i. Hence, it should be a value in the 
%               range 1..K
%
% Note: You can use a for-loop over the examples to compute this.
%
M = size(X,1);
N = size(X,2);

centroids_t = centroids';
centroids_unrolled = centroids_t(:);
centroids_repmat = repmat(centroids_unrolled,1,M);

X_repmat = repmat(X',K,1);

% Compute X - centroid.
X_m_centroids = X_repmat - centroids_repmat;
X_m_centroids_reshape = reshape(X_m_centroids,N,M*K);

% Computer |X - centroid| ^2
metric = sum(X_m_centroids_reshape.^2,1);
metric_reshape = reshape(metric,K,M);

% compute the closest centroid
[min_vals, indices] = min(metric_reshape,[],1);
idx = indices';


% =============================================================

end

