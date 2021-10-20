# Dependencies:
# pip: scikit-learn, anndata, scanpy
#
# Python starter kit for the NeurIPS 2021 Single-Cell Competition.
# Parts with `TODO` are supposed to be changed by you.
#
# More documentation:
#
# https://viash.io/docs/creating_components/python/
import logging
import os
import sys

import anndata as ad


logging.basicConfig(level=logging.INFO)

## VIASH START
# Anything within this block will be removed by `viash` and will be
# replaced with the parameters as specified in your config.vsh.yaml.
par = {
    "input_train_mod1": "sample_data/openproblems_bmmc_multiome_starter/openproblems_bmmc_multiome_starter.train_mod1.h5ad",
    "input_train_mod2": "sample_data/openproblems_bmmc_multiome_starter/openproblems_bmmc_multiome_starter.train_mod2.h5ad",
    "input_test_mod1": "sample_data/openproblems_bmmc_multiome_starter/openproblems_bmmc_multiome_starter.test_mod1.h5ad",
    "distance_method": "minkowski",
    "output": "output.h5ad",
    "n_pcs": 50,
    "load_method_from_zip": False,
}
meta = {"resources_dir": "."}
## VIASH END

if par["load_method_from_zip"]:
    import zipimport

    path_to_module = os.path.join(meta["resources_dir"], "method.zip")
    importer = zipimport.zipimporter(path_to_module)
    method = importer.load_module("method")
else:
    import method


method_id = method.METHOD_ID

logging.info("Reading `h5ad` files...")
input_train_mod1 = ad.read_h5ad(par["input_train_mod1"])
input_train_mod2 = ad.read_h5ad(par["input_train_mod2"])
input_test_mod1 = ad.read_h5ad(par["input_test_mod1"])

input_train = ad.concat(
    {"train": input_train_mod1, "test": input_test_mod1},
    axis=0,
    join="outer",
    label="group",
    fill_value=0,
    index_unique="-",
)

y_pred = method.main(input_train_mod1, input_train_mod2, input_test_mod1, input_train)

adata = ad.AnnData(
    X=y_pred,
    obs=input_test_mod1.obs,
    var=input_train_mod2.var,
    uns={
        "dataset_id": input_train_mod1.uns["dataset_id"],
        "method_id": method_id,
    },
)

logging.info("Storing annotated data...")
adata.write_h5ad(par["output"], compression="gzip")
