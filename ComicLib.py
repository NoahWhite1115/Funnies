"""
Comic library 1.0
Written by Noah White

Supports the finding of and the loading of webcomics.

Formatting follows PEP 8.0
https://www.python.org/dev/peps/pep-0008/
"""

import urllib
import ComicParser
from os.path import join


"""
readConfig(path)
reads the config file
takes an optional path variable to where the config file is
returns a lits of 3-tuples containing Name, url and formatting of comic
"""
def readConfig(path = "."):

    #read the config file. Throw an error if one is not found.
    try:
        config_file = open( join(path,".funconfig"), 'r')
    except:
        print "ERROR: No config file found. Please run ./setup first to initialize directory for first time use." #Too long   
        exit()

    #convert to 3-tuple
    config_file = config_file.readlines()

    comic_info = []
    
    for line in config_file:
        (name,url,info,flags) = line.split(",")
        comic_info.append((name,url,info,flags[:-1]))
        #[:-1] to drop \n from flags

    return comic_info


"""
Comic object
Designed to handle grabbing comics from the internet.
Takes 5 arguements:
    name: name of comic as string
    url: url of comic as string
    info: 3 integers describing comic, back and forward link indexes.
        Passed as a string with '-' characters seperating the values.
    flags: Optional flags, describing other things about the comic.
        Passed as a string with '-' characters seperating the values.
    path (optional): Path of where to save comics. '.' by default.

Functions provided:
    flag_parsing():
        parses flags to set up the comic obj
    load():
        makes sure the url can be opened and sets max and min comics.
    
"""
class comic_obj():

    #initialization of the 
    def __init__(self,name,url,info,flags,path = join(".","Comics")):
        self.name = name
        self.url = url
        self.path = path

        #quick info index list
            #0 is what image in parser the comic url is stored at
            #1 and 2 are the links in parser where next and prev are stored.

        self.info = info.split("-")
        self.flags = flags.split("-")
       
        self.flag_parsing()

        #All info processing is done below
        #Get comic/link locations
        self.comic_loc = int(self.info[0])
        self.prev_loc = int(self.info[1])
        self.next_loc = int(self.info[2])

        self.parser = ComicParser.ComicParser()
        self.page = ""

        self.error = False
        code = self.load()
        if code == -2:
            self.error = True
        

    #Handles the self.flags list
    def flag_parsing(self):
        #Check if title text is wanted
        if "tt" in self.flags:
            self.title = True
        else:
            self.title = False

        #Check if additional image is wanted
        if "ai" in self.flags:
            try:            
                ai_index = self.flags.index("ai") + 1
                self.ai_image_loc = int(self.flags[ai_index])
                self.add_image = True
            except:
                print "WARNING: Invalid index provided for additional image. Additional image will be disabled for " + self.name
                self.add_image = False
        else:
            self.add_image = False

        #Check if random link is provided
        if "rand" in self.flags:
            try:
                rand_index = self.flags.index("rand") + 1
                self.rand_loc = int(self.flags[rand_index])
                self.rand_link = True
            except:
                print "WARNING: Invalid index provided for random link. Random link will be disabled for " + self.name
                self.rand_link = False
        else:
            self.rand_link = False

        #If url provided in script isn't guarunteed to be the max url, then a link to the max comic must be provided.
        if "nm" in self.flags or "max" in self.flags:
            try:
                nm_index = self.flags.index("nm") + 1
                self.max_link_loc = int(self.flags[nm_index])
                self.max_link = True
                if "nm" in self.flags:
                    self.max_link_needed = True
            except:
                print "WARNING: Invalid max link provided for " + self.name + " even though it was indicated one was needed. Errors may occur."
                self.max_link = False
                self.max_link_needed = False
        else:
            self.max_link_needed = False
            self.max_link = False

        #get min link
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

        #check for local links
        if "lcl" in self.flags:
            self.lcl = True
            self.base_url = self.url
        else:
            self.lcl = False
            self.base_url = None

        #check if the comic name should be extracted
        #needs full implementation someday
        if "name" in self.flags:
            self.named = True
            
        else:
            self.named = False

    #check comic url, get max and min indices
    def load(self):
        #Check if the url even loads
        try:
            self.page = urllib.urlopen(self.url).read()
            self.parser.feed(self.page)

        except:
            print "Warning: Comic " + self.name + " not found at url provided. Please check config file at ./.funconfig to make sure comic is set up correctly."
            self.error = True
            return -2

        #get the max and min indices
        self.max_index = None
        self.min_index = None

        #if a max link is provided, use that
        if self.max_link_needed:
            self.max()
            self.prev()
            self.next()
            self.max_index = self.url

        #otherwise, just go back and then forward
        else:
            try: 
                self.prev()
                self.next()
                self.max_index = self.url
            except:
                print "WARNING: Issue getting max index for " + self.name

    #downloads the current comic
    def read(self):
        #Do nothing if error in loading
        if self.error == True:
            return    

        image = self.parser.image_list[self.comic_loc]
    
        #get image url
        for img in image:
            if img[0] == 'src':
                image_url = img[1]

        #get url
        if self.lcl == True:            
            urllib.urlretrieve("https:" + image_url, join(self.path, self.name + ".png"))
        else:
            urllib.urlretrieve(image_url, join(self.path,self.name + ".png"))

        #get title text
        if self.title == True:
            for img in image:
                if img[0] == 'title':
                    self.title_text = img[1]

        #get additional image
        if self.add_image == True:
            add_image = self.parser.image_list[self.ai_image_loc]
            for img in add_image:
                if img[0] == 'src':
                    add_image_url = img[1]

            #get url
            if self.lcl == True:            
                urllib.urlretrieve("https:" + add_image_url, join(self.path,self.name + "_ai.png"))
            else:
                urllib.urlretrieve(add_image_url, join(self.path,self.name + "_ai.png"))

    #load the next comic
    def next(self):
        #check if valid
        if self.url == self.max_index:
            print self.name + " is already at max index."
            return

        self.get_comic(self.next_loc,self.base_url)

    #load the previous comic
    def prev(self):
        #check if valid
        if self.url == self.min_index:
            print self.name + " is already at min index."
            return

        self.get_comic(self.prev_loc,self.base_url)

    #loads a random comic, if enabled
    def random(self):
        #check if valid
        if not self.rand_link:
            print "Warning: random not enabled on " + self.name
            return

        self.get_comic(self.rand_loc,"https:")

    #loads max comic, if enabled
    def max(self):
        #check if valid
        if not self.max_link:
            print "Warning: max not enabled on " + self.name
            return
        if self.url == self.max_index:
            print "Warning: already at max on " + self.name
            return
        self.get_comic(self.max_link_loc,"https:")

    #loads min comic, if enabled
    def min(self):
        #check if valid
        if not self.min_link or self.url == self.min_index:
            print "Warning: min not enabled on " + self.name
            return
        if self.url == self.min_index:
            print "Warning: already at min on " + self.name
            return

        self.get_comic(self.min_link_loc,"https:")

    #get the comic from the web
    def get_comic(self,loc,lcl_prefix):
        #do nothing if error has occurred
        if self.error == True:
            return
        
        #Check if link is global or local; adjust accordingly
        for link in self.parser.link_list[loc]:
            if link[0] == 'href':
                if self.lcl == True:

                    self.url = lcl_prefix + link[1]

                else:
                    self.url = link[1]

        #get the page
        self.page = urllib.urlopen(self.url).read()
        self.parser.clear()
        self.parser.feed(self.page)

#Before running test, save your current version of ./.funconfig as something else and replace it with the following line:
#xkcd,http://xkcd.com,1-7-9,tt-lcl-rand-8
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

    xkcd = comic_obj(xkcdArgs[0],xkcdArgs[1],xkcdArgs[2],xkcdArgs[3])
    xkcd.read()

    xkcd.prev()
    xkcd.read()
    xkcd.random()
    xkcd.read()
    print xkcd.title_text

