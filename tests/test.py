import sys
import os 

CODE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CODE_PATH)

from ctube.cli import main


main()
