from __future__ import division, print_function

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets

from groundupml.supervised.linear_regression import LinearRegression
from groundupml.utils.data_manipulation import split_data


if __name__ == '__main__':
    NUM_SAMPLES = 500

    # Generate random correlated dataset
    X, y = datasets.make_regression(n_features=1, n_samples=NUM_SAMPLES,
                                    bias=50, noise=20, random_state=7901)
    # Split into test and training sets
    X_train, y_train, X_test, y_test = split_data(X, y, proportion=0.7)

    # Run gradient descent model
    lr_gd = LinearRegression(stochastic=True)
    lr_gd.fit(X_train, y_train)
    y_gd_pred = lr_gd.predict(X_test)

    # Run normal model
    lr_pi = LinearRegression(gradient_descent=False, reg_term=10)
    lr_pi.fit(X_train, y_train)
    y_pi_pred = lr_pi.predict(X_test)

    # Compute the model error
    mse_gd = np.mean(np.power(y_gd_pred - y_test, 2))
    mse_pi = np.mean(np.power(y_pi_pred - y_test, 2))

    # Plot the results
    f, (ax1, ax2) = plt.subplots(1, 2)

    ax1.scatter(X_test[:, 0], y_test)
    ax1.plot(X_test[:, 0], y_gd_pred)
    ax1.set_title('Linear Regression SGD (MSE: {:2f})'.format(
        mse_gd))

    ax2.scatter(X_test[:, 0], y_test)
    ax2.plot(X_test[:, 0], y_pi_pred)
    ax2.set_title('Linear Regression Pseudoinverse (MSE: {:2f})'.format(
        mse_pi))
    plt.show()
