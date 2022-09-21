from __future__ import print_function
from __future__ import division

# module for parsing when calling functions
import argparse
import sys
import os

# Import the modules to read the dynamical matrix
import cellconstructor as CC
import cellconstructor.Phonons

# Import the SCHA modules
import sscha, sscha.Ensemble
import math
import os
import numpy as np
import pandas as pd
import pandas as pd
import re


# import the auxiliary functions
from generate import generate
from interpolate import interpolate
from to_vasp import to_vasp
from en_processing import en_processing
from f_processing import f_processing

#from sqlalchemy import create_engine

angstrom_to_bohr = 1.88973
conversionright = 0.0205816249
conversion = 0.0205817167 # = eV2Ry/A2au**2 (dyn mat phonopy is in eV/(A**2*mass)
digits = 8
masstoau = 911.444242

#Dictionary with all the elements and atomic masses

elements_dict = {'H' : 1.008,'He' : 4.003, 'Li' : 6.941, 'Be' : 9.012,\
                 'B' : 10.811, 'C' : 12.011, 'N' : 14.007, 'O' : 15.999,\
                 'F' : 18.998, 'Ne' : 20.180, 'Na' : 22.990, 'Mg' : 24.305,\
                 'Al' : 26.982, 'Si' : 28.086, 'P' : 30.974, 'S' : 32.066,\
                 'Cl' : 35.453, 'Ar' : 39.948, 'K' : 39.098, 'Ca' : 40.078,\
                 'Sc' : 44.956, 'Ti' : 47.867, 'V' : 50.942, 'Cr' : 51.996,\
                 'Mn' : 54.938, 'Fe' : 55.845, 'Co' : 58.933, 'Ni' : 58.693,\
                 'Cu' : 63.546, 'Zn' : 65.38, 'Ga' : 69.723, 'Ge' : 72.631,\
                 'As' : 74.922, 'Se' : 78.971, 'Br' : 79.904, 'Kr' : 84.798,\
                 'Rb' : 84.468, 'Sr' : 87.62, 'Y' : 88.906, 'Zr' : 91.224,\
                 'Nb' : 92.906, 'Mo' : 95.95, 'Tc' : 98.907, 'Ru' : 101.07,\
                 'Rh' : 102.906, 'Pd' : 106.42, 'Ag' : 107.868, 'Cd' : 112.414,\
                 'In' : 114.818, 'Sn' : 118.711, 'Sb' : 121.760, 'Te' : 126.7,\
                 'I' : 126.904, 'Xe' : 131.294, 'Cs' : 132.905, 'Ba' : 137.328,\
                 'La' : 138.905, 'Ce' : 140.116, 'Pr' : 140.908, 'Nd' : 144.243,\
                 'Pm' : 144.913, 'Sm' : 150.36, 'Eu' : 151.964, 'Gd' : 157.25,\
                 'Tb' : 158.925, 'Dy': 162.500, 'Ho' : 164.930, 'Er' : 167.259,\
                 'Tm' : 168.934, 'Yb' : 173.055, 'Lu' : 174.967, 'Hf' : 178.49,\
                 'Ta' : 180.948, 'W' : 183.84, 'Re' : 186.207, 'Os' : 190.23,\
                 'Ir' : 192.217, 'Pt' : 195.085, 'Au' : 196.967, 'Hg' : 200.592,\
                 'Tl' : 204.383, 'Pb' : 207.2, 'Bi' : 208.980, 'Po' : 208.982,\
                 'At' : 209.987, 'Rn' : 222.081, 'Fr' : 223.020, 'Ra' : 226.025,\
                 'Ac' : 227.028, 'Th' : 232.038, 'Pa' : 231.036, 'U' : 238.029,\
                 'Np' : 237, 'Pu' : 244, 'Am' : 243, 'Cm' : 247, 'Bk' : 247,\
                 'Ct' : 251, 'Es' : 252, 'Fm' : 257, 'Md' : 258, 'No' : 259,\
                 'Lr' : 262, 'Rf' : 261, 'Db' : 262, 'Sg' : 266, 'Bh' : 264,\
                 'Hs' : 269, 'Mt' : 268, 'Ds' : 271, 'Rg' : 272, 'Ch' : 285,\
                 'Nh' : 284, 'Fl' : 289, 'Mc' : 288, 'Lv' : 292, 'Tr' : 294,\
                 'Og' : 294}

