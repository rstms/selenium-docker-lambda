# NFAtools Fatal Exceptions

class NFAToolsException(Exception):
    """base class for NFATools exceptions"""
    pass

class LoginTimeoutException(NFAToolsException):
    """called when a timeout occurs while waiting for the front page to be ready after a login"""
    pass

class EformsFailure(NFAToolsException):
    """Called when an eforms DOM sync or element location fails"""
    pass
