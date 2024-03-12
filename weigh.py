import pandas as pd
import numpy as np
import math
from exceptions import *
from handlers import *

'''  
Ожидаемый формат params-csv-файла
NAME  INDEX  VALUE LINKED
0   m1    1      1            NaN
1   n1    1     10            NaN
2   m2    2      2            a1;a2
3   n2    2    100            NaN
4   m3    NaN      3          NaN
5    M    NaN   1000          a3;1/cy

Ожидаемый формат geomerty-csv-файла
NAME      VALUE
wing_area 1
ba        1
wingspan  1
AR        1

Подсчёт массы ЛА осуществляется по правилам:
 1) в ходе парсинга двух файлов (params_file, geometry_file) 
    формируется набор слагаемых, которые в сумме образуют массу ЛА
 2) все параметры из params_file, имеющие одинаковые индексы, будут перемножены, образуя слагаемое
 3) если у параметра из params_file в поле LINKED указана связанная величина 
    (или набор связанных величин) из geometry_file, 
    то этот параметр будет перемножен с ней, образуя слагаемое
    (в случае набора, слагаемым станет произведение всех величин из этого набора, умноженное на сам параметр) 
 4) если у величин указан и индекс, и связанная величина, то слагаемым станет 
    произведение всех параметров с одинаковыми индексами и всех у них указанных связанных величин
 5) в случае, если у параметра нет индекса, им становится имя параметра
 6) параметр, у которого не указан индекс и не указана связанная величина, не будет учтён при подсчёте массы
'''

def weigh(params_file_name, geometry_file_name, indicate_missing_param_vals=True, show_keys_in_logs=False):
    geom_df = pd.read_csv(geometry_file_name, header=None).loc[1:] #удаление заголовка из DF
    geom = dict(zip(geom_df[0], geom_df[1])) #создание словаря {Cy: <val>, ...}

    #создание таблицы с колонками вида 
    #[<colomn_num>, <NAME>, <INDEX>, <VALUE>, <LINKED>]
    params = pd.read_csv(params_file_name, index_col=False) 
    params = pd.DataFrame(filter(lambda x: x["NAME"][0] != "#", [params.iloc[i] for i in range(len(params.axes[0]))])).T
    
    #создание словаря 
    #{<index>: <список значений всех параметров и связанных величин, которые в произведении образуют слагаемое>}
    multiply_dict = dict()
    multiply_dict_names = dict()
    TOM = 0
    for var in params: #итерация по колонкам; в var попадает номер колонки (colomn_num)
        params[var]["VALUE"] = float(params[var]["VALUE"])
        if isnan(params[var]["VALUE"]):
            ans = "y"
            if indicate_missing_param_vals:
                ans = get_correct_answer(f"\nУ ПАРАМЕТРА {params[var]['NAME']} нет значения - пропустить и продолжить (y/n)?", ["y", "n"])
            if ans == "y":
                continue
            else:
                raise InsufficientInputData(f"no value for variable '{params[var]['NAME']}'")

        if isnan(params[var]["INDEX"]) and isnan(params[var]["LINKED"]):
            continue
        if not isnan(params[var]["INDEX"]):
            index = params[var]["INDEX"]
        
        else:
            index = params[var]['NAME']

        multiply_dict[index] = multiply_dict.get(index, [])
        multiply_dict_names[index] = multiply_dict_names.get(index, [])

        #сборка слагаемого:
        #добавление параметра к тем, у которых такой же индекс
        multiply_dict[index].append(params[var]["VALUE"])
        multiply_dict_names[index].append(params[var]["NAME"])

        #добавление связанных величин = 
        if not isnan(params[var]["LINKED"]):
            linked_list = "".join(params[var]["LINKED"].split()).split(";")
            try:
                linked = list(map(lambda conj: 1/float(geom[conj[2:]]) if conj[0:2] == "1/" else float(geom[conj]), linked_list))
            except KeyError as e:
                print(e)
                raise InsufficientInputData(f"for variable '{params[var]['NAME']}', '{params[var]['LINKED']}' "+\
                                                f"is specified as linked, but it is no '{params[var]['LINKED']}'"+\
                                                f" in the geom-file")
            for conj, conj_name in zip(linked, linked_list):
                multiply_dict[index].append(conj)
                multiply_dict_names[index].append(conj_name)

    #вычисление и суммирование слагаемых
    print(multiply_dict.items())
    for item in multiply_dict.items():
        key, vals = item #в vals содержатся все компоненты, в произведении образующие слагаемое
        TOM += math.prod(vals)
        if show_keys_in_logs:
            print(f"[key={key}]\n + ", " * ".join(multiply_dict_names[key]) , f": {TOM}", sep="")
        else:
            print(" + ", " * ".join(multiply_dict_names[key]) , f": {TOM}", sep="")
    
    print(f"------------------------\nИтоговая масса: {TOM}\n------------------------\n\n")
    return TOM