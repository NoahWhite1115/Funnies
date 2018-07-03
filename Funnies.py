#Funnies 0.00
#Written by Noah White
from Tkinter import *
import ComicLib

class ComicGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
    
    def widgets(self):
        self.parent.title("Funnies: Python Webcomic Browser")


def main():
    #read/split config file as a list of 3-tuples (Name,URL,info_string).
    config_list = ComicLib.readConfig()


    #create a list holding all the comic objects
    comic_list = []

    for comic in config_list:
        x = ComicLib.comic_obj(comic[0],comic[1],comic[2],comic[3])
        comic_list.append(x)
        x.read()

    top = Tk()
    top.geometry("{0}x{1}". \
        format(top.winfo_screenwidth(), top.winfo_screenheight()))
    top.update()

    Comic = ComicGUI(top)
    top.mainloop()

if __name__ == '__main__':
    main()
