import pandas as pd
import numpy as np
from handlers import isnan

from aerolib import *
from xfoillib import *
from exceptions import *


class Sculptor():
    """ **Sculptor is a calculator of plane geometry.**
    It uses parametrs and a some requirements (performance) to 
    calculate geometry and weidth of a plane.
    """
    def __init__(self, performance_file_name, params_file_name, settings_file_name, m):
        """The Sculptor class initializer.
        
        :param performance_file_name:      The name of file, where performance is defined. It must be an .csv file, filled in a certain way. For more information, see the section performance file format.
        :type performance_file_name:       str
        :param params_file_name:      The name of file, where params is defined. It must be an .csv file, filled in a certain way. For more information, see the section params file format.
        :type params_file_name:       str
        :param settings_file_name:      The name of file, where settings is defined. It must be an .csv file, filled in a certain way. For more information, see the section settings file format.
        :type settings_file_name:       str
        :param m:     a first approximation of the plane mass value.
        :type m:      float
        
        :return: none
        """
        self.params_file_name: str = params_file_name
        """The name of file, where performance is defined."""
        self.geom_file_name: str = "GEOM.csv"
        """The name of file, where geometry of plane will be placed."""
        
        self.aero_file_name: str = "AERO.csv"
        """The name of file, where cruising characteristics will be placed. **Сurrently not supported!**"""
        
        df = pd.read_csv(performance_file_name, header=None)[1:]
        self.performance: dict = dict(zip(df[0], [float(x) for x in df[1]]))
        """Dataframe formed from performance_file_name-file"""
        self.preprocess_performance()

        df = pd.read_csv(settings_file_name, header=None)[1:]
        self.settings: dict = dict(zip(df[0], [x for x in df[1]]))
        """Dataframe formed from settings_file_name-file"""
        self.preprocess_settings()

        df=pd.read_csv(params_file_name, index_col=False)
        self.params: dict = dict(filter(lambda x: x[0][0]!="#", dict(zip(df["NAME"], [float(x) for x in df["VALUE"]])).items()))
        """Dataframe formed from params_file_name-file"""
        self.preprocess_params()

        self.geom: dict = {}
        """Dataframe formed from geom_file_name-file"""
        self.aero = {"cruise":np.nan}
        """Dataframe formed from aero_file_name-file"""
        self.tom = m
        """The weight of the aircraft in kilograms"""

    def preprocess_params(self):
        """Checking the parameter dataframe - params
        
        The developers have set a list of critical parameters. That is, those without which the calculation will not make sense at all. Their values are required. This function checks the dataframe for all critical parameters
        
        :return: none
        """
        critical_params = ['CL_take_off', 'eta_prop', 'A_aft', 
                           'B_keel', 'l_stab']
        for name in critical_params:
            if isnan(self.params.get(name, np.nan)):
                raise InsufficientInputData(f'obligatory parametr {name} not found')

    def preprocess_performance(self):
        """Checking the parameter data frames - performance
        
        The developers have set a list of critical parameters. That is, those without which the calculation will not make sense at all. Their values are required. This function checks the dataframe for all critical parameters
        
        :return: none
        """
        critical_performance = ['cruise_speed', 'take_off_speed', 'flight_time']
        for name in critical_performance:
            if isnan(self.performance.get(name, np.nan)):
                raise InsufficientInputData(f'obligatory parametr {name} not found')
    
    def preprocess_settings(self):
        """Checking the parameter dataframe - settings
        
        The developers have set a list of critical parameters. That is, those without which the calculation will not make sense at all. Their values are required. This function checks the dataframe for all critical parameters
        
        :return: none
        """
        if isnan(self.settings.get('g', np.nan)):
            self.settings['g'] = 9.81
            
        if isnan(self.settings.get('density', np.nan)):
            self.settings['density'] = 1.22

        if isnan(self.settings.get('wire_scale_coef', np.nan)):
            self.performance['wire_scale_coef'] = 1.3
        
        critical_settings = ['dyn_viscosity', 'density', 'g', 'Re', 'M', 
                             'xfoil_max_it', 'ncr', 'alpha_min', 'alpha_max', 'alpha_step', 
                             'ar_min', 'ar_max', 'ar_delta', 'osvald_coef', 
                             'wire_scale_coef', 'XFoil_path', 'foil1_name', 'work_dir']
        for name in critical_settings:
            if isnan(self.settings.get(name, np.nan)):
                raise InsufficientInputData(f'obligatory parametr {name} not found')

    def calculate_geometry(self):
        """Geometry calculation.
        
        This function fills the geom data frames using functions from the aerolib library
        
        :return: none
        """
  
        self.geom["wing_area"] = wing_area(self.tom, float(self.settings["g"]),
                                           float(self.settings["density"]), 
                                           float(self.performance["take_off_speed"]), 
                                           float(self.params["CL_take_off"]))
        CL_cr = CL_cruise(self.tom, self.performance["cruise_speed"],
                               float(self.geom["wing_area"]), float(self.settings["g"]), 
                               float(self.settings["density"]))
        ar_step_number = int(abs(float(self.settings["ar_max"]) - float(self.settings["ar_min"])) // float(self.settings["ar_delta"]))
        
        ar_range = np.linspace(float(self.settings["ar_min"]), float(self.settings["ar_max"]), ar_step_number)
        
        self.geom["AR"] = AR_selector(ar_range, self.geom, 
                                      self.settings, self.performance, self.tom)
        self.aero["cruise"] = K_V_solver(self.geom, self.settings, 
                                         self.performance["cruise_speed"], 
                                         self.geom["AR"], self.tom)
        self.geom["ba"] = ba(self.geom["AR"], self.geom["wing_area"])
        self.geom["wingspan"] = wingspan(self.geom["AR"], self.geom["wing_area"])
        self.geom["aft_area"] = aft_area(float(self.params["A_aft"]), 
                                         self.geom["wing_area"], self.geom["ba"], 
                                         float(self.params["l_stab"]))
        self.geom["keel_area"] = keel_area(float(self.params["B_keel"]), 
                                           self.geom["wing_area"], self.geom["wingspan"], 
                                           float(self.params["l_stab"]))
        self.geom["V_dihedral"] = gamma(self.geom["keel_area"], self.geom["aft_area"])
        self.geom["Vtail_area"] = stab_area(self.geom["aft_area"], self.geom["V_dihedral"])
        self.geom["P_cruise"] = P_cruise(self.tom, self.aero["cruise"].K[0], 
                                        float(self.params["eta_prop"]), float(self.settings["g"]))
        self.geom["wire_length"] = wire_length(self.geom["wingspan"], float(self.params["l_stab"]), 
                                              float(self.settings["wire_scale_coef"]))

        self.geom["V_dihedral"] = math.degrees(gamma(self.geom["keel_area"], self.geom["aft_area"]))
        
    def update_m(self, new_m):
        """A simple setter.
        
        This function sets a new value to tom
        
        :return: none
        """
        self.tom = new_m
    
    def write_geom(self):
        """Writing to a file
        
        Writes the contents of the geom data frames to the geom_file_name file
        
        :return: none
        """
        with open(self.geom_file_name, 'w') as f:
            f.write("%s, %s\n" % ("NAME", "VALUE"))
            for key in self.geom.keys():
                f.write("%s, %s\n" % (key, self.geom[key]))
    
    def write_aero(self):
        """Writing to a file
    
    	Writes the contents of the aero data frames to the aero_file_name file
    	
        :return: none
        """
        with open(self.aero_file_name, 'w') as f:
            f.write("%s, %s\n" % ("NAME", "VALUE"))
            for key in self.aero.keys():
                f.write("%s, %s\n" % (key, self.aero[key]))
    
    def write_info(self):
        """Writing to a file
    
    	Writes the contents of the aero and geom data frames to the aero_file_name and geom_file_name files
    	
        :return: none
        """
        self.write_geom()
        self.write_aero()
        
        

    def get_data_to_weigh(self):
        """ A hendler to use weight-function
	
	Read more about the weight function
    	
	:return: a list with the file names params_file_name and geom_file_name
	:rtype: list
	"""
        return [self.params_file_name, self.geom_file_name]