class DynamicalMatrixArray():
    def __init__(self, supercell_dimension=None):
        self.n_kpoints = 0                          #Number of kpoints in total
        self.supercell_dimension = np.array([supercell_dimension,supercell_dimension,supercell_dimension])      #list with the supercell dimension
        self.unit_cell_atoms = []                #list with the atom identifiers for the unit cell
        self.n_atoms = 0                                      #number of atoms in the unit cell
        self.type_atoms = []                          #############
        self.mass_atoms = []                                  #list with the mass of the atoms in the unit cell
        self.dynamical_matrix = []
        self.dynamical_matrix_complex = []
        self.supercell_multiplier = []                          #mulitplier of the lattice vectors
        self.atom_occurencies = []                              #list with the occurencies of each atom in order
        self.basis_vectors = []                                 #list that contains 3 string for each entry. Each string is the basis vector
        self.atomic_positions = []                              #list that contains 3 string for each entry. Each string is an atomic position
        self.header = None

    def get_masses(self):
        for atom in self.unit_cell_atoms:
            self.mass_atoms.append(elements_dict.get(atom))

    def get_mass(self, atom):
        return elements_dict.get(atom)*masstoau

    def phonopy_execution(self):
            print("\n Generation of Phonopy Dyn matrix:\n")
            os.system(
                "phonopy --dim='" + str(self.supercell_dimension[0]) + " " + str(self.supercell_dimension[1]) + " " + str(self.supercell_dimension[2]) + "' --writedm --readfc --qpoints='0 0 0'")
                #"phonopy --dim='" + self.supercell_dimension[0] + " " + self.supercell_dimension[1] + " " + self.supercell_dimension[2] + "' --writedm --qpoints='" + str(round(self.list_kpoints.at[i, 0], digits))+" "+str(round(self.list_kpoints.at[i, 1], digits))+" "+str(round(self.list_kpoints.at[i, 2], digits)) + "'")
            os.system("mv qpoints.yaml " + str(1) + ".txt")

    def poscar_reader(self):
        self.supercell_multiplier = pd.read_csv("POSCAR", engine='python', skiprows=1, nrows=1, header=None).values.tolist()[0]
        self.supercell_multiplier = float(self.supercell_multiplier[0])*angstrom_to_bohr
        self.basis_vectors.append(pd.read_csv("POSCAR", engine='python', sep="\s+", skiprows=2, nrows=1, header=None).values.tolist()[0])
        self.basis_vectors.append(pd.read_csv("POSCAR", engine='python', sep="\s+", skiprows=3, nrows=1, header=None).values.tolist()[0])
        self.basis_vectors.append(pd.read_csv("POSCAR", engine='python', sep="\s+", skiprows=4, nrows=1, header=None).values.tolist()[0])
        self.type_atoms = pd.read_csv("POSCAR", engine='python', sep="\s+", skiprows=5, nrows=1, header=None).values.tolist()[0]
        self.atom_occurencies = pd.read_csv("POSCAR", engine='python', sep="\s+", skiprows=6, nrows=1, header=None).values.tolist()[0]
        for index in range(len(self.atom_occurencies)):
            self.n_atoms += self.atom_occurencies[index]
        for index in range(len(self.type_atoms)):
            for indey in range(self.atom_occurencies[index]):
                    self.unit_cell_atoms.append(self.type_atoms[index])
        for index in range(self.n_atoms):
            self.atomic_positions.append(pd.read_csv("POSCAR", engine='python', sep="\s+", skiprows=8+index, nrows=1, header=None).values.tolist()[0])
        self.get_masses()
        self.header = header(self.supercell_multiplier, self.atomic_positions, self.basis_vectors)
        print(f" Supercell multiplier: {self.supercell_multiplier} \n basis_vectors: {self.basis_vectors} \n type_atoms: {self.type_atoms} \n atom_occurencies: {self.atom_occurencies} \n unit_cell_atoms: \n{self.unit_cell_atoms} \n atomic_positions: {self.atomic_positions} \n n_atoms: {self.n_atoms}")

    def matrix_reading(self):
            self.dynamical_matrix = (pd.read_csv(str(1) + ".txt", engine='python', sep="\s+", skiprows=9, nrows=3*self.n_atoms, header=None))

    def matrix_formatting(self):
            self.dynamical_matrix = self.dynamical_matrix.drop(0, 1)
            self.dynamical_matrix = self.dynamical_matrix.drop(1, 1)
            self.dynamical_matrix = self.dynamical_matrix.iloc[:, :-1]
            self.dynamical_matrix[:] = self.dynamical_matrix[:].replace({']': ''}, regex=True)
            self.dynamical_matrix[:] = self.dynamical_matrix[:].replace({',': ''}, regex=True)
            self.dynamical_matrix.columns = range(self.dynamical_matrix.shape[1])
            for col in self.dynamical_matrix:
                self.dynamical_matrix[col] = self.dynamical_matrix[col].astype(np.float32)
                self.dynamical_matrix[col] = self.dynamical_matrix[col].round(decimals=6)
            self.dynamical_matrix = self.dynamical_matrix / (15.633302 * 15.633302)
            #print(self.dynamical_matrix)
            self.dynamical_matrix = self.dynamical_matrix.to_numpy()

    def matrix_complexifier(self):
        #print(self.dynamical_matrix)
        self.dynamical_matrix_complex = np.array(self.dynamical_matrix[:, ::2] + 1j*self.dynamical_matrix[:, ::2], dtype=complex)

    def print_matrix_complex(self):
        #for i in range(0, self.n_kpoints):
        #print(self.dynamical_matrix_complex)
        print("")

    def write_dyn(self):
        # !!! read rec latt vectors
        aa=pd.read_csv("1.txt", engine='python', sep="   | |,", skiprows=3, nrows=3, header=None)
        # b1,b2,b3 in units of 2pi/a (read in 1/A, so multiply by alat in A)
        b1=aa.loc[0,2:6:2].to_numpy(float)*self.supercell_multiplier/angstrom_to_bohr
        b2=aa.loc[1,2:6:2].to_numpy(float)*self.supercell_multiplier/angstrom_to_bohr
        b3=aa.loc[2,2:6:2].to_numpy(float)*self.supercell_multiplier/angstrom_to_bohr
        print(f"\n The reciprocal lattice vectors in units of 2pi/a:")
        print(b1)
        print(b2)
        print(b3)

        file = open("dynq"+str(1), "a+")
        file.write("Dynamical matrix file\nFile generated with the CellConstructor by Lorenzo Monacelli")
        #file.write(f"\n{len(self.type_atoms)} {self.n_atoms} 0   {self.supercell_multiplier} 0    0.0000    0.000    0.0000    0.0000    0.0000")
        file.write(f"\n{len(self.type_atoms)} {self.n_atoms} 0   {self.supercell_multiplier} 0.0000    0.000    0.0000    0.0000    0.0000")
        file.write("\nBasis vectors")
        for index in range(len(self.basis_vectors)):
            file.write("\n")
            self.header.write_string(self.basis_vectors, index, file)
        for index in range(len(self.type_atoms)):
            file.write("\n")
            file.write(f"{index+1}   '{self.type_atoms[index]} '   {self.get_mass(self.type_atoms[index])}")
        for index in range(len(self.header.atomic_positions)):
            file.write(f"\n   {index+1}    {self.type_atoms.index(self.unit_cell_atoms[index])+1}    ")
            self.header.write_string(self.atomic_positions, index, file)
        file.close()
        file = open("dynq"+str(1), "a+")
        file.write("\n\n     Dynamical  Matrix in cartesian axes \n\n     q = (0.0  0.0  0.0)\n")
        # qui rimoltiplico la matrice dinamica per le masse amu che phonopy usa per creare la matrice dinamiche dividendo
        # per queste masse....spero siano i valori giusti!
        for i in range(0,self.n_atoms):
            for j in range(0,self.n_atoms):
                file.write("\n    " + str(i+1) + "   " + str(j+1) + "\n")
                sub_matrix = self.dynamical_matrix[i*3 : i*3+3 , j*6 : j*6+6] * math.sqrt(self.mass_atoms[i]*self.mass_atoms[j])
                sub_matrix = conversion*sub_matrix
                pd_sub_matrix = pd.DataFrame(sub_matrix)
                pd_sub_matrix.to_csv(file, sep='\t', index=False, header=False, float_format="%12.8f", mode="w+")
        file.close()

