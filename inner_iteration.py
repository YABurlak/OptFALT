import pandas as pd
from new_sculptor import *
from handlers import import_py_module

# Все единицы в СИ
def inner_iteration():
    performance_file_name = "input_files/performance.py"#input("имя файла performances: ")
    params_file_name = "input_files/params.py" #input("имя файла params: ")
    settings_file_name = "input_files/settings.py" #input("имя файла settings: ") 
    tom = 1 #input("нулевое приближение влётной массы: ")
    max_iter = 5 #input("максимальное число итераций: ")
    
    tom_eps = import_py_module(settings_file_name).tom_eps
    
    sculptor = Sculptor(performance_file_name, params_file_name, settings_file_name, tom)
    sculptor.enable_log() 
    
    i = 1
    ask_about_no_value = True
    while True:
        sculptor.calculate_geometry()
        sculptor.write_info()

        sculptor.log(f"итерация {i}")
        new_tom = sculptor.weigh()
        ask_about_no_value = False
        if abs(tom - new_tom) > tom_eps:
            tom = new_tom
            sculptor.update_m(new_tom)
        else:
            sculptor.log(f"сошлось на итерации: {i}")
            sculptor.log("информация сохранена в файл с геометрией")
            return new_tom
        
        if i == max_iter:
            sculptor.log(f"прошло {i} итераций, но расчёт всё ещё не завершён.")
            flag = 2
            while flag not in ['0', '1']:
                flag = input(f"введите 1, чтобы произвести ещё {max_iter} операций, иначе 0: ")
            if flag == '1':
                i = 0
            else:
                sculptor.log("последняя итерация геометрии сохранена")
                break
        i+=1
    