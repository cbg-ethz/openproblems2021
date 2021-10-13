from dataclasses import dataclass
from collections import defaultdict

import numpy as np

import torch
from torch import optim

from .vaes import VAE_rna_atac
from .objectives import m_elbo_naive_warmup
from .vaes.utils import Timer, EarlyStopping_nosave as EarlyStopping


@dataclass
class ModelParams:
    # VAE params
    r_dim: int  # dimensionality of RNA data
    p_dim: int  # dimensionality of ATAC data

    latent_dim: int = 10  # latent dimensionality
    num_hidden_layers: int = 1  # number of hidden layers in enc and dec

    r_hidden_dim: int = 100  # number of hidden units in enc/dec for RNA VAE
    p_hidden_dim: int = 20  # number of hidden units in enc/dec for ATAC VAE

    learn_prior: bool = True  # whether to learn model prior parameters
    llik_scaling: float = 1  # setting this to 0 crashes because of missing properties

    # optim params
    learning_rate: float = 1e-4


class scMM:
    def __init__(
        self, batch_size=100, epochs=10, deterministic_warmup=50, device="cpu"
    ):
        # setup model parameters
        self.batch_size = batch_size
        self.epochs = epochs
        self.device = device
        self.deterministic_warmup = deterministic_warmup
        self.print_freq = 1

    def fit(self, anndata_rna, anndata_atac):
        # setup model parameters
        self.params = ModelParams(
            r_dim=anndata_rna.var.shape[0], p_dim=anndata_atac.var.shape[0]
        )

        # instantiate model
        self.model = VAE_rna_atac(self.params).to(self.device)
        self.objective = m_elbo_naive_warmup
        self.optimizer = optim.Adam(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=self.params.learning_rate,
            amsgrad=True,
        )

        # prepare data
        data_loader = self.model.getDataLoaders(
            [
                anndata_rna.layers["counts"].toarray().astype(np.float32),
                anndata_atac.layers["counts"].toarray().astype(np.float32),
            ],
            batch_size=self.batch_size,
            shuffle=True,
            drop_last=True,
            device=self.device,
        )

        # get crackin'
        with Timer("MM-VAE") as t:
            agg = defaultdict(list)
            # initialize the early_stopping object
            early_stopping = EarlyStopping(patience=10, verbose=True)
            W = self.deterministic_warmup
            start_early_stop = W
            for epoch in range(1, self.epochs + 1):
                b_loss = self.train(data_loader, epoch, agg, W)
                if torch.isnan(torch.tensor([b_loss])):
                    break

                # TODO: actually handle test data
                # test(epoch, agg, W)

                if epoch > start_early_stop:
                    early_stopping(
                        agg["test_loss"][-1],
                        self.model,
                        "thisisjustsomedummypathisetbecauseiwastoolazytochangetheimplementation",
                    )
                if early_stopping.early_stop:
                    print("Early stopping")
                    break

    def train(self, train_loader, epoch, agg, W):
        self.model.train()
        b_loss = 0
        for i, dataT in enumerate(train_loader):
            beta = (epoch - 1) / W if epoch <= W else 1
            if dataT[0].size()[0] == 1:
                continue
            data = [d.to(self.device) for d in dataT]  # multimodal
            self.optimizer.zero_grad()
            loss = -self.objective(self.model, data, beta)
            loss.backward()
            self.optimizer.step()
            b_loss += loss.item()
            if self.print_freq > 0 and i % self.print_freq == 0:
                print(
                    "iteration {:04d}: loss: {:6.3f}".format(
                        i, loss.item() / self.batch_size
                    )
                )
        agg["train_loss"].append(b_loss / len(train_loader.dataset))
        print(
            "====> Epoch: {:03d} Train loss: {:.4f}".format(
                epoch, agg["train_loss"][-1]
            )
        )
        return b_loss

    def predict_mod(self, mod1=None, mod2=None):
        # TODO: magic
        pass
