##########################################################################
############################ vaspsscha 1.0 ##############################
#########################################################################

VASP = Vienna Ab Initio Simulation Package
SSCHA = Stochastic Self Consistent Harmonic Approximation

This is the first version of the python package for the treatment of VASP and SSCHA input/output.


### 1 HOW TO INSTALL ###

Two ways:

1) pip install vaspsscha

This will safely store your package in the python environment in which you are running the command. In general, i really advice adopting the conda environment manager. If this is the case, it would be really useful to set an alias for the main script  "vaspsscha/vaspsscha/interface.py", creating a line in ~/.bashrc, ~/.myaliases (or any sourced file):

alias vaspsscha="python /YOUR-ANACONDA-INSTALLATION-PATH/anaconda3/envs/YOUR-ENVIRONMENT/lib/python3.10/site-packages/vaspsscha/interface.py"

2) python setup.py install

This will store the package folder as a subdirectory of your python in use. If you use the built-in python (highgly not recommended), it will end up in /usr/local/lib/python2.X.

FINAL REMARK: Wherever the package is installed, assign an alias to it in order to be able to call all the vaspsscha modules without referring to the installation path.

                                             
### 2 HOW TO USE ###
A step-by-step tutorial can be found in the "tutorial" folder. The C2 diamond is taken as a test case.
