import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from aerolib import *
from sys import platform

class XFoilException(Exception):
    def __init__(self, text):
        self.txt = text

def get_del_comand():
    del_comand = 'rm'
    if platform[0:3] == "win":
        del_comand = 'del'
    return del_comand

def XFoil_command_CL(V, AR, Sw, m, nu, M, ncr, xfoil_max_it, XFoil_path, work_path, foil_name):
    command_file=open(work_path + 'commands.in','w')
    command_file.write('load ' + work_path + foil_name + '.dat'+'\n'\
    + foil_name + '\n\
    panel\n\
    oper\n\
    visc ' + str(Re(V, ba(AR, Sw), nu)) + '\n\
    M ' + str(M) + '\n\
    type 1\n\
    vpar\n\
    n ' + str(ncr) + '\n\
    \n\
    iter\n' + str(xfoil_max_it) + '\n\
    pacc\n'\
    + work_path + 'polar.dat\n\
    \n\
    cl ' + str(CL_required(V, Sw, m)) +'\n\
    \n\
    \n\
    quit\n')
    #print(str(Re(V, ba(AR, Sw), nu)))
    command_file.close()
    return 0

def XFoil_run(file_path, xfoil_path):
    sep=os.path.sep
    if os.path.exists(file_path ):
        os.system(get_del_comand() + ' ' + file_path + 'polar.dat')
    run_xfoil_command = xfoil_path + 'xfoil < ' + file_path + \
    'commands.in'
    os.system(run_xfoil_command)
    return 0

def XFoil_read(file_path):
    aero_data_file = open(file_path + 'polar.dat', 'r')
    last_line = aero_data_file.readlines()[-1].split()
    if last_line[0][:2] == '--':
        raise XFoilException(f'на одном из удлинений XFoil выдал отбивку')
    aero_data_file.close()

    
    os.system(get_del_comand() + ' ' + file_path + 'polar.dat')
    alpha, cl, cd = float(last_line[0]), float(last_line[1]), float(last_line[2])
    return [alpha, cl, cd]

def K_V_solver(geom, settings, v, ar, tom):
    polar = np.array([])
    XFoil_command_CL(V=v, AR=ar, xfoil_max_it=int(settings.xfoil_max_it), M=float(settings.M), m=tom, nu = float(settings.dyn_viscosity), ncr=int(settings.ncr), Sw=float(geom.wing_area), work_path=str(settings.work_dir), XFoil_path=str(settings.XFoil_path), foil_name=str(settings.foil1_name))
    XFoil_run(file_path=settings.work_dir, xfoil_path=settings.XFoil_path)
    polar = np.append(polar, XFoil_read(file_path = settings.work_dir))
    polar = polar.reshape(polar.size // 3, 3)
    POLAR = pd.DataFrame(polar, columns = ['alpha', 'CL', 'CD'])
    POLAR.insert(0, "AR", ar)
    POLAR.insert(1, "V", v)
    POLAR.insert(4, "CDi", CDi(POLAR.CL, ar, osvald_coef = float(settings.osvald_coef)))
    POLAR.insert(5, "K", POLAR.CL / (POLAR.CD + POLAR.CDi))
    return POLAR
    #print(polar)
    #return [ar, v, polar[0][0], polar[0][1], polar[0][2], POLAR.CL / (POLAR.CD + POLAR.CDi), CDi(POLAR.CL, ar, osvald_coef = float(settings.osvald_coef))]

def AR_selector(ar_range, geom, settings, performance, tom):
    df = pd.DataFrame()
    for ar in ar_range:
        try:
            p = K_V_solver(geom, settings, float(performance.cruise_speed), ar, tom)
            #print(p)
            df = pd.concat([df, p], ignore_index=True, sort=False)
        except XFoilException as e:
            print(e)

    return df.iloc[df.K.argmax()].AR    
