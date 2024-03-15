import pandas as pd
import numpy as np
from handlers import isnan, import_py_module
from importlib import reload, import_module 
import logger 

from aerolib import *
from xfoillib import *
from exceptions import *
import input_files.mass_dependencies as md


class Sculptor():
    def __init__(self, performance_file_name, params_file_name, settings_file_name, m):
        self.params_file_name: str = params_file_name
        self.params = import_py_module(params_file_name)
        
        self.performance_file_name: str = performance_file_name
        self.performance = import_py_module(performance_file_name)

        self.settings_file_name: str = settings_file_name
        self.settings = import_py_module(settings_file_name)
        
        self.geometry_file_name = self.generate_geometry_file()
        self.geometry = import_py_module(self.geometry_file_name)

        self.aero_file_name = self.generate_aero_file()
        self.aero = import_py_module(self.aero_file_name)
        
        self.tom = m 
        self.log_flag = False
        self.log_file_name = "output_files/log.txt"
        open(self.log_file_name, "w").close()
        

    def log(self, *data, end='\n', sep=' '):
        file = open(self.log_file_name, "a")
        for line in data: 
            file.write(str(line))
            file.write(sep)
        file.write(end)
        file.close()

    def enable_log(self):
        self.log_flag = True

    def generate_geometry_file(self, unic_name=False):
        geometry_file_name = "output_files/geometry.py"
        if unic_name:
            pass
        self.geometry_variables = ["wing_area", "AR", "ba", "wingspan", "foil1_perimeter",
                              "foil1_area", "aft_area", "keel_area", "V_dihedral",
                              "Vtail_area", "P_cruise", "wire_length"]
        file = open(geometry_file_name, "w")
        for var in self.geometry_variables:
            file.write(var+" = 0\n")
        file.close()
        return geometry_file_name

    def generate_aero_file(self, unic_name=False):
        aero_file_name = "output_files/aero.py"
        if unic_name:
            pass
        self.aero_variables = ["AR", "V", "alpha", "CL", "CDi", "K", "CD"]
        file = open(aero_file_name, "w")
        for var in self.aero_variables:
            file.write(var+" = 0\n")
        file.close()
        return aero_file_name

    def calculate_geometry(self):
        self.geometry.wing_area = wing_area(self.tom, float(self.settings.g), float(self.settings.density), float(self.performance.take_off_speed), float(self.params.CL_take_off))
        
        CL_cr = CL_cruise(self.tom, self.performance.cruise_speed, float(self.geometry.wing_area), float(self.settings.g), float(self.settings.density))
        ar_step_number = int(abs(float(self.settings.ar_max) - float(self.settings.ar_min)) // float(self.settings.ar_delta))
        ar_range = np.linspace(float(self.settings.ar_min), float(self.settings.ar_max), ar_step_number)
        
        self.geometry.AR = AR_selector(ar_range, self.geometry, self.settings, self.performance, self.tom)
        self.aero.AR, self.aero.V, self.aero.alpha, self.aero.CL, self.aero.CDi, self.aero.K, self.aero.CD = K_V_solver(self.geometry, self.settings, self.performance.cruise_speed, self.geometry.AR, self.tom).values.tolist()[0]
        
        self.geometry.ba = ba(self.geometry.AR, self.geometry.wing_area)
        self.geometry.wingspan = wingspan(self.geometry.AR, self.geometry.wing_area)
        self.geometry.aft_area = aft_area(float(self.params.A_aft), self.geometry.wing_area, self.geometry.ba, float(self.params.l_stab))
        self.geometry.keel_area = keel_area(float(self.params.B_keel), self.geometry.wing_area, self.geometry.wingspan, float(self.params.l_stab))
        self.geometry.V_dihedral = gamma(self.geometry.keel_area, self.geometry.aft_area)
        self.geometry.Vtail_area = stab_area(self.geometry.aft_area, self.geometry.V_dihedral)
        self.geometry.P_cruise = P_cruise(self.tom, self.aero.AR, float(self.params.eta_prop), float(self.settings.g))
        self.geometry.wire_length = wire_length(self.geometry.wingspan, float(self.params.l_stab), float(self.settings.wire_scale_coef))
        self.geometry.V_dihedral = math.degrees(gamma(self.geometry.keel_area, self.geometry.aft_area))
        
    def update_m(self, new_m):
        self.tom = new_m
    
    def write_geom(self):
        file = open(self.geometry_file_name, "w")
        for var_name in self.geometry_variables:
            tmp = getattr(self.geometry, var_name)
            file.write(f"{var_name} = {tmp}\n")
        file.close()
     
    def write_aero(self):
        file = open(self.aero_file_name, "w")
        for var_name in self.aero_variables:
            tmp = getattr(self.aero, var_name)
            file.write(f"{var_name} = {tmp}\n")
        file.close()
    
    def write_info(self):
        self.write_geom()
        self.write_aero()

    def weigh(self, log=False):
        reload(md)
        reload(logger)
        
        if self.log_flag:
            logger.log_weigh(self.log_file_name)
        M = md.weigh()
        return M
