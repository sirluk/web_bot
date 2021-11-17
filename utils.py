import re
import os
from typing import Tuple, Callable
from functools import wraps


def str2bool(string: str) -> bool:
    """Converts a string to boolean dtype
    Accepted values for true ["yes", "true", "t", "1"]
    Args:
        string (str): the string to convert
    Returns:
        bool: converted boolean value
    """    
    return string.lower() in ("yes", "true", "t", "1") 


def get_env_vars(match_pattern: re.Pattern) -> list:
    return [v for k,v in os.environ.items() if re.match(match_pattern, k)]


def on_off_check(
    on_off: bool = True,
    return_on: Tuple[str, int] = ("ON", 200),
    return_off: Tuple[str, int] = ("OFF", 201),
    custom_on: bool = False
    ) -> Callable:
    """Generate Decorator for Flask function which implicitely handles return values based on ON OFF state 
    of application. 
    Args:
        on_off (bool, optional): Wether function state is ON or OFF. Defaults to True (=ON).
        return_on (Tuple[str, int], optional): Dummy return value if function is turned on. 
            Only used if custom_on=False. Defaults to ("ON", 200).
        return_off (Tuple[str, int], optional): Dummy return value if function is turned off. 
            Defaults to ("OFF", 201).
        custom_on (bool, optional): If function has its own return value output this if function 
            is turned on. Defaults to False.
    Returns:
        Callable: Decorator
    """    
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if on_off:
                x = f(*args, **kwargs)
                if custom_on:
                    return x
                else:
                    return return_on
            else:
                return return_off
        return wrapped
    return wrapper