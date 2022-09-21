from __future__ import print_function
from __future__ import division

# Import the modules to read the dynamical matrix
import cellconstructor as CC

# Import the SCHA modules
import sscha, sscha.Ensemble

import os

def generate(parsed_args=None,n_random=None, n_population=None, NQIRR=None, T=None):
    ##################################### ARGUMENTS INITIALIZATION
    DATA_DIR = "data"
    DYN_PREFIX = "dyn/dynq"
    print(parsed_args)
    if isinstance(parsed_args, list):
        n_random = int(parsed_args[0][0])
        if len(parsed_args[0]) == 2:
            n_random = int(parsed_args[0][0])
            n_population = int(parsed_args[0][1])
        if len(parsed_args[0]) == 3:
            n_random = int(parsed_args[0][0])
            n_population = int(parsed_args[0][1])
            NQIRR = int(parsed_args[0][2])
        if len(parsed_args[0]) == 4:
            n_random = int(parsed_args[0][0])
            n_population = int(parsed_args[0][1])
            NQIRR = int(parsed_args[0][2])
            T = float(parsed_args[0][3])

    if isinstance(n_random, int):
        pass
    else:
        n_random = int(input("\nHow many random ensembles you want to generate? (input the raw number)\n"))

    if isinstance(n_population, int):
        pass
    else:
        n_population = int(input("\nWhich population is this? (input the raw number)\n"))

    if isinstance(NQIRR, int):
        pass
    else:
        NQIRR = int(input("\nHow many irreducible dyn/dynq do you have in the dyn folder, after the eventual interpolation?? (input the raw number)\n"))

    if isinstance(T, int) or isinstance(T, float):
        pass
    else:
        T = int(input("\nAt which temperature you want to generate the ensembles? (input the raw number)\n"))

    ##################################### CORE
    # Print the info in the screen
    print()
    print(" ========== RUNNING =========== ")
    print()

    print("Loading the dynamical matrix...")
    dyn = CC.Phonons.Phonons(DYN_PREFIX, NQIRR)

    ###############################POSITIVIZATION?
    bool = input("You want to positivize your dynamical matrix? y/n\n")
    if bool == 'y':
        dyn.ForcePositiveDefinite()
    elif bool == 'n':
        pass
    else:
        print("\nThis is not a valid answer, try again\n")
    ################################
    dyn.Symmetrize()
    # dyn.save_qe("dyn_positive")
    print("The loaded dynamical matrix has a supercell of", dyn.GetSupercell())

    print("")
    print("Generating the ensemble of {} configurations".format(n_random))

    dyn.save_qe("dyn/dynq")
    ens = sscha.Ensemble.Ensemble(dyn, T, dyn.GetSupercell())  # (((dyn->new_dyn)
    # Evenodd keyword is used to reduce the stochastic noise, by generating symmetric configurations
    # Around the centroid positions. It requires an even ensemble or the code will complain.
    ens.generate(n_random, evenodd=True)

    print("")
    print("Saving the ensemble into {}, with id = {}...".format(DATA_DIR, n_population))
    ens.save(DATA_DIR, n_population)

    print("Done.")
    os.system("rm dyn*")
    return n_random, n_population, NQIRR




