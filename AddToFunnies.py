import ComicParser
import urllib

def add_comic():
    
    comic_url = raw_input ("URL of comic to add:")
    comic_name = raw_input ("Name of comic to add:")

    try:
        comic = urllib.urlopen(comic_url).read()
    except:
        print "Unable to read URL given."
        exit()

    parser = ComicParser.ComicParser()

    parser.feed(comic)

    print "Here are a list of images on the page. Please type the number of the one that looks like the main comic."

    index = 0
    for image in parser.image_list:
        print index
        print image
        index += 1

    try:
        comic_index = raw_input("Index: ")
        int(comic_index)
    except:
        print "Not an integer!"
        exit()

    print "Here are a list of links on the page. Please type the number of the one that looks like the next button."

    index = 0
    for link in parser.link_list:
        print index
        print link
        index += 1

    try:
        next_index = raw_input("Next: ")
        int(next_index)
    except:
        print "Not an integer!"
        exit()

    print "Type the index of the prev button."

    try:
        prev_index = raw_input("Prev: ")
        int(prev_index)
    except:
        print "Not an integer!"
        exit()

    




    config_file = open("./.funconfig",'a')
    config_file.write(comic_name + "," + comic_url + "," + comic_index + "-" + prev_index + "-" + next_index + ",")
    config_file.close()

if __name__ == '__main__':
    add_comic()
