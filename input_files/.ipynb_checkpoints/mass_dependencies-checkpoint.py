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
    M += mAT2308 * nAT2308
    M += mAT2312 * nAT2312
    M += mLiIon18650 * nLiIon18650
    M += mLiIon21700 * nLiIon21700

    #Конструкционные материалы
    M += specific_wing * wing_area
    M += specific_aft * Vtail_area
    M += mfus * nfus
    M += tube8X7 * ltube8X7
    M += tube8X6 * ltube8X6

    #Cервы+провода
    M += mMG90 * nMG90
    M += mES9051 * nES9051
    M += specific_3wire * wire_length

    #Мозги+датчики
    M += mPixhawk * nPixhawk
    M += mPito * nPito

    #Полезная нагрузка
    M += mGoPRO11 * nGoPRO11
    return M
