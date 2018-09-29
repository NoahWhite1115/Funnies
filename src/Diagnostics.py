"""
Diagnostic Library for Funnies
Written by Noah White
Contains a set of functions that provide simple debugging cases.
"""

from ComicLib import ComicObj
from ComicLib import read_config
from ComicParser import ComicParser
from urllib import urlopen
import os

"""
Test function for ComicParser from ComicParser.py
Tests by pulling the http://xkcd.com/1 page.
A change on that website will break this test function
"""


def ParserTest():
    xkcd = urlopen("http://xkcd.com/1").read()

    parser = ComicParser()

    parser.feed(xkcd)

    xkcd = parser.image_list[1][0][1]
    tt = parser.image_list[1][1][1]
    link_p = parser.link_list[7][1][1]
    link_n = parser.link_list[9][1][1]

    if xkcd != "//imgs.xkcd.com/comics/barrel_cropped_(1).jpg":
        print "Wrong image name found"
        print "Expected //imgs.xkcd.com/comics/barrel_cropped_(1).jpg"
        print "Got " + xkcd
        print "Note that this could be due to a change on the website end."
        exit()

    if tt != "Don't we all.":
        print "Wrong title text found"
        print "Expected Don't we all."
        print "Got " + tt
        print "Note that this could be due to a change on the website end."
        exit()

    if link_p != '#':
        print "Wrong prev link found"
        print "Expected #"
        print "Got " + link_p
        print "Note that this could be due to a change on the website end."
        exit()

    if link_n != '/2/':
        print "Wrong next link found"
        print "Expected /2/"
        print "Got " + link_n
        print "Note that this could be due to a change on the website end."
        exit()

    return True


"""
Test function for the ComicObj from ComicLib
Before running test, save your current version of ./.funconfig
as something else and replace it with the following line:
xkcd,https://xkcd.com,1-7-9,rand-8-max-10-min-6-lcl-tt-
"""


def ComicTest():
    xkcdArgs = read_config("..")[0]

    if xkcdArgs[0] != 'xkcd':
        print "Name arg not properly set."
        exit()

    if xkcdArgs[1] != 'https://xkcd.com':
        print "Url arg not properly set."
        exit()

    if xkcdArgs[2] != '1-7-9':
        print "Info arg not properly set."
        exit()

    if xkcdArgs[3] != 'rand-8-max-10-min-6-lcl-tt-':
        print "Flags arg not properly set."
        exit()

    print "No issue with config reader."

    xkcd = ComicObj(xkcdArgs[0], xkcdArgs[1], xkcdArgs[2], xkcdArgs[3])
    xkcd.read()

    print "No issue with comic loading."

    xkcd.min()
    xkcd.read()
    print "No issues with Comic.min()."

    xkcd.next()
    xkcd.read()
    print "No issues with Comic.next()."

    xkcd.prev()
    xkcd.read()
    print "No issues with Comic.prev()."

    xkcd.max()
    xkcd.read()
    print "No issues with Comic.max()."

    xkcd.random()
    xkcd.read()
    print "No issues with Comic.random()."


if __name__ == "__main__":

    if not os.path.exists(os.path.join(".", "Comics")):
        os.makedirs(os.path.join(".", "Comics"))

    ParserTest()
    print "No issues with parser."
    ComicTest()
    print "No issues with comic object."
