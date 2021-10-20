"""The module containing different methods, implemented as different submodules.

To use any given method, simply import `main` from it. 
"""
# from .scmm import main  # The scMM model. Sophisticated, so may yield better results, but slow to train without a GPU.
from .baseline import main  # The baseline method from the organizers. Can be used to quickly test the pipeline. (Well, it's a smoke test).

METHOD_ID = "bewinator"
