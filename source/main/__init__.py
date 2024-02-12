import sys
from os.path import abspath, dirname, realpath


# autopep8: off
PATH = realpath(abspath(__file__))
sys.path.insert(0, dirname(dirname(PATH)))
# autopep8: on