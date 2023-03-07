#!/usr/bin/env bash
#
#  run_cicle.sh
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
runner=True
Start_POPULATION=1
POPULATION=$Start_POPULATION
while [[ $runner = 'True' ]]
do
  if [[ $POPULATION -eq $Start_POPULATION ]]
  then
      convergence="False"
  else
      last_pop=$(($POPULATION-1))
      convergence=`grep "SSCHA converge" minim$last_pop.out|tail -1 | awk '{print $NF}'`
  fi
  echo "============================="
  echo "Population="$POPULATION
  echo "Convergence="$convergence
  echo "============================="
  # convergence=`grep "SSCHA converge" minim$POPULATION.out|tail -1 | awk '{print $NF}'`
  case $convergence in
   (True)
       echo "OK, calculation converged"
       runner=False
       ;;
   (False)
       echo "NOT-converged"
       bash run_local.sh $POPULATION
       ((POPULATION++))
       ;;
  esac
  # if [[ $POPULATION -le 5 ]]
  # then
  #   bash run_local.sh $POPULATION
  #   ((POPULATION++))
  # else
  #   runner=False
  # fi
done
