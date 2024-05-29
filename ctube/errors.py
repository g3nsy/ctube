class CTubeError(Exception):
    """ctube base exception. All exceptions contained in 
       this module inherit from this one."""


class InvalidIndexSyntax(CTubeError):
    """ Occurs when the user provides an argument 
        to the 'download' command with invalid syntax."""


class NoMP4StreamAvailable(CTubeError):
    """ Occurs when no stream with subtype mp4 is available. """


class EmptyStreamQuery(CTubeError):
    """This occurs when there are no streams for a song."""
