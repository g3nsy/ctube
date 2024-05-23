import os


HOME = os.path.expanduser("~")
MUSIC = os.path.join(HOME, "Music")
USER_CONFIG_DIR = os.path.join(HOME, ".config")
CLITUBE_CONFIG_DIR = os.path.join(USER_CONFIG_DIR, "clitube")
CONFIG = os.path.join(CLITUBE_CONFIG_DIR, "clitube.toml")