class header():
    def __init__ (self, supercell_multiplier=0, atomic_positions=[], basis_vectors=[]):
        self.basis_vectors = basis_vectors
        self.supercell_multiplier = supercell_multiplier
        self.atomic_positions = atomic_positions
        self.attribute = None

    def write_string(self, attribute, index, file):
        #splitted = attribute[index].split(" ",2)
        for element in attribute[index]:
            file.write(f"     {element}   ")

class Poscar():
    lattice_vectors = []
    header=header()
    def __init__ (self, n_population, arun, n_ensemble):
        self.n_ensemble = n_ensemble
        self.run = arun
        route = "data/position/scf_population"+str(n_population)+"_"+str(self.n_ensemble)+".dat"
        self.lattice_vectors = []
        self.lattice_vectors.append(pd.read_csv(route, engine='python', sep="\s+", skiprows=1, nrows=1, header=None).values.tolist()[0])
        self.lattice_vectors.append(pd.read_csv(route, engine='python', sep="\s+", skiprows=2, nrows=1, header=None).values.tolist()[0])
        self.lattice_vectors.append(pd.read_csv(route, engine='python', sep="\s+", skiprows=3, nrows=1, header=None).values.tolist()[0])

        a = pd.read_csv(route, engine='python', sep="\s+", skiprows=6, names=['specie', 'x','y','z'], header=None)
        #print(a)
        self.positions = a

    def poscar_to_vasp(self,qpoints):
        f = open(f"vasp/POSCAR_"+str(self.n_ensemble), "w+")
        f.write("generated by phonopy ")
        f.write(f"\n1.0") ################## TO BE MODIFIED!
        for index in range(len(self.lattice_vectors)):
            f.write("\n")
            self.header.write_string(self.lattice_vectors, index, f)
        f.write("\n")
        for index in self.run.type_atoms:
            f.write(f"{index} ")
        f.write("\n")
        for index in self.run.atom_occurencies:
            f.write(f"{index*int(qpoints[0])*int(qpoints[0])*int(qpoints[0])}   ")
        f.write("\n")
        f.write("Cartesian")

        for atom in self.run.type_atoms:
            for index in range(self.run.n_atoms*int(qpoints[0])*int(qpoints[0])*int(qpoints[0])):
                if self.positions.iloc[index,0] == atom:
                    f.write("\n")
                    f.write(f" {self.positions.iloc[index, 1]}  {self.positions.iloc[index, 2]}  {self.positions.iloc[index, 3]}")
        f.close()

