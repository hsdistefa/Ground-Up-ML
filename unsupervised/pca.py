from __future__ import division, print_function

import math

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets


class PCA():
    def __init__(self, svd=True):
        """Principal Component Analysis

        Args:
            svd (:obj: `bool`, optional):
                If true use single value decomposition to calculate the
                transformation
        """
        self.svd = svd

    def transform(self, X, n_components):
        """Project X onto the n principal components of X

        Args:
            X (numpy array of shape [n_samples, n_features]):
                Data to be transformed
            n_components (int):
                Number of principal components to project the data onto
        """
        n_samples, n_features = X.shape

        # Re-center input at the origin
        X = X - np.mean(X, axis=0)

        # SVD Solution
        if self.svd:
            # Construct matrix Y such that Y^T Y is the covariance matrix
            Y = X / math.sqrt(n_samples - 1)

            # Compute singular value decomposition
            U, S, PC = np.linalg.svd(Y)

            # Pick the first n principal components that minimize redundancy
            PC = PC.T[:, :n_components]

        # Covariance matrix solution
        else:
            # Calculate the covariance matrix
            cov = X.T.dot(X) / (n_samples - 1)

            # Get the eigenvectors and eigenvalues of the covariance matrix
            # These eigenvectors are necessarily orthogonal since the covariance
            # matrix is symmetric
            eigenvalues, PC = np.linalg.eig(cov)

            # Sort the principal components (eigenvectors of cov-matrix) in
            # decreasing order by the magnitude of their eigenvalues
            # i.e. by how much they contribute to variance
            indices = np.argsort(eigenvalues)[::-1]
            PC = np.atleast_1d(PC[:, indices])

            # Pick the first n principal components that minimize redundancy
            PC = PC[:, :n_components]

        # Project input onto the n principal components
        return X.dot(PC)


def test():
    # Get Data
    data = datasets.load_digits()
    X = data.data
    y = data.target

    # Transform
    pca = PCA(svd=False)
    X_transformed = pca.transform(X, 2)
    pc1 = X_transformed[:, 0]
    pc2 = X_transformed[:, 1]

    # Plot
    plt.scatter(pc1, pc2, c=y)
    plt.title('Digits Dataset 0-9')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.show()


if __name__ == '__main__':
    test()
