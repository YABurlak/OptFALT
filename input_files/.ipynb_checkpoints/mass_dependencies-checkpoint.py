from importlib import reload
from input_files.params import *
from output_files.geometry import *


def weigh():
    M = 0
    
    #Компоненты FPV-системы
    M += mVTX * nVTX
    M += mCrossfire * nCrossfire
    M += mRunc_s4 * nRunc_s4

    #Силовая установка
    M += mReg * nReg
    # M += mAT2308 * nAT2308
    # M += mAT2312 * nAT2312
    M += mAT2814 * nAT2814
    # M += mLiIon18650 * nLiIon18650
    # M += mLiIon21700 * nLiIon21700
    M += mKIT * nKIT

    #Конструкционные материалы
    M += specific_wing * wing_area
    M += specific_glass * wing_area * 2
    M += (specific_aft + specific_glass * 2) * aft_area * 1.2
    M += specific_petg * spar_thickness * keel_area * 1.4
    M += mfus * nfus
    M += tube8X7 * ltube8X7
    M += tube8X6 * ltube8X6
    M += tube10X9 * ltube10X9
    M += spar1_hight * spar_thickness * wingspan * specific_lwpla
    M += spar2_hight * spar_thickness * wingspan * specific_lwpla
    M += spar3_hight * spar_thickness * wingspan * specific_lwpla 
    M += spar4_hight *  spar_thickness * wingspan * specific_lwpla

    #Cервы+провода
    M += mMG90 * nMG90
    M += mES9051 * nES9051
    M += specific_3wire * wire_length

    #Мозги+датчики
    M += mPixhawk * nPixhawk
    M += mPito * nPito

    #Полезная нагрузка
    M += mCargo * nCargo
    return M
