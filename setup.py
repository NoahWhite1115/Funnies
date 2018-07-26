"""
Setup.py 1.0
Authored by Noah White

Sets up Funnies for use.
"""

from os.path import abspath
from os.path import join
from os import name

path = abspath('Funnies.py')

#linux/mac case
if name == 'posix':
    exe_file = open("./funnies", 'w')
    exe_file.write("python " + path)
#windows case
else:
    exe_file = open("./funnies.bat",'w')
    exe_file.write("python " + path)
