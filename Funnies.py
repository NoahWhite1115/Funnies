#Funnies 0.10
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
        self.set_up()

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


    #handles scrolling
    def mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1,"units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1,"units")

    #set up the comic_guis
    def set_up(self):

        #generate comic objects
        index = 0
        for comic in self.comics:
            new_gui = ComicGui(comic,self.canvas,self.parent,self,index)
            self.comic_guis.append(new_gui)
            index += 1

        #refresh from 0 to load whole page
        self.refresh(0)

    #redraw all the page elements
    def refresh(self, index):
        height = 0
        center = self.parent.winfo_screenwidth() / 2

        for comic_gui in self.comic_guis:
            comic_gui.clear_gui()
            comic_gui.draw_gui(height,center)
            height = comic_gui.new_height

        self.canvas.config(scrollregion=(0,0,center*2,height+35))

class ComicGui():
    def __init__(self,comic,canvas,parent,funnies,index):
        self.parent = parent
        self.comic = comic
        self.parent_canvas = canvas
        self.funnies = funnies
        self.index = index

        self.name_text = None
        self.drawn_image = None
        self.title_text = None

        #load comic
        self.comic_image = Image.open("./Comics/" + self.comic.name + ".png")
        (comic_width,comic_height) = self.comic_image.size
        self.comic_image_obj = ImageTk.PhotoImage(self.comic_image)

        #initialize buttons
        #random button
        if comic.rand_link == True:
            self.rand_button = Button(self.parent, text = "Rand", command = (lambda: self.random()))
            self.rand_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
            self.rand_obj = self.parent_canvas.create_window(0, 0, anchor=N, window=self.rand_button)
            
        #next button
        self.next_button = Button(self.parent, text = "Next", command = (lambda : self.next()))
        self.next_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
        self.next_obj = self.parent_canvas.create_window(0, 0, anchor=N, window=self.next_button)

        #previous button
        self.prev_button = Button(self.parent, text = "Prev", command = (lambda : self.prev()))
        self.prev_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
        self.prev_obj = self.parent_canvas.create_window(0, 0, anchor=N, window=self.prev_button)

    #clear the gui
    def clear_gui(self):
        self.parent_canvas.delete(self.name_text)
        self.parent_canvas.delete(self.drawn_image)
        self.parent_canvas.delete(self.title_text)

    #draw the gui
    def draw_gui(self,height,center):
        
        #space for comic name
        self.name_text = self.parent_canvas.create_text(center,height,text = self.comic.name, font=name_font, anchor = N)
        height += int(name_font[1] * 1.5)

        #draw the new comic
        self.drawn_image = self.parent_canvas.create_image(center, height, image = self.comic_image_obj, anchor=N)

        #get comic size and adjust for height
        (comic_width,comic_height) = self.comic_image.size
        height += comic_height

        
        #space for comic name
        self.title_text = self.parent_canvas.create_text(center, height, text = self.comic.title_text, font=title_font, anchor = N, width = center * 1.8, justify = CENTER)
        width_by_char = int(center*1.8/(title_font[1]/1.5))
        lines = int(len(self.comic.title_text) / width_by_char)
        if int(len(self.comic.title_text) % width_by_char) > 0:
            lines += 1
        height += lines * int(title_font[1] * 1.5)
        
        next_spacing = 40
        prev_spacing = 40

        #move buttons
        if self.comic.rand_link == True:
            self.parent_canvas.coords(self.rand_obj,(center,height+5))
            next_spacing = 80
            prev_spacing = 80

        self.parent_canvas.coords(self.prev_obj,(center - prev_spacing,height+5))
        self.parent_canvas.coords(self.next_obj,(center + next_spacing ,height+5))

        height += 45
        self.new_height = height

    #The prev function for the ComicGUI class
    #get the prev comic and load it into memory from the file
    def prev(self):
        self.comic.prev()
        self.comic.read()
        self.comic_image = Image.open("./Comics/" + self.comic.name + ".png")
        self.comic_image_obj = ImageTk.PhotoImage(self.comic_image)
        #refresh the page so that the changes are loaded.
        self.funnies.refresh(self.index)

    #The next function for the ComicGUI class
    #get the next comic and load it into memory from the file
    def next(self):
        self.comic.next()
        self.comic.read()
        self.comic_image = Image.open("./Comics/" + self.comic.name + ".png")
        self.comic_image_obj = ImageTk.PhotoImage(self.comic_image)
        #refresh the page so that the changes are loaded.
        self.funnies.refresh(self.index)

    #The next function for the ComicGUI class
    #get the next comic and load it into memory from the file
    def random(self):
        self.comic.random()
        self.comic.read()
        self.comic_image = Image.open("./Comics/" + self.comic.name + ".png")
        self.comic_image_obj = ImageTk.PhotoImage(self.comic_image)
        #refresh the page so that the changes are loaded.
        self.funnies.refresh(self.index)

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
    name_font = ("Verdana",22)
    title_font = ("Verdana",10)
    main()
