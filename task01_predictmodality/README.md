# Predict Modality - Starter Kit for Python Users

## Why there are two ways of running everything
There are two ways to run the script:
  1. use Viash (which implicitly builds a Docker image and stores different runs in different directories).
  2. run as an ordinary Python script.

Method 1. is important as it generates a submission, which is then marked by eval.ai (see the documentation below).
Method 2. is important as it allows us to iterate quickly and experiment with different methods.  

## Running the scripts
To run the script using method 1., make sure the dependencies are installed (see the official information from the organizers. It needs Docker and Viash)
and then run
```
./scripts/2_generate_submission.sh   # Type ./scripts/2<TAB> to use autocompletion.
```

To run the script using method 2., install the Python dependecies, as specified in `config.vsh.yaml`.
**Caution!** Currently it does not specify any CUDA support. Check the pytorch installation guide, if you intend to use CUDA. 

Then, you can simply run:
```
python script.py
```

## Adding new methods
The `script.py` file should be left as is (it does some magic to make sure we can run it using both methods).
If you intend to modify the method, see the `method` module.
Every new method should be implemented as a submodule and we can easily substitute by a tiny modification of `method/__init__.py`.


## Information from the organizers

Full documentation for the competition, including much of the information here, can be found online 
at [openproblems.bio/neurips_docs/](https://openproblems.bio/neurips_docs/). The documentation for 
Viash is available at [viash.io/docs](https://viash.io/docs).
​
### Getting Started
​
Check the [Quickstart](https://openproblems.bio/neurips_docs/submission/quickstart/) to create and upload your first submission to EvalAI.
​
Check the following links for more information:
​
- [Starter kit contents](https://openproblems.bio/neurips_docs/submission/starter_kit_contents/)
- [Development process](https://openproblems.bio/neurips_docs/submission/development_process/)
- [Submit to EvalAI](https://eval.ai/web/challenges/challenge-page/1111/submission)
​
### Folder Structure
​
```
├── LICENSE                                 # MIT License
├── README.md                               # Some starter information
├── bin/                                    # Binaries needed to generate a submission
│   ├── check_format
│   ├── nextflow
│   └── viash
├── config.vsh.yaml                         # Viash configuration file
├── script.py                               # Script containing your method
├── sample_data/                            # Small sample datasets for unit testing and debugging
│   ├── openproblems_bmmc_cite_starter/     # Contains H5AD files for CITE data
│   └── openproblems_bmmc_multiome_starter/ # Contains H5AD files for multiome data
├── scripts/                                # Scripts to test, generate, and evaluate a submission
│   ├── 0_sys_checks.sh                     # Checks that necessary software installed
│   ├── 1_unit_test.sh                      # Runs the unit tests in test.py
│   ├── 2_generate_submission.sh            # Generates a submission pkg by running your method on validation data
│   ├── 3_evaluate_submission.sh            # (Optional) Scores your method locally
│   └── nextflow.config                     # Configurations for running Nextflow locally
└── test.py                                 # Default unit tests. Feel free to add more tests, but don't remove any.
```

