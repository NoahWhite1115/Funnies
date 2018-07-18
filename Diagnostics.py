"""
Diagnostic Library for Funnies
Written by Noah White
Contains a set of functions that provide simple debugging cases.
"""

from ComicLib import ComicObj
from ComicParser import ComicParser

"""
Test function for ComicParser from ComicParser.py
Tests by pulling the http://xkcd.com/1 page.
A change on that website will break this test function
"""


def ParserTest():
    xkcd = urllib.urlopen("http://xkcd.com/1").read()

    parser = ComicParser()

    parser.feed(xkcd)

    for i in parser.link_list:
        print i

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
xkcd,http://xkcd.com,1-7-9,tt-lcl-rand-8
"""


def comicTest():
    xkcdArgs = readConfig()[0]

    if xkcdArgs[0] != 'xkcd':
        print "Name arg not properly set."
        exit()

    if xkcdArgs[1] != 'http://xkcd.com':
        print "Url arg not properly set."
        exit()

    if xkcdArgs[2] != '1-7-9':
        print "Info arg not properly set."
        exit()

    if xkcdArgs[3] != 'tt-lcl-rand-8':
        print "Flags arg not properly set."

    xkcd = comic_obj(xkcdArgs[0], xkcdArgs[1], xkcdArgs[2], xkcdArgs[3])
    xkcd.read()

    xkcd.prev()
    xkcd.read()
    xkcd.random()
    xkcd.read()
    print xkcd.title_text
