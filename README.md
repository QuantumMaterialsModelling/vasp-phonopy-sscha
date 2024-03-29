############################ vaspsscha 1.0


This is the first version of the python package for the treatment of VASP and SSCHA input/output, withi the aid of PHONOPY. A tutorial on C2 diamond will serve as a procedural guide, where a Machine Learning Force Field approach is adopted, as in:

https://arxiv.org/abs/2211.09616
https://arxiv.org/abs/2211.09616

Informatic resources:

SSCHA:
http://sscha.eu/

PHONOPY:
https://phonopy.github.io/phonopy/

VASP:
https://www.vasp.at/wiki/index.php/The_VASP_Manual


### 1 HOW TO INSTALL ###
The scripts are ready to use as they are. Wherever the package is installed, assign an alias to it in order to be able to call all the vaspsscha modules without referring to the installation path. To install the dependencies:

python setup.py install

Installing numpy may give problems, so it may be needed to install it by hand.

                                             
### 2 HOW TO USE ###
A step-by-step tutorial can be found in the "tutorial" folder (see README). The C2 diamond is taken as a test case.
