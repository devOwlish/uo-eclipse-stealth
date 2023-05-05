"""
    Misc helpers
"""
from py_stealth import *

def cancel_targets():
    """
        Cancel target and wait target
    """
    if TargetPresent():
        CancelTarget()
    CancelWaitTarget()