####################################### FOR THE GENERATION FROM SCRATCH, THE CODE ST8ARTS HERE
first_execution=True

if __name__ == '__main__':
    # if you type --help
    parser = argparse.ArgumentParser(description='Run some functions')

    # Add a command
    parser.add_argument('--generate',  action='append', nargs='+', help='\nGenerate an ensemble starting from the dyn/dynq* matrixes. \nUsage: \ninterface.py --generate "number of ensembles" "population number" "number of dynq files(= number of irreducible q*)" "Temperature"  ')
    parser.add_argument('--interpolate',  action='append', nargs='+', help='\nInterpolate from the old qgrid to the new one. Usage: interface.py --interpolate "NQIRR" "q_grid_new" "q_grid_old"\n')
    parser.add_argument('--to_vasp', action='append', nargs='+', help='\nFill vasp directory with the populations in data. YOU NEED A POSCAR PRIMITIVE CELL FILE IN THE PRESENT DIRECTORY! \nUsage:\n interface.py --to_vasp "population_id" "supercell dimension" (if NxNxN, type N)' )
    parser.add_argument('--en_processing', action='append', nargs='+', help='\nConvert the VASP energies from the /vasp/energies file to the /data folder in QE format. \nUsage:\n interface.py --en_processing "population_id"')
    parser.add_argument('--f_processing', action='append', nargs='+', help='\nConvert the VASP forces from the /vasp/forces folder to the /data folder in QE format. YOU NEED A POSCAR PRIMITIVE CELL FILE IN THE PRESENT DIRECTORY! \nUsage:\n interface.py --f_processing "population_id" "supercell dimension" (if NxNxN, type N)')

    # Get our arguments from the user
    args = parser.parse_args()

    if args.generate:
        generate(args.generate)
        exit()

    if args.interpolate:
        interpolate(args.interpolate)
        exit()

    if args.to_vasp:
        run_shot = DynamicalMatrixArray()
        run_shot.poscar_reader()
        path=to_vasp()
        n_ensemble = 0
        ordered_files = sorted(os.listdir(path), key=lambda x: (int(re.sub('\D', '', x)), x))
        for file in ordered_files:
            print(file)
            n_ensemble += 1
            ensemble = Poscar(args.to_vasp[0][0], run_shot, n_ensemble)
            ensemble.poscar_to_vasp(np.array([args.to_vasp[0][1]]))
        exit()

    if args.en_processing:
        en_processing(args.en_processing)
        exit()

    if args.f_processing:
        run_temp = DynamicalMatrixArray()
        run_temp.poscar_reader()
        f_processing(args.f_processing,run_temp.atom_occurencies,run_temp.type_atoms)
        exit()

