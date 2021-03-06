"""
Comic library 1.0
Written by Noah White

Supports the finding of and the loading of webcomics.

Formatting follows PEP 8.0
https://www.python.org/dev/peps/pep-0008/

Uses the GNU GPL 2.0 Lisence.
Check LISENCE for more info.
"""

import urllib
import ComicParser
from os.path import join


"""
readConfig(path)
reads the config file
takes an optional path variable to where the config file is (.funconfig)
returns a lits of 3-tuples containing Name, url and formatting of comic
"""


def read_config(path="."):

    # Read the config file at .funconfig. Throw an error if one is not found.
    try:
        config_file = open(join(path, ".funconfig"), 'r')
    except:
        print "ERROR: No config file found."
        print "Run ./AddToFunnies first to initialize config file."
        exit()

    # Convert to 3-tuple
    config_file = config_file.readlines()

    comic_info = []

    for line in config_file:
        (name, url, info, flags) = line.split(",")
        comic_info.append((name, url, info, flags[:-1]))
        # [:-1] to drop \n from flags

    return comic_info


"""
ComicObj
Designed to handle grabbing comics from the internet.
Takes 5 arguements on initialization:
    name: name of comic as string
    url: url of comic as string
    info: 3 integers describing comic, back and forward link indexes.
        Passed as a string with '-' characters seperating the values.
    flags: Optional flags, describing other things about the comic.
        Passed as a string with '-' characters seperating the values.
    path (optional): Path of where to save comics. '.' by default.
"""


