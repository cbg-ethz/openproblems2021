import logging

from scipy.sparse import csc_matrix

import matplotlib.pyplot as plt

from .scmm import scMM

EPOCHS: int = 5  # The number of training epochs for scMM


def summary_plots(model, input_train_mod1, input_train_mod2):
    # loss
    lossless_losslist = [e["train_loss"] for e in model.fit_stats]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(lossless_losslist)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    fig.savefig("loss.pdf")

    # trivial sanity check
    X_prediction_train_mod2 = model.predict_mod2(input_train_mod1)
    X_input_train_mod2 = input_train_mod2.layers["counts"].toarray()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(
        X_input_train_mod2.ravel(), X_prediction_train_mod2.ravel(), rasterized=True
    )
    fig.savefig("training_prediction.pdf")


def main(
    input_train_mod1, input_train_mod2, input_test_mod1, input_train
):  # TODO: Why these args?
    logging.info("Training scMM...")
    model = scMM(epochs=EPOCHS)
    model.fit(input_train_mod1, input_train_mod2)  # for now, RNA and ATAC

    logging.info("Predicting modality 2 from given modality 1 with scMM...")
    y_pred = model.predict_mod2(input_test_mod1)

    logging.info("Plotting summary statistics...")
    summary_plots(model, input_train_mod1, input_train_mod2)

    return csc_matrix(y_pred)

