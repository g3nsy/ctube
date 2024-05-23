from ctube.cmds import Commands


class CTubeError(Exception):
    """Music Downloader Base Exception"""


class InvalidCommandArgument(CTubeError):
    """ """
    def __init__(self, cmd: Commands):
        self.cmd = cmd


class InvalidSyntax(CTubeError):
    """ """


class InvalidIndexSyntax(InvalidSyntax):
    """ """
