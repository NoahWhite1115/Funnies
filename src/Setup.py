"""
Setup.py 1.0
Authored by Noah White

Sets up Funnies for use.
"""

from os.path import abspath
from os.path import join

path = abspath('./src/Funnies.py')

exe_file = open("./funnies", 'w')

exe_file.write("python2 " + path)
