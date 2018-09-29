import ComicParser
import urllib
from os.path import join


def add_comic():

    comic_url = raw_input("URL of comic to add: ")
    comic_name = raw_input("Name of comic to add: ")
    flags = ""

    try:
        comic = urllib.urlopen(comic_url).read()
    except:
        print "Unable to read URL given."
        exit()

    parser = ComicParser.ComicParser()

    parser.feed(comic)

    # Set up main comic
    print "Here are a list of images on the page."
    print "Please type the number of the one that looks like the main comic."

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

    # Next and prev links
    print "Here are a list of links on the page."
    print "Please type the number of the one that looks like the next button."

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

    # Get the random button
    user_input = raw_input("Does this comic have a random link? Y/N: ").lower()
    if user_input == "y" or user_input == "yes":
        flags += "rand-"

        print "Type the index of the rand button."
        try:
            rand_index = raw_input("Rand: ")
            int(rand_index)
            flags += (rand_index + "-")
        except:
            print "Not an integer!"
            exit()

    elif user_input != "n" and user_input != "no":
        print "Did not understand that input. Please type y or n."
        exit()

    # Get the max button
    print "Does this comic have a max/newest link?"
    user_input = raw_input("Y/N: ").lower()
    if user_input == "y" or user_input == "yes":

        print "Does the link provided link to the max comic?"
        user_input = raw_input("Y/N: ").lower()
        if user_input == "y" or user_input == "yes":
            flags += "max-"
        elif user_input == "n" or user_input == "no":
            flags += "nm-"
        else:
            print "Did not understand that input. Please type y or n."
            exit()

        print "Type the index of the max button."
        try:
            max_index = raw_input("Max: ")
            int(max_index)
            flags += (max_index + "-")
        except:
            print "Not an integer!"
            exit()

    # Get the min button
    print "Does this comic have a min/first link?"
    user_input = raw_input("Y/N: ").lower()
    if user_input == "y" or user_input == "yes":
        flags += "min-"

        print "Type the index of the min button."
        try:
            min_index = raw_input("Min: ")
            int(min_index)
            flags += (min_index + "-")
        except:
            print "Not an integer!"
            exit()

    elif user_input != "n" or user_input != "no":
        print "Did not understand that input. Please type y or n."
        exit()

    # Local links
    print "Are the links and images on this page local links;\
i.e. links are just /1 rather than comic.com/1?"

    user_input = raw_input("Y/N: ").lower()
    if user_input == "y" or user_input == "yes":
        flags += "lcl-"
    elif user_input != "n" and user_input != "no":
        print "Did not understand that input. Please type y or n."
        exit()

    # Title text
    print "Does this image have title text (also known as mouseover text)?"
    user_input = raw_input("Y/N: ").lower()
    if user_input == "y" or user_input == "yes":
        flags += "tt-"
    elif user_input != "n" and user_input != "no":
        print "Did not understand that input. Please type y or n."
        exit()

    # Additional image
    print "Does this comic have an additional image?"
    user_input = raw_input("Y/N: ").lower()
    if user_input == "y" or user_input == "yes":
        flags += "ai-"

        print "Here are a list of images on the page."
        print "Type the number of one that looks like the additional comic."

        index = 0
        for image in parser.image_list:
            print index
            print image
            index += 1

        try:
            ai_index = raw_input("Index: ")
            int(ai_index)
            flags += (ai_index + "-")
        except:
            print "Not an integer!"
            exit()

    elif user_input != "n" and user_input != "no":
        print "Did not understand that input. Please type y or n."
        exit()

    config_file = open(join(".", ".funconfig"), "a")
    config_file.write(
            comic_name + ","
            + comic_url + ","
            + comic_index + "-"
            + prev_index + "-"
            + next_index + ","
            + flags
            )
    config_file.close()


if __name__ == '__main__':
    add_comic()
