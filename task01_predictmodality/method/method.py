import logging

from scipy.sparse import csc_matrix

from .scmm import scMM


def main(
    input_train_mod1, input_train_mod2, input_test_mod1, input_train
):  # TODO: Why these args?
    logging.info("Training scMM...")
    model = scMM(epochs=100)
    model.fit(input_train_mod1, input_train_mod2)  # for now, RNA and ATAC

    logging.info("Predicting modality 2 from given modality 1 with scMM...")
    y_pred = model.predict_mod2(input_test_mod1)

    return csc_matrix(y_pred)
