"""Custom exception classes
"""

class InsufficientInputData(Exception):
    """Insufficient Input Data

    Raised when there is not enough input data from user files (such as a SETTINGS-file, etc.)

    Cases of raising:
    1) When processing files in the process-functions of the Sculptor class, no critical parameters were found in them.
    
    2) If in weigh-function indicate_missing_param_vals == 1 and user answerd "n" to the question about skipping the parameter
    
    3) If in weigh-function a non-existent related parameter is specified
    """
    def __init__(self, text):
        self.txt = text
