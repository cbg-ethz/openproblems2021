from .vaes import VAE_rna, VAE_atac, VAE_rna_atac


class scMM:
    def __init__(self, mod1, mod2):
        self.mod1 = mod1
        self.mod2 = mod2

    def fit(self, data):
        # TODO: magic
        pass

    def predict_mod(self, mod1=None, mod2=None):
        # TODO: magic
        pass
