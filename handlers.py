from importlib import import_module

def isnan(obj):
    """ Checking for nan
    
    the lack of a standard isnan function 
    that accepts an arbitrary type 
    (isnan(str) and isnan(float) are used here)
    """
    return obj != obj

def get_correct_answer(msg, ans_list):
    ans = 0
    while ans not in ans_list:
        ans = input(msg)
    return ans


def import_py_module(name):
    if name.split('.')[1] != "py" or len(name.split('.'))!=2:
        print(f"File {name} was not import! It's name is incorrect!")
        return
    return import_module(name.split('.')[0])