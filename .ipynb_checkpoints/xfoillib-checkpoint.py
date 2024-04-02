import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from aerolib import *
from sys import platform

class XFoilException(Exception):
    def __init__(self, text):
        self.txt = text


def XFoil_command_CL(RE: float, CL: float, M: float, ncr: int, xfoil_max_it: int, XFoil_path: str, work_path: str, foil_name: str):
    '''Forms the text command file for XFoil.
    
    :param V: True Air Speed. Needed for Reynolds number calculation
    :param AR: Aspect ratio. Needed for mean aerodynamic chord calculation in Re
    :param :
    
    :return: 0
    :rtype: int
    '''
    command_file=open(work_path + 'commands.in','w')
    command_file.write('load ' + work_path + foil_name + '.dat'+'\n'\
    + foil_name + '\n\
    plop\n\
    g f\n\
    \n\
    oper\n\
    visc ' + str(RE) + '\n\
    M ' + str(M) + '\n\
    type 1\n\
    vpar\n\
    n ' + str(ncr) + '\n\
    \n\
    iter\n' + str(xfoil_max_it) + '\n\
    pacc\n'\
    + work_path + 'polar.dat\n\
    \n\
    cl ' + str(CL) +'\n\
    \n\
    \n\
    quit\n')
    #print(str(Re(V, ba(AR, Sw), nu)))
    command_file.close()
    return 0

def XFoil_run(file_path: str, xfoil_path: str):
    '''Runs commands.in file in xfoil.
    This function takes commands.in file from the file_path folder and runs this script 
    in xfoil. Returns standart polar.dat file, which contains data from calculation.
    It polar.dat already exists, it would be replaced by a new one.

    :param file_path: Path of commands.in file and also new polar.dat file.
    :type file_path: str

    :param xfoil_path: XFoil.exe path
    :return: 0
    '''
    sep=os.path.sep
    if os.path.exists(file_path):
        os.system('del ' + file_path + 'polar.dat')
    run_xfoil_command = xfoil_path + 'xfoil < ' + file_path + \
    'commands.in'
    os.system(run_xfoil_command)
    return 0

def XFoil_read(file_path: str):
    '''Reads data from the last line of polar.dat file.

    :param file_path: Path of polar.dat file.
    :return: Tuple contains [alpha, cl, cd] 
    :rtype: tuple[float, float, float]
    '''
    aero_data_file = open(file_path + 'polar.dat', 'r')
    last_line = aero_data_file.readlines()[-1].split()
    if last_line[0][:2] == '--':
        raise XFoilException(f'на одном из удлинений XFoil выдал отбивку')
    aero_data_file.close()

    
    os.system('del' + ' ' + file_path + 'polar.dat')
    alpha, cl, cd = float(last_line[0]), float(last_line[1]), float(last_line[2])
    return [alpha, cl, cd]


def K_V_solver(Sw: float, foil_name: str, v: float, ar: float, tom: float, 
               xfoil_max_it: int, M: float, nu: float, ncr: int, Osvald_c: float, work_path: str, XFoil_path: str):
    '''For given parameters of airplane and flow calculates aerodynamic coefficients via XFoil

    :param Sw: wing area
    :param foil_name: Name of the file (without extension) of the main wing foil.
    :param v: Airspeed
    :param ar: Aspect ratio of the wing
    :param tom: Take-off mass
    :param xfoil_max_it: Maximum number of iterations in XFoil. Preferably between 100 and 1000.
    :param M: Mach number for XFoil calculations. For velocities less than 50 m/s can be chosen 0.
    :param nu: Dynamic viscosity.
    :param ncr: n_crit parameter in XFoil. Responsible for laminar-turbulent transition modelling. [5, 12].
    You have to calibrate this parameter for particular foil and Re. By default can be chosen 9.
    :param Osvald_c: Oswald efficiency number in induced drag coefficient formula by the lifting line theory.
    Depends from wing plan form.
    :param work_path: Working directory with foil.dat file. Also polar.dat file will be created here.
    :param XFoil_path: XFoil.exe is situated here.
    :return: [AR, V, alpha, CL, CD, CDi, K]
    :rtype: Dataframe
    
    '''
    polar = np.array([])
    XFoil_command_CL(Re(v, ba(ar, Sw), nu), CL_required(v, Sw, tom), 
                     M, ncr, xfoil_max_it, XFoil_path, work_path, foil_name)
    XFoil_run(work_path, XFoil_path)
    polar = np.append(polar, XFoil_read(work_path))

    polar = polar.reshape(polar.size // 3, 3)
    POLAR = pd.DataFrame(polar, columns = ['alpha', 'CL', 'CD'])
    POLAR.insert(0, "AR", ar)
    POLAR.insert(1, "V", v)

    POLAR.insert(5, "CDi", CDi(POLAR.CL, ar, osvald_coef = Osvald_c))
    POLAR.insert(6, "K", POLAR.CL / (POLAR.CD + POLAR.CDi))

    return POLAR
    #print(polar)
    #return [ar, v, polar[0][0], polar[0][1], polar[0][2], POLAR.CL / (POLAR.CD + POLAR.CDi), CDi(POLAR.CL, ar, osvald_coef = float(settings.osvald_coef))]

def AR_selector(Sw: float, foil_name: str, v: float, ar_range: np.array, tom: float, xfoil_max_it: int, 
                M: float, nu: float, ncr: int, Osvald_c: float, work_path: str, XFoil_path: str):
    '''Chooses the aspect ratio from given in ar_range array, which provides maximum aerodynamic efficiency
    for given airspeed.
    
    :param Sw: wing area
    :param foil_name: Name of the file (without extension) of the main wing foil.
    :param v: Airspeed.
    :param ar: Array with aspect ratios from witch the best would be chosen.
    :param tom: Take-off mass
    :param xfoil_max_it: Maximum number of iterations in XFoil. Preferably between 100 and 1000.
    :param M: Mach number for XFoil calculations. For velocities less than 50 m/s can be chosen 0.
    :param nu: Dynamic viscosity.
    :param ncr: n_crit parameter in XFoil. Responsible for laminar-turbulent transition modelling. [5, 12].
    You have to calibrate this parameter for particular foil and Re. By default can be chosen 9.
    :param Osvald_c: Oswald efficiency number in induced drag coefficient formula by the lifting line theory.
    Depends from wing plan form.
    :param work_path: Working directory with foil.dat file. Also polar.dat file will be created here.
    :param XFoil_path: XFoil.exe is situated here.
    :return: aspect ratio
    :rtype: float
    '''
    df = pd.DataFrame()
    for ar in ar_range:
        try:
            p =  K_V_solver(Sw, foil_name, v, ar, tom, xfoil_max_it, M, nu, ncr, Osvald_c, work_path, XFoil_path)
            #print(p)
            df = pd.concat([df, p], ignore_index=True, sort=False)
        except XFoilException as e:
            print(e)

    return df.iloc[df.K.argmax()].AR    

    
