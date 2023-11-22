from math import pi
import math

def Re(V, l, nu = 1.5 * 10 ** (-5)):
    return int(V * l / nu)

def CL_required (V, S, m, rho = 1.22):
    return (2 * m * 9.81 / (rho * V ** 2 * S))

def CDi (CL, AR, osvald_coef = 0.9):
    return (CL ** 2 / (pi * osvald_coef * AR))

def wing_area(TOM, g, Density, take_off_speed, CL_take_off):
    return 2 * TOM * g / (Density * take_off_speed ** 2 * CL_take_off)

def CL_cruise(TOM, cruise_speed, wing_area, g, Density):
    return 2 * TOM * g / (Density * cruise_speed ** 2 * wing_area)

def wingspan (AR, wing_area):
    return (AR * wing_area) ** 2

def ba(AR, wing_area):
    return (wing_area / AR) ** 0.5

def aft_area(A_aft, wing_area, ba, l_stab):
    return A_aft * wing_area * ba / l_stab

def keel_area(B_keel, wing_area, wing_span, l_stab):
    return B_keel * wing_area * wing_span / l_stab

def gamma(keel_area, aft_area):
    return math.atan((keel_area / aft_area) ** 0.5)

def stab_area(aft_area, gamma):
    return aft_area / (math.cos(gamma)) ** 2

def P_cruise(TOM, K_cruise, eta_prop, g):
    return TOM * g / (K_cruise * eta_prop)

def wire_length(wingspan, l_stab, wire_scale_coef):
    return wingspan / 2 + 2 * wire_scale_coef * l_stab
    
def calc_foil_perimeter(filename):
    f = open(filename, 'r')
    dots = f.read().split("\n")[1:]
    if dots[-1].split() == []:
        dots = dots[:-1]
    P = 0
    for i in range(0, len(dots)):
        i = i%len(dots)
        try:
            x_, y_ = list(map(lambda x: float(x), dots[i-1].split()))
            x, y = list(map(lambda x: float(x), dots[i].split()))
        except Exception:
            print(f"\tWARN! calc_perimeter: ошибка парсинга строк {i}, {i-1}")
            raise ValueError
        P += ((x-x_)**2 + (y-y_)**2)**0.5
    return P