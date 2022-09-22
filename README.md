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


### 2 FOLDER STRUCTURE ###
                                              pop_n
                                                |
    dyn                                        data                                                    vasp
                                 -where the SSCHA ensemble are stored                            - VASP execution directory 
                                                                                                    containing the ensembles POSCARs
### 3 HOW TO USE ###

vaspsscha intervenes in different points in the VASP+SSCHA workflow. All the scripts 
reside in the same folder vaspsscha/vaspsscha. 

FIRST THINGS FIRST: you need to have executed a phonopy harmonic calculation (even of very low precision), wheter using DFPT in the unit cell or FINITE DIFFERENCES in the supercell. Furthermore, you should have extracted the force constants through PHONOPY. 

THE MAIN SCRIPT

interface.py

1) 
    i) Creation of the Gamma point dynamical matrix (dynq1) from the just calculated PHONOPY FC (trial harmonic guess for the SSCHA cycle)
    ii) Interpolation on any q-grid of choice. These matrixes are grouped by reciprocal space symmetry in as many "dynq" files as the number of irreducible q* points.
    iii) generation of the first population from the harmonic guess. In case the dynamical matrix is not positive definite (aka unstable/imaginary phonons), it can be positivized in order to be able to generate the ensembles. 

