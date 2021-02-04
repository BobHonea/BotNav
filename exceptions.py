'''
exceptions.py
Custom Exceptions for NavBot
'''


class NavError(BaseException):
    """Base class for other exceptions"""
    pass


class ShapeOutOfBounds(NavError):
    """A Shape Crosses Straddles A Boundary"""
    pass
