import pandas as pd
from new_sculptor import *
from handlers import import_py_module
'''
Модуль расчёта геометрических характеристик потребляет на вход: 
dataframe PERFORMANCE с потребными эксплуатационными характеристиками
dataframe PARAMS с параметрами электронных компонент, конструкционных материалов, аккумуляторов и т.д.
пути до файлов селиговского формата с профилем крыла wing_foil и с профилем оперения aft_foil.
TOM - значение взлётной массы в начальном приближении.

PERFORMANCE включает параметры take_off_speed, cruise_speed, flight_time, payload

PARAMS включает параметры m_FPV, m_powerplant, m_flight_control, m_fus, m_servo1, m_servo2,
line_dens_wire, line_dens_tube1, line_dens_tube2, line_dens_tube3,
area_dens_LWPLA
energy_dens_bat
number_servo1, number_servo2
l_stab
'''

# Все единицы в СИ
def inner_iteration():
    performance_file_name = "performance.py"#input("имя файла performances: ")
    params_file_name = "params.py" #input("имя файла params: ")
    settings_file_name = "settings.py" #input("имя файла settings: ") 
    tom = 2 #input("нулевое приближение влётной массы: ")
    max_iter = 10 #input("максимальное число итераций: ")
    
    tom_eps = import_py_module(settings_file_name).tom_eps
    
    sculptor = Sculptor(performance_file_name, params_file_name, settings_file_name, tom)
    mass_dependencies = import_py_module("mass_dependencies.py")
    mass_logger = import_py_module("mass_logger.py")
    
    i = 1
    ask_about_no_value = True
    while True:
        sculptor.calculate_geometry()
        sculptor.write_info()

        mass_logger.print(f"итерация {i}")
        new_tom = mass_dependencies.weigh()
        mass_logger.log_mass()
        ask_about_no_value = False
        if abs(tom - new_tom) > tom_eps:
            tom = new_tom
            sculptor.update_m(new_tom)
        else:
            mass_logger.print(f"сошлось на итерации: {i}")
            mass_logger.print("информация сохранена в файл с геометрией")
            return new_tom
        
        if i == max_iter:
            mass_logger.print(f"прошло {i} итераций, но расчёт всё ещё не завершён.")
            flag = 2
            while flag not in ['0', '1']:
                flag = input(f"введите 1, чтобы произвести ещё {max_iter} операций, иначе 0: ")
            if flag:
                i = 0
            else:
                mass_logger.print("последняя итерация геометрии сохранена")
                break
            
        i+=1
    