######################################## HERE THE FIRST INITIALIAZATION STARTS BY TAKING THE HARMONIC COMPUTED IN VASP+PHONOPY

os.system("rm -r pop")
run1 = DynamicalMatrixArray(input("\nI am gonna generate the dynamical matrix in Gamma from the phonopy FC matrix. Which is your phonopy supercell? \n(if NxNxN, type N)\n"))#, unit_cell_atoms = ['O', 'O', 'O', 'K', 'Ta'], type_atoms = ['O', 'K', 'Ta'])
os.system("mkdir dyn pop")

run1.poscar_reader()
run1.phonopy_execution()
run1.matrix_reading()
run1.matrix_formatting()
run1.matrix_complexifier()
run1.write_dyn()
os.system("mv dynq* dyn")
os.system("mv dyn pop")
os.chdir("pop")

bool = input("\nDo you want to interpolate the dynamical matrix? y/n\n")
if bool == 'y':
    Q = input("\nTo which QxQxQ grid you want to interpolate? Input Q\n")
    interpolate(None,1,1,Q)
else:
    Q = 1

n_random,n_population,NQIRR = generate(None)

print("making position\n")
os.system("mkdir data/position")
print("made position\n")
os.system("mv data/scf_population"+f"{n_population}_* data/position")
os.system("mkdir vasp")

path = "data/position/"
ordered_files = sorted(os.listdir(path), key=lambda x: (int(re.sub('\D', '', x)), x))
n_ensemble = 0
for file in ordered_files:
    print(file)
    n_ensemble += 1
    ensemble = Poscar(n_population, run1, n_ensemble)
    ensemble.poscar_to_vasp(np.array([Q, Q, Q]))
