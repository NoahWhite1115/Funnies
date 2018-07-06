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
        self.comic_images = []

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
        self.canvas = Canvas(self.parent, width = screenwidth, height = screenheight, scrollregion=(0,0,screenwidth,2*screenheight), bg = "White")

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

        self.refresh()

    #handles scrolling
    def mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1,"units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1,"units")

    #redraw the page
    def refresh(self):
        height = 0
        center = self.parent.winfo_screenwidth() / 2

        for comic in self.comics:
            #space for comic name
            self.canvas.create_text(center,height,text = comic.name, anchor = N)
            height += 15

            #load comic
            comic_image = Image.open("./Comics/" + comic.name + ".png")
            (comic_width,comic_height) = comic_image.size
            comic_image_obj = ImageTk.PhotoImage(comic_image)
            #needed to keep comic in scope after fn ends so garbage collection doesn't get it
            self.comic_images.append(comic_image_obj)
            #Draw comic
            self.canvas.create_image(center, height, image = comic_image_obj, anchor=N)
            height += comic_height

            #buttons
            #spacing on buttons
            next_spacing = 40
            prev_spacing = 40
        
            #random button
            if comic.rand_link == True:
                rand_button = Button(self.parent, text = "Rand", command = self.quit)
                rand_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
                self.canvas.create_window(center, height + 5, anchor=N, window=rand_button)
                
                #adjust spacing if random button exists
                next_spacing = 80
                prev_spacing = 80

            #next button
            next_button = Button(self.parent, text = "Next", command = self.quit)
            next_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
            self.canvas.create_window(center + next_spacing, height + 5, anchor=N, window=next_button)

            #previous button
            prev_button = Button(self.parent, text = "Prev", command = self.quit)
            prev_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
            self.canvas.create_window(center - prev_spacing, height + 5, anchor=N, window=prev_button)

            """
            #last button
            if comic.last == True:
                last_button = Button(self.parent, text = "Last", command = self.quit)
                last_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
                self.canvas.create_window(center + next_spacing + 40, height + 5, anchor=N, window=last_button)
 
            #first button
            if comic.first == True:
                first_button = Button(self.parent, text = "First", command = self.quit)
                first_button.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
                self.canvas.create_window(center - prev_spacing - 40, height + 5, anchor=N, window=first_button)
            """

            height += 40

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
