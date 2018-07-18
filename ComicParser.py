"""
ComicParser 1.0
Written by Noah White

Designed to make it easier to get webcomics from the internet
Primarily for use with Funnies

Formatting follows PEP 8.0
https://www.python.org/dev/peps/pep-0008/

Uses the GNU GPL 2.0 Lisence.
Check LISENCE for more info.
"""

import urllib
from HTMLParser import HTMLParser


class ComicParser(HTMLParser):
    # Init adds in 2 lists to hold links and images.
    def __init__(self):
        HTMLParser.__init__(self)
        self.link_list = []
        self.image_list = []

    # Add things to link and image lists when feed is called
    def handle_starttag(self, tag, attrs):
        # Get all images on a page
        if tag == "img":
            image_attrs = []

            for attr in attrs:
                image_attrs.append(attr)

            self.image_list.append(image_attrs)

        # Get all links on a page
        if tag == "a":
            link_attrs = []

            for attr in attrs:
                link_attrs.append(attr)

            self.link_list.append(link_attrs)

    # Removes the previous lists so that new ones can be loaded.
    def clear(self):
        self.link_list = []
        self.image_list = []


def ParserTest():
    # Tests on xkcd #1
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
