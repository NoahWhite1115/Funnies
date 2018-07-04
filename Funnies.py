#Funnies 0.00
#Written by Noah White
from Tkinter import *
import ComicLib

class ComicGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master

        self.widgets()

    def widgets(self):
        self.parent.title("Funnies: Python Webcomic Browser")

        #Set up the file menu
        menubar = Menu(self.parent)
        filemenu = Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Version", command = self.show_version)
        filemenu.add_command(label="Exit", command = self.parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.parent.config(menu=menubar)
        
        #main canvas element
        #self.canvasFrame = Frame(self.parent,bg="Black")

        screenwidth = self.parent.winfo_screenwidth()
        screenheight = self.parent.winfo_screenheight()
        self.canvas = Canvas(self.parent, width = screenwidth, height = screenheight, scrollregion=(0,0,screenwidth,2*screenheight), bg = "Black")

        #Add scrollbar
        canvasScroll= Scrollbar(self.parent, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.config(yscrollcommand = canvasScroll.set)
        canvasScroll.pack(side="right", fill="y")
        self.canvas.pack()

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
