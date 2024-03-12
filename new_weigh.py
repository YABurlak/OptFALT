import pandas as pd
import numpy as np
import math
from exceptions import *
from handlers import *
from importlib import reload, import_module


def weigh(params_file_name, geometry_file_name, indicate_missing_param_vals=True, show_keys_in_logs=False):
    if params_file_name.split('.')[1] != "py" or len(params_file_name.split('.'))!=2:
        print("FO")
        return
    params = import_module(params_file_name.split('.')[0])
    return 