class PalletConflictError(Exception):
    pass

#Helper Function
def parse_weight(weight_string):
    
    if not isinstance(weight_string, str):
        raise TypeError