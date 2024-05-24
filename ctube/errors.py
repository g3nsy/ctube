class CTubeError(Exception):
    """ctube base exception. All exceptions contained in 
       this module inherit from this one."""


class InvalidCommandArgument(CTubeError):
    """It occurs when at least one argument passed as input 
       to a command is considered invalid."""


class CommandNotFoundError(CTubeError):
    """It occurs when the user provides an unknown command."""


class ArtistNotFoundError(CTubeError):
    """This occurs when, during the process of extracting 
       an artist's id, the id is not found."""


class ContentNotFoundError(CTubeError):
    """This occurs when, during the process of extracting 
       an artist's content, the content is not found."""


class InvalidIndexSyntax(CTubeError):
    """ """
