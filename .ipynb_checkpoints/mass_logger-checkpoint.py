from params import *
from geometry import *
from mass_dependencies import weigh

def print(*data, end='\n', sep=' '):
    file = open("log.txt", "a")
    for line in data:
        file.write(str(line))
        file.write(sep)
    file.write(end)
    file.close()

def log_mass():
    file = open("mass_dependencies.py", "r")
    mass_list_started = False
    for line in file.readlines():
        if line[:12] == "def weigh():":
            mass_list_started = True
            continue
        if mass_list_started:
            if line.isspace():
                continue
            line = line[4:-1]
            if line[0] == "#":
                print()
                print(line[1:])
            elif line[0] == "M" and line.split() != ["M", "=", "0"]:
                expression = " ".join(line.split()[2:]) 
                print(expression + " = ", end="" )
                exec("print(" + expression + ")")

    print("="*20)
    print(f"M = {weigh()}\n")
    file.close()