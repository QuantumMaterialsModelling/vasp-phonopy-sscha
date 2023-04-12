#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import re
from glob import glob
import numpy as np

def f_processing(parsed_args,atom_occurrencies,type_atoms):
    pop_id = parsed_args[0][0]
    n = parsed_args[0][1]
    all_files = glob("vasp/forces/*")
    all_files.sort(key=lambda f: int(re.sub('\D', '', f)))
    a = 0
    for file in all_files:
        a = a + 1
        print(file)
        forces = pd.read_csv(file, engine='python', sep="\s+", skiprows=1, header=None)
        forces.drop([0, 4], axis=1, inplace=True)
        #forces[3] = pd.to_numeric(forces[3], downcast="float")   #what do this do???
        forces = forces * 0.0388937935
        #forces = forces * 0.02058171960
        processed_forces_path = f"data/forces_population{pop_id}_" + str(a) + ".dat"
        f = open(processed_forces_path, "w+")
        #forces.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")
        N = int(n)*int(n)*int(n)
        # for i in range(0, N):
        #     for j in range(0,int(np.sum(atom_occurrencies))):
        #         force =  forces.iloc[i+j*N+1-1]
        #         force = force.to_frame()
        #         force = force.transpose()
        #         force.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")
        # # FIXME:
        for i in range(0, N):
            for j in range(len(type_atoms)):
                for jj in range(0,int(atom_occurrencies[j])):
                    print("[",atom_occurrencies[j]*i+j*N+jj,"]")
                    force =  forces.iloc[atom_occurrencies[j]*i+j*N+jj]
                    force = force.to_frame()
                    force = force.transpose()
                    force.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")

            # #quickfix for SrTiO3
            # print(i,N,"[",i+1,"*",i+N+1,"*",3*i+2*N+1,"*",3*i+2*N+2,"*",3*i+2*N+3,"]")
            #
            # force =  forces.iloc[i+1-1]
            # force = force.to_frame()
            # force = force.transpose()
            # force.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")
            #
            # force = forces.iloc[i+N+1-1]
            # force = force.to_frame()
            # force = force.transpose()
            # force.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")
            #
            # force = forces.iloc[3*i+2*N+1-1]
            # force = force.to_frame()
            # force = force.transpose()
            # force.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")
            #
            # force = forces.iloc[3*i+2*N+2-1]
            # force = force.to_frame()
            # force = force.transpose()
            # force.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")
            #
            # force = forces.iloc[3*i+2*N+3-1]
            # force = force.to_frame()
            # force = force.transpose()
            # force.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")
            # for j in range(0, len(atom_occurrencies)):
            #     for k in range(0,atom_occurrencies[j]):
            #         force = forces.iloc[N * int(np.sum(atom_occurrencies[0:j])-atom_occurrencies[j]) + atom_occurrencies[j]*i + k]
            #         force = force.to_frame()
            #         force = force.transpose()
            #         force.to_csv(f, index=False, header=False, float_format="%16.12f", sep='\t', mode="w+")
############### everything alright, maybe read the dynamical matrix file instead of the POSCAR!
