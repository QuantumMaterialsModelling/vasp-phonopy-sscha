import sys,os

import ase
from ase.calculators.espresso import Espresso
from ase.visualize import view

# We import the basis modules for the SSCHA
import cellconstructor as CC
import cellconstructor.Structure
import cellconstructor.Phonons

# Import the SSCHA engine (we will use it later)
import sscha, sscha.Ensemble, sscha.SchaMinimizer, sscha.Relax

N=300
T=0
pop=1
dyn = CC.Phonons.Phonons("dyn/dynq",4) ###(position of the dyn matr, # of irred q-points)
ensemble = sscha.Ensemble.Ensemble(dyn, T, supercell = (3,3,3))
ensemble.load("data", pop, 300, verbose=True)

minimizer = sscha.SchaMinimizer.SSCHA_Minimizer(ensemble)

# Ignore the structure minimization (is fixed by symmetry)
minimizer.minim_struct = False

# Setup the minimization parameter for the covariance matrix
minimizer.min_step_struc = 0.05
minimizer.min_step_dyn = 0.05
minimizer.gradi_op = "all"
minimizer.precond_dyn = True
minimizer.root_representation = "normal"
minimizer.kong_liu_ratio = 0.5 # Usually 0.5 is a good value
minimizer.meaningful_factor = 0.00000001

# Lest start the minimization


minimizer.init()
IO = sscha.Utilities.IOInfo()
IO.SetupSaving('minim_1')
IO.SetupAtomicPositions('minim_1_positions', save_each_step=True)

####### define custom function: we select all branches, but limit gradient on Gamma 

minimizer.run(custom_function_post=IO.CFP_SaveAll)

minimizer.finalize()

# We can save the dynamical matrix
minimizer.dyn.save_qe("dyn/dynq_after")

# Print the frequencies before and after the minimization
w_old, p_old = ensemble.dyn_0.DiagonalizeSupercell() # This is the representation of the density matrix used to generate the ensemble
w_new, p_new = minimizer.dyn.DiagonalizeSupercell()

#We can now print them
print(" Old frequencies |  New frequencies")
print("\n".join(["{:16.4f} | {:16.4f}  cm-1".format(w_old[i] * CC.Units.RY_TO_CM, w_new[i] * CC.Units.RY_TO_CM) for i in range(len(w_old))]))
