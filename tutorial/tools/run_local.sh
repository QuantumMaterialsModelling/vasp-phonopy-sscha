#!/usr/bin/env bash
#
#  run_local.sh
#
#  Copyright 2023 Diego Martinez Gutierrez <diego.martinez@ehu.eus>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
POPULATION=$1
SUPERCELL_SIZE=2
TEMPERATURE=300
NCONFSSCHA=512
NQIRR=4
kong_liu_ratio=0.5
echo "============================="
echo "Population="$POPULATION
echo "Supercell size="$SUPERCELL_SIZE
echo "Number of configurations="$NCONFSSCHA
echo "Temperature="$TEMPERATURE
echo "============================="
echo "Change directory to "pop$POPULATION
cd pop$POPULATION
echo "========"+`pwd`+"======="
cp ../POSCAR_UNITCELL POSCAR
python /home/diego/github/vasp-phonopy-sscha/vasp-phonopy-sscha/interface.py --f_processing $POPULATION $SUPERCELL_SIZE
python /home/diego/github/vasp-phonopy-sscha/vasp-phonopy-sscha/interface.py --en_processing $POPULATION
cd ..
##echo "Editing SSCHA inputfile"
##nano minimize.py
echo "------Running SSCHA-----"
#python3 minimize.py > minim$POPULATION.out
python3 minimize.py -pop $POPULATION -nconf $NCONFSSCHA -cell $SUPERCELL_SIZE -temp $TEMPERATURE -nqirr $NQIRR > minim$POPULATION.out
echo "Change directory to "pop$(($POPULATION+1))
cd pop$(($POPULATION+1))
echo "========"+`pwd`+"======="
python /home/diego/github/vasp-phonopy-sscha/vasp-phonopy-sscha/interface.py --generate $NCONFSSCHA $(($POPULATION+1)) $SUPERCELL_SIZE $TEMPERATURE
cp ../POSCAR_UNITCELL POSCAR
python /home/diego/github/vasp-phonopy-sscha/vasp-phonopy-sscha/interface.py --to_vasp $(($POPULATION+1)) $SUPERCELL_SIZE
cp ../INCAR.sc vasp/INCAR
cp ../POTCAR.SrOTi vasp/POTCAR
cp ../ML_FF vasp/ML_FF
mkdir vasp/forces
# cp ../run.sh vasp/run.sh
# nano vasp/run.sh
#echo "---------------------------------------"
#echo "Now is time to do the VASP calculations"
#echo "---------------------------------------"
echo "============================="
echo "Change directory back"
cd ..
echo "========"+`pwd`+"======="
echo "----------------------------------------"
echo "Checking if the Kong-Liu parameter is OK"
echo "----------------------------------------"
#for i in `seq 1 $POPULATION`; do grep "Kong-liu" minim$i.out|tail -1;done
#grep "Kong-Liu" minim1.out|head -1;echo "--------";for i in `seq 1 12`;do grep "Kong-Liu" minim$i.out|tail -1;done
#echo "if those numbers are withing error (first one divided by last one less than KL ratio), continue with the VASP calculation"
kong_liu_1=`grep "Kong-Liu" minim1.out|head -1`
kong_liu_2=`grep "Kong-Liu" minim$POPULATION.out|tail -1`
echo "If this formula is OK, then you are converged:"
echo $(($kong_liu_1/$kong_liu_2))">"$kong_liu_ratio"?"
if [$(($kong_liu_1/$kong_liu_2)) -le $kong_liu_ratio]
then
  echo "---------------------------------------"
  echo "Now is time to do the VASP calculations"
  echo "---------------------------------------"
  echo "Change directory to "pop$(($POPULATION+1))
  cd pop$(($POPULATION+1))
  echo "========"+`pwd`+"======="
  #########################################################################
  #np=40           #number of cpus
  #POPULATION=1    #population index
  IONS=54         #number of atoms in the supercells
  #NCONFSSHA=300   #number of configurations in the sscha ensemble
  #mpirun vasp_std > stdout
  for i in `seq 1 $NCONFSSCHA`; do
      echo "---RUN--"$i"--of--"$NCONFSSCHA
      echo `date` >> timing
      cp POSCAR_$i POSCAR
  #    mpirun -np $np vasp_std > stdout
      ~/VASP/vasp.6.3.0/bin/vasp_std > stdout
      grep "energy  without entropy" OUTCAR  >> energies
      grep "forces" -A $IONS vasprun.xml > forces/forces_population$POPULATION'_'$i.dat
      rm POSCAR
      mv OUTCAR OUTCAR_$i
      echo `date` >> timing
  done
  #########################################################################
else
  echo "--------------------------"
  echo "The calculation converged."
  echo "--------------------------"
fi
