import logging

from scipy.sparse import csc_matrix

from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LinearRegression


def main(input_train_mod1, input_train_mod2, input_test_mod1, input_train):
    # Do PCA on the input data
    logging.info('Performing dimensionality reduction on modality 1 values...')
    embedder_mod1 = TruncatedSVD(n_components=50)
    mod1_pca = embedder_mod1.fit_transform(input_train.X)

    logging.info('Performing dimensionality reduction on modality 2 values...')
    embedder_mod2 = TruncatedSVD(n_components=50)
    mod2_pca = embedder_mod2.fit_transform(input_train_mod2.X)

    # split dimred back up
    X_train = mod1_pca[input_train.obs['group'] == 'train']
    X_test = mod1_pca[input_train.obs['group'] == 'test']
    y_train = mod2_pca

    assert len(X_train) + len(X_test) == len(mod1_pca)

    # Get all responses of the training data set to fit the
    # KNN regressor later on.
    #
    # Make sure to use `toarray()` because the output might
    # be sparse and `KNeighborsRegressor` cannot handle it.

    logging.info('Running Linear regression...')

    reg = LinearRegression()

    # Train the model on the PCA reduced modality 1 and 2 data
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    # Project the predictions back to the modality 2 feature space
    y_pred = y_pred @ embedder_mod2.components_

    # Store as sparse matrix to be efficient. Note that this might require
    # different classifiers/embedders before-hand. Not every class is able
    # to support such data structures.
    y_pred = csc_matrix(y_pred)

    return y_pred
