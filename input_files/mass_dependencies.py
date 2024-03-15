from importlib import reload
from input_files.params import *
from output_files.geometry import *


def weigh():
    M = 0
    #Аэродинамические параметры

    #Геометрические ограничения
    M += l_stab * tube6X5

    #Компоненты FPV-системы
    M += mVTX * nVTX
    M += mCrossfire * nCrossfire
    M += mRunc_s4 * nRunc_s4

    #Силовая установка
    M += mReg * nReg
    M += mAT2308 * nAT2308
    M += mLiIon18650 * nLiIon18650
    M += mLiIon21700 * nLiIon21700

    #Конструкционные материалы
    M += specific_wing * wing_area * AR
    M += specific_aft * Vtail_area
    M += mfus * nfus

    #Cервы+провода
    M += mMG90 * nMG90
    M += mES9051 * nES9051
    M += specific_3wire * wire_length

    #Мозги+датчики
    M += mPixhawk * nPixhawk
    M += mPito * nPito
    return M
