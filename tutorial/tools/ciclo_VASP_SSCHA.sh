#!/usr/bin/env bash
POPULATION=$1
SUPERCELL_SIZE=2
TEMPERATURE=300
NCONFSSCHA=512
echo "============================="
echo "Population="$POPULATION
echo "Supercell size="$SUPERCELL_SIZE
echo "Number of configurations="$NCONFSSCHA
echo "Temperature="$TEMPERATURE
echo "============================="
echo "Change directory to "pop$POPULATION
$(($POPULATION+1))

cd pop$POPULATION
cp ../POSCAR_UNITCELL POSCAR
python ../../vasp-phonopy-sscha/vasp-phonopy-sscha/interface.py --f_processing $POPULATION $SUPERCELL_SIZE
python ../../vasp-phonopy-sscha/vasp-phonopy-sscha/interface.py --en_processing $POPULATION
cd ..
nano minimize.py
python3 minimize.py > minim$POPULATION.out
echo "Change directory to "pop$(($POPULATION+1))
cd pop$(($POPULATION+1))
python ../../vasp-phonopy-sscha/vasp-phonopy-sscha/interface.py --generate $NCONFSSCHA $(($POPULATION+1)) $SUPERCELL_SIZE $TEMPERATURE
cp ../POSCAR_UNITCELL POSCAR
python ../../vasp-phonopy-sscha/vasp-phonopy-sscha/interface.py --to_vasp $(($POPULATION+1)) $SUPERCELL_SIZE
cp ../INCAR.sc vasp/INCAR
cp ../POTCAR.SrOTi vasp/POTCAR
cp ../ML_FF vasp/ML_FF
cp ../run.bash vasp/run.bash
nano vasp/run.bash
echo "---------------------------------------"
echo "Now is time to do the VASP calculations"
echo "---------------------------------------"
cd ..
