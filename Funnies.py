#comic class:

#read /w no args gets the most recent comic, loads it under ./comics/name.png/ or ./comics/name.jpg
#read /w args gets the comic at that index
#read's args determined by info string

#show returns the file location of the current stored comic. 

#index returns the index the comic is currently set to
#max_index gets the highest possible index

#name gets the comics name

#read_next() gets the next comic in order (and then calls read)
#read_prev() gets the prev comic in order (and then calls read)




def main():
    #read/split config file as a list of 3-tuples (Name,URL,info_string).
    config_list = readConfig()

    #create a list holding all the comic objects
    for comic in config_list:
        comic_list.append(comic_object(comic))

    #call the read method on all comic objects
    for comic in comic_list:
        comic.read()

    Comic = launchComicGUI()