class ComicObj():

    # Initialization of the comic object
    def __init__(self, name, url, info, flags, path=join(".", "Comics")):
        self.name = name
        self.url = url
        self.path = path

        # Quick info index list
        # 0 is what image in parser the comic url is stored at
        # 1 and 2 are the links in parser where next and prev are stored.
        self.info = info.split("-")
        self.flags = flags.split("-")

        self.flag_parsing()

        # All info processing is done below
        # Get comic/link locations
        self.comic_loc = int(self.info[0])
        self.prev_loc = int(self.info[1])
        self.next_loc = int(self.info[2])

        self.parser = ComicParser.ComicParser()
        self.page = ""

        self.error = False
        code = self.load()
        if code == -2:
            self.error = True

    """
    ComicObj.flag_parsing()
    takes: nothing
    returns: nothing
    designed to parse the flags passed in __init__
    private
    """
    def flag_parsing(self):
        # Check if title text is wanted
        if "tt" in self.flags:
            self.title = True
        else:
            self.title = False

        # Check if additional image is wanted
        if "ai" in self.flags:
            try:
                ai_index = self.flags.index("ai") + 1
                self.ai_image_loc = int(self.flags[ai_index])
                self.add_image = True
            except:
                print "WARNING: Invalid index provided for additional image."
                print "Additional image will be disabled for " + self.name
                self.add_image = False
        else:
            self.add_image = False

        # Check if random link is provided
        if "rand" in self.flags:
            try:
                rand_index = self.flags.index("rand") + 1
                self.rand_loc = int(self.flags[rand_index])
                self.rand_link = True
            except:
                print "WARNING: Invalid index provided for random link."
                print "Random link will be disabled for " + self.name
                self.rand_link = False
        else:
            self.rand_link = False

        # If url provided in script isn't guarunteed to be the max url,
        # Then a link to the max comic must be provided.
        if "nm" in self.flags or "max" in self.flags:
            try:
                if "nm" in self.flags:
                    max_index = self.flags.index("nm") + 1
                    self.max_link_needed = True

                elif "max" in self.flags:
                    max_index = self.flags.index("max") + 1
                    self.max_link_needed = False

                self.max_link_loc = int(self.flags[max_index])
                self.max_link = True
            except:
                print "WARNING: Invalid max link provided for " + self.name
                + " even though it was indicated one was needed."
                print "Errors may occur."
                self.max_link = False
                self.max_link_needed = False
        else:
            self.max_link_needed = False
            self.max_link = False

        # Get min link
        if "min" in self.flags:
            try:
                min_index = self.flags.index("min") + 1
                self.min_link_loc = int(self.flags[min_index])
                self.min_link = True
            except:
                print "WARNING: Invalid min link provided for " + self.name
                self.min_link = False
        else:
            self.min_link = False

        # Check for local links
        if "lcl" in self.flags:
            self.lcl = True
            self.base_url = self.url
        else:
            self.lcl = False
            self.base_url = None

    """
    ComicObj.load()
    takes: nothing
    returns: an error code or None
    Sets the min and max indexes for the ComicObj.
    Private
    """
    def load(self):
        # Check if the url even loads
        try:
            self.page = urllib.urlopen(self.url).read()
            self.parser.feed(self.page)

        except:
            print "Warning: Comic " + self.name + " not found at url provided."
            print "Check config file to ensure comic is set up correctly."
            self.error = True
            return -2

        # Get the max and min indices
        self.max_index = None
        self.min_index = None

        # If a max link is provided, use that
        if self.max_link_needed:
            self.max()
            self.prev()
            self.next()
            self.max_index = self.url

        # Otherwise, just go back and then forward
        else:
            try:
                self.prev()
                self.next()
                self.max_index = self.url
            except:
                print "WARNING: Issue getting max index for " + self.name

        # If a min link is provided, get the min index
        if self.min_link:
            original_url = self.url
            self.min()
            self.min_index = self.url
            self.url = original_url

            # Get the page
            self.page = urllib.urlopen(self.url).read()
            self.parser.clear()
            self.parser.feed(self.page)

    """
    ComicObj.read()
    takes: nothing
    returns: nothing
    Downloads the comic and any additional info needed.
    Public
    """
    def read(self):
        # Do nothing if error in loading
        if self.error:
            return

        image = self.parser.image_list[self.comic_loc]

        # Get image url
        for img in image:
            if img[0] == 'src':
                image_url = img[1]

        # Get url
        if self.lcl:
            urllib.urlretrieve(
                "https:" + image_url,
                join(self.path, self.name + ".png")
            )
        else:
            urllib.urlretrieve(image_url, join(self.path, self.name + ".png"))

        # Get title text
        if self.title:
            for img in image:
                if img[0] == 'title':
                    self.title_text = img[1]

        # Get additional image
        if self.add_image:
            add_image = self.parser.image_list[self.ai_image_loc]
            for img in add_image:
                if img[0] == 'src':
                    add_image_url = img[1]

            # Get url
            if self.lcl:
                urllib.urlretrieve(
                    "https:" + add_image_url,
                    join(self.path, self.name + "_ai.png")
                )
            else:
                urllib.urlretrieve(
                    add_image_url,
                    join(self.path, self.name + "_ai.png")
                )

    """
    ComicObj.next()
    takes: nothing
    returns: nothing
    Loads the next comic
    Public
    """
    def next(self):
        # Check if valid
        if self.url == self.max_index:
            print self.name + " is already at max index."
            return

        self.get_comic(self.next_loc, self.base_url)

    """
    ComicObj.prev()
    takes: nothing
    returns: nothing
    Loads the previous comic
    Public
    """
    def prev(self):
        # Check if valid
        if self.url == self.min_index:
            print self.name + " is already at min index."
            return

        self.get_comic(self.prev_loc, self.base_url)

    """
    ComicObj.random()
    takes: nothing
    returns: nothing
    Loads a random comic
    Public
    """
    def random(self):
        # Check if valid
        if not self.rand_link:
            print "Warning: random not enabled on " + self.name
            return

        self.get_comic(self.rand_loc, "https:")

    """
    ComicObj.max()
    takes: nothing
    returns: nothing
    Loads the max comic
    Public
    """
    def max(self):
        # Check if valid
        if not self.max_link:
            print "Warning: max not enabled on " + self.name
            return
        if self.url == self.max_index:
            print "Warning: already at max on " + self.name
            return
        self.get_comic(self.max_link_loc, self.base_url)

    """
    ComicObj.min()
    takes: nothing
    returns: nothing
    Loads the first comic
    Public
    """
    # Loads min comic, if enabled
    def min(self):
        # Check if valid
        if not self.min_link or self.url == self.min_index:
            print "Warning: min not enabled on " + self.name
            return
        if self.url == self.min_index:
            print "Warning: already at min on " + self.name
            return

        self.get_comic(self.min_link_loc, self.base_url)

    """
    ComicObj.get_comic()
    takes:
        loc: the index of the link to load
        lcl_prefix: the prefix to append if the link is local
    returns: nothing
    Adjusts the link to get the comic from the internet
    Private
    """
    # Get the comic from the web
    def get_comic(self, loc, lcl_prefix):
        # Do nothing if error has occurred
        if self.error:
            return

        # Check if link is global or local; adjust accordingly
        for link in self.parser.link_list[loc]:
            if link[0] == 'href':
                if self.lcl:

                    self.url = lcl_prefix + link[1]

                else:
                    self.url = link[1]

        # Get the page
        self.page = urllib.urlopen(self.url).read()
        self.parser.clear()
        self.parser.feed(self.page)


# Before running test, save your current version of ./.funconfig
# as something else and replace it with the following line:
# xkcd,http://xkcd.com,1-7-9,tt-lcl-rand-8
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
