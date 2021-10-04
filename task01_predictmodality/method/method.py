import logging

from scipy.sparse import csc_matrix

from .scmm import scMM

def main(input_train_mod1, input_train_mod2, input_test_mod1, input_train): # TODO: Why these args?
    logging.info("Training scMM...")
    model = scMM(mod1='RNA', mod2='ATAC')
    model.fit([input_train_mod1.X, input_train_mod2.X])

    logging.info("Predicting modality 2 from given modality 1 with scMM...")
    y_pred = model.predict_mod(mod1=input_test_mod1.X)

    y_pred = csc_matrix(y_pred)

    return y_pred
