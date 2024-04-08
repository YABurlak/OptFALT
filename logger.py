from importlib import reload

from input_files.params import *
from output_files.geometry import *
from input_files.mass_dependencies import weigh



def log_weigh(file_name):
    file = open("input_files/mass_dependencies.py", "r")
    mass_list_started = False
    log_file = open(file_name, "a")
    for line in file.readlines():
        if line[:12] == "def weigh():":
            mass_list_started = True
            continue
        if mass_list_started:
            if line.isspace():
                continue
            line = line[4:-1]
            if line[0] == "#":
                log_file.write("\n")
                log_file.write(line[1:]+"\n")
            elif line[0] == "M" and line.split() != ["M", "=", "0"]:
                expression = " ".join(line.split()[2:]) 
                log_file.write(expression + " = ")
                exec("log_file.write(str(" + expression + ")\n)")
                log_file.write("\n")
                
    log_file.write("\n")
    log_file.write("="*20)
    log_file.write("\n")
    log_file.write(f"M = {weigh()}\n")
    log_file.write("\n")
    log_file.write("\n")
    log_file.close()
    