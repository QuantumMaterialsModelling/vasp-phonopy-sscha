import cellconstructor as CC
import sys
import os

def interpolate(parsed_args=None,NQIRR=None,q_points_old=None,q_points_new=None):
    if isinstance(parsed_args, list):
        NQIRR = int(parsed_args[0][0])
        if len(parsed_args[0]) == 2:
            q_points_old = int(parsed_args[0][1])
        if len(parsed_args[0]) == 3:
            q_points_old = int(parsed_args[0][1])
            q_points_new = int(parsed_args[0][2])
    print(parsed_args,NQIRR,q_points_old,q_points_new)
    DYN_PREFIX = "dyn/dynq"
    dyn = CC.Phonons.Phonons(DYN_PREFIX, NQIRR)
    dyn.Symmetrize()
    new_dyn = dyn.Interpolate((int(q_points_old),int(q_points_old),int(q_points_old)),(int(q_points_new),int(q_points_new),int(q_points_new)))
    os.system(f"mv dyn dyn_old"+str(q_points_old)+"x"+str(q_points_old)+"x"+str(q_points_old)+"")
    os.system("mkdir dyn")
    new_dyn.save_qe("dyn/dynq")

