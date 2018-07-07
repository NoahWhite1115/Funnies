#Funnies 0.01
#Written by Noah White
from Tkinter import *
import ComicLib
from PIL import Image,ImageTk

class FunniesGUI(Frame):
    def __init__(self, master,comic_list):
        Frame.__init__(self, master)
        self.parent = master
        self.comics = comic_list
        self.comic_guis = []

        self.widgets()

    #Set up the main interface
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
        self.canvas = Canvas(self.parent, width = screenwidth, height = screenheight, bg = "White")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        #Add scrollbar
        canvasScroll= Scrollbar(self.parent, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.config(yscrollcommand = canvasScroll.set)
        canvasScroll.pack(side="right", fill="y")
        self.canvas.pack()

        #enable scrolling
        #Windows/Mac
        self.parent.bind_all("<MouseWheel>", self.mousewheel)
        #Linux
        self.parent.bind("<Button-4>", self.mousewheel)
        self.parent.bind("<Button-5>", self.mousewheel)

        self.set_up()

    #handles scrolling
    def mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1,"units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1,"units")

    #set up the page
    def set_up(self):
        height = 0
        center = self.parent.winfo_screenwidth() / 2

        for comic in self.comics:
            new_gui = ComicGui(comic,self.canvas,height,center,self.parent,self)
            height = new_gui.new_height
            self.comic_guis.append(new_gui)

        self.canvas.config(scrollregion=(0,0,center*2,height+35))

    def refresh(self):
        height = 0
        center = self.parent.winfo_screenwidth() / 2

        for comic_gui in self.comic_guis:
            comic_gui.refresh(height,center)
            height = comic_gui.new_height

        self.canvas.config(scrollregion=(0,0,center*2,height+35))

class ComicGui():
    def __init__(self,comic,canvas,height,center,parent,funnies):
        self.parent = parent
        self.comic = comic
        self.canvas = canvas
        self.funnies = funnies

        #space for comic name
        canvas.create_text(center,height,text = comic.name, anchor = N)
        height += 15

        #load comic
        self.comic_image = Image.open("./Comics/" + self.comic.name + ".png")
        (comic_width,comic_height) = self.comic_image.size
        self.comic_image_obj = ImageTk.PhotoImage(self.comic_image)
        #Draw comic
        canvas.create_image(center, height, image = self.comic_image_obj, anchor=N)
        height += comic_height

        #buttons
        #spacing on buttons
        next_spacing = 40
        prev_spacing = 40
    
        #random button
        if comic.rand_link == True:
            self.rand_button = Button(self.parent, text = "Rand", command = (lambda: self.comic.random()))
            self.rand_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
            self.rand_obj = canvas.create_window(center, height + 5, anchor=N, window=self.rand_button)
            
            #adjust spacing if random button exists
            next_spacing = 80
            prev_spacing = 80

        #next button
        self.next_button = Button(self.parent, text = "Next", command = (lambda : self.next()))
        self.next_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
        self.next_obj = canvas.create_window(center + next_spacing, height + 5, anchor=N, window=self.next_button)

        #previous button
        self.prev_button = Button(self.parent, text = "Prev", command = (lambda : self.prev()))
        self.prev_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
        self.prev_obj = canvas.create_window(center - prev_spacing, height + 5, anchor=N, window=self.prev_button)

        height += 45
        self.new_height = height

    def refresh(self,height,center):
        #space for comic name
        height += 15

        #load comic
        self.canvas.create_image(center, height, image = self.comic_image_obj, anchor=N)
        #get comic size
        (comic_width,comic_height) = self.comic_image.size

        height += comic_height

        next_spacing = 80
        prev_spacing = 80

        #move buttons
        if self.comic.rand_link == True:
            self.canvas.coords(self.rand_obj,(center,height+5))
            next_spacing = 80
            prev_spacing = 80

        self.canvas.coords(self.prev_obj,(center - prev_spacing,height+5))

        self.canvas.coords(self.next_obj,(center + next_spacing ,height+5))

        height += 45
        self.new_height = height

    def prev(self):
        self.comic.prev()
        self.comic.read()
        self.comic_image = Image.open("./Comics/" + self.comic.name + ".png")
        (comic_width,comic_height) = self.comic_image.size
        self.comic_image_obj = ImageTk.PhotoImage(self.comic_image)
        self.funnies.refresh()


    def next(self):
        self.comic.next()
        self.comic.read()
        self.comic_image = Image.open("./Comics/" + self.comic.name + ".png")
        (comic_width,comic_height) = self.comic_image.size
        self.comic_image_obj = ImageTk.PhotoImage(self.comic_image)
        self.funnies.refresh()


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

    Funnies = FunniesGUI(top, comic_list)
    top.mainloop()

if __name__ == '__main__':
    main()
