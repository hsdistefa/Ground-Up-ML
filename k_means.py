import numpy as np


class KMeans():
    def __init__(self, k, max_iterations=1000):
        self.k = k
        self.max_iterations = max_iterations

    def fit(self, X):
        # Initialize centroids
        centroids = self._initialize_centroids(X)
        prev_centroids = np.zeros(self.k)
        # Iterate only until convergence or max iterations
        for _ in range(self.max_iterations):
            # Has converged if the centroids haven't changed
            difference = centroids - prev_centroids
            if not difference.any():
                break

            # Assign each point to the closest centroid
            clusters = self._get_clusters(centroids, X)

            # Calculate new centroids
            prev_centroids = centroids
            centroids = self._get_new_centroids(clusters, X)
        return self._get_cluster_labels(clusters, X)

    def _get_clusters(self, centroids, X):
        # Create clusters by assigning each point to the nearest centroid
        clusters = [[] for _ in range(self.k)]
        for i, x in enumerate(X):
            closest_dist = float('inf')
            closest_index = None
            for j, c in enumerate(centroids):
                dist = self._euclidean_distance(x, c)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_index = j
            clusters[closest_index].append(x)  # possibly memory inefficient
        return clusters

    def _get_cluster_labels(self, clusters, X):
        n_samples, _ = np.shape(X)
        labels = np.zeros(n_samples, dtype=np.int32)
        for cluster_i, cluster in enumerate(clusters):
            for point_i, _ in enumerate(cluster):
                labels[point_i] = cluster_i
        return labels

    def _get_new_centroids(self, clusters, X):
        # Calculate new centroids by taking the mean of each cluster
        _, n_features = np.shape(X)
        centroids = np.zeros((self.k, n_features))
        for i, cluster in enumerate(clusters):
            centroids[i] = np.mean(cluster, axis=0)
        return centroids

    def _initialize_centroids(self, X):
        # TODO: Random Partition, k-means++, minimax initialization
        # Forgy initialization
        #   i.e. Choose random points from X as initial centroids
        n_samples, n_features = np.shape(X)
        centroids = np.zeros((self.k, n_features))
        for i in range(len(centroids)):
            centroids[i] = X[np.random.choice(range(n_samples))]
        return centroids

    def _euclidean_distance(self, x1, x2):
        return np.linalg.norm(x1 - x2)


def test():
    # TODO: more in depth testing
    np.random.seed(10001)
    X = np.arange(10).reshape(5, 2)
    km = KMeans(2, max_iterations=1)
    print(X)
    print(km.fit(X))


if __name__ == '__main__':
    test()
