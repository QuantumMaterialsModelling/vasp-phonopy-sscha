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
POPULATION=1
kong_liu_ratio=0.5
while [[ $runner = 'True' ]]
do
  if [[ $POPULATION -ne 1 ]]
  then
    kong_liu_1=`grep "Kong-Liu" minim1.out|head -1 | awk '{print $NF}'`
    kong_liu_2=`grep "Kong-Liu" minim$POPULATION.out|tail -1 | awk '{print $NF}'`
  else
    kong_liu_1=1
    kong_liu_2=0.4
  fi

  echo "============================="
  echo "Population="$POPULATION
  echo "Kong-Liu ratio="$kong_liu_ratio
  echo "============================="
  nkong_liu=`echo "$kong_liu_2 / $kong_liu_1" | bc -l`

#  if [[ $nkong_liu > $kong_liu_ratio ]]
  if [[ $POPULATION -le 5 ]]  #test
  then
    bash run_local.sh $POPULATION
    ((POPULATION++))
  else
    runner=False
  fi
done
