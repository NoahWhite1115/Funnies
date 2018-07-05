"""
Comic library 0.1
Written by Noah White

Supports the finding of and the loading of webcomics.
"""

import urllib
import ComicParser

#reads a config file, returns a lits of 3-tuples containing Name, url and formatting of comic
def readConfig():

    #read the config file. Throw an error if one is not found.
    try:
        config_file = open("./.funconfig",'r')
    except:
        print "ERROR: No config file found. Please run ./setup first to initialize directory for first time use."
        exit()

    #convert to 3-tuple
    config_file = config_file.readlines()
    
    comic_info = []
    
    for line in config_file:
        (name,url,info,flags) = line.split(",")
        comic_info.append((name,url,info,flags[:-1]))
        #[:-1] to drop \n from flags

    return comic_info


#comic object
class comic_obj():


    #initialize comic object
    def __init__(self,name,url,info,flags):
        self.name = name
        self.url = url

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
        self.load()
        

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
        if "nm" in self.flags:
            try:
                nm_index = self.flags.index("nm") + 1
                self.max_link_loc = int(self.flags[nm_index])
                self.max_link_needed = True
            except:
                print "WARNING: No max link provided for " + self.name + " even though it was indicated one was needed. Errors may occur."
                self.max_link_needed = False
        else:
            self.max_link_needed = False

        #check for local links
        if "lcl" in self.flags:
            self.lcl = True
            self.base_url = self.url
        else:
            self.lcl = False

        #check if the comic name should be extracted
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
            print "ERROR: Comic " + self.name + " not found at url provided. Please check config file at ./.funconfig to make sure comic is set up correctly."
            self.error = True
            return -2

        #get the max and min indices
        self.max_index = None
        self.min_index = None

        #if a max link is provided, use that
        if self.max_link_needed:
            self.max_index = self.max_link_loc 

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
        #Needs to be more general
        urllib.urlretrieve("https:" + image_url, "./Comics/" + self.name + ".png")

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

            urllib.urlretrieve("https:" + add_image_url, "./Comics/" + self.name + "_ai.png")

    #load the next comic
    def next(self):
        #check if valid
        if self.url == self.max_index:
            print self.name + " is already at max index."
            return

        #Check if link is global or local; adjust accordingly
        for link in self.parser.link_list[self.next_loc]:
            if link[0] == 'href':
                if self.lcl == True:
                    self.url = self.base_url + link[1]
                else:
                    self.url = link[1]

        #get the page
        self.page = urllib.urlopen(self.url).read()
        self.parser.clear()
        self.parser.feed(self.page)


    #load the previous comic
    def prev(self):
        #check if valid
        if self.url == self.min_index:
            print self.name + " is already at min index."
            return

        #Check if link is global or local; adjust accordingly
        for link in self.parser.link_list[self.prev_loc]:
            if link[0] == 'href':
                if self.lcl == True:
                    self.url = self.base_url + link[1]
                else:
                    self.url = link[1]

        #get the page
        self.page = urllib.urlopen(self.url).read()
        self.parser.clear()
        self.parser.feed(self.page)

    #loads a random comic, if enabled
    def random(self):
        #check if valid
        if not self.rand_link:
            print "Warning: random not enabled on " + self.name
            return

        #Check if link is global or local; adjust accordingly
        for link in self.parser.link_list[self.rand_loc]:
            if link[0] == 'href':
                if self.lcl == True:
                    self.url = "https:" + link[1]
                else:
                    self.url = link[1]

        #get the page
        self.page = urllib.urlopen(self.url).read()
        self.parser.clear()
        self.parser.feed(self.page)

#Before running test, save your current version of ./.funconfig as something else and replace it with the following line:
#xkcd,http://xkcd.com,1-7-9,tt-lcl
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

comicTest()
