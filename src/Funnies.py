"""
Funnies 1.1
Written by Noah White

Python webcomic browser

Formatting follows PEP 8.0
https://www.python.org/dev/peps/pep-0008/

Uses the GNU GPL 2.0 Lisence.
Check LISENCE for more info.
"""
from Tkinter import *
import ComicLib
from PIL import Image, ImageTk
from os.path import join
from os.path import exists
from os import makedirs

# A bunch of configuration constants.
# Feel free to change to personalize.

# Fonts used
name_font = ("Verdana", 22)
title_font = ("Verdana", 10)

# Paths used
config_path = None
comic_path = None

# Colors used
canvas_bg = "White"
active_bg = "#33B5E5"

# Scroll speed
scroll_speed = 1

"""
FunniesGUI(master,comic_list)
Takes:
    master: the tk frame it belongs to
    comic_list: a list of comic objects, to dislay
This object serves as the wrapper that holds all the indivual comicGUIs
"""


class FunniesGUI(Frame):
    def __init__(self, master, comic_list):
        Frame.__init__(self, master)
        self.parent = master
        self.comics = comic_list
        self.comic_guis = []

        self.widgets()
        self.set_up()

    """
    FunniesGUI.widgets()
    takes: none
    Sets up the main interface
    Private
    """
    def widgets(self):
        self.parent.title("Funnies: Python Webcomic Browser")

        # Set up the file menu
        menubar = Menu(self.parent)
        filemenu = Menu(
            menubar,
            tearoff=0,
            relief=FLAT,
            activebackground=active_bg
            )
        filemenu.add_command(label="Version", command=self.show_version)
        filemenu.add_command(label="Exit", command=self.parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.parent.config(menu=menubar)

        # Main canvas element
        screenwidth = self.parent.winfo_screenwidth()
        screenheight = self.parent.winfo_screenheight()
        self.canvas = Canvas(
            self.parent,
            width=screenwidth,
            height=screenheight,
            bg=canvas_bg
            )
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        # Add scrollbar
        canvasScroll = Scrollbar(
            self.parent,
            orient=VERTICAL,
            command=self.canvas.yview
            )
        self.canvas.config(yscrollcommand=canvasScroll.set)
        canvasScroll.pack(side="right", fill="y")
        self.canvas.pack()

        # Enable scrolling
        # Windows/Mac
        self.parent.bind_all("<MouseWheel>", self.mousewheel)
        # Linux
        self.parent.bind("<Button-4>", self.mousewheel)
        self.parent.bind("<Button-5>", self.mousewheel)

    """
    FunniesGUI.mousewheel(event)
    takes:
        event: a mouse scroll event
    Handles scrolling
    Private
    """
    def mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(scroll_speed, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-scroll_speed, "units")

    """
    FunniesGUI.set_up()
    takes: none
    Sets up the ComicGui objects
    Private
    """
    def set_up(self):

        # Generate comic objects
        index = 0
        for comic in self.comics:
            # Don't load if an error has occurred
            if not comic.error:
                new_gui = ComicGui(
                    comic,
                    self.canvas,
                    self.parent,
                    self,
                    index
                    )
                self.comic_guis.append(new_gui)
                index += 1

        # Refresh from 0 to load whole page
        self.refresh(0)
    """
    FunniesGUI.refresh(index)
    takes:
        index: the index to begin at
    Redraws all the page elements at and below index
    Public
    """
    def refresh(self, index):
        height = 0
        center = self.parent.winfo_screenwidth() / 2

        for comic_gui in self.comic_guis:
            comic_gui.clear_gui()
            comic_gui.draw_gui(height, center)
            height = comic_gui.new_height

        self.canvas.config(scrollregion=(0, 0, center*2, height+35))

    """
    FunniesGUI.show_version()
    takes: none
    Displays Funnies version/author information
    Private
    """
    def show_version(self):
        window = Toplevel(self.parent)
        version_info = Label(
            window,
            width=30,
            height=5,
            anchor=CENTER,
            text="Funnies!\n"
            + "Version 1.1\n"
            + "Authored By Noah White\n"
            + "Liscenced under GNU-GLP 2.0\n"
            + "See Liscence file for details"
            )
        version_info.pack()


"""
ComicGUI(comic,canvas,parent,funnies,index)
takes:
    comic: the comic object that this will be interacting with
    canvas: The canvas element in FunniesGUI
    parent: the tk instance hosting all of this
    funnies: the FunniesGUI object managing this
    index: where this falls on the page
Displays a comic and the buttons needed to interact with it
"""


class ComicGui():
    def __init__(self, comic, canvas, parent, funnies, index):
        self.parent = parent
        self.comic = comic
        self.parent_canvas = canvas
        self.funnies = funnies
        self.index = index

        self.name_text = None
        self.drawn_image = None
        self.title_text = None
        self.drawn_add_image = None

        # Load comic
        self.comic_image = Image.open(join(
            self.comic.path,
            self.comic.name + ".png"
            ))
        self.comic_image_obj = ImageTk.PhotoImage(self.comic_image)

        if comic.add_image:
            # Load comic
            self.add_image = Image.open(join(
                self.comic.path,
                self.comic.name + "_ai.png"
                ))
            self.add_image_obj = ImageTk.PhotoImage(self.add_image)

        # Initialize buttons
        # Random button
        if comic.rand_link:
            self.rand_button = Button(
                    self.parent,
                    text="Rand",
                    command=(lambda: self.load("rand")))
            self.rand_button.configure(
                    width=5,
                    activebackground=active_bg,
                    relief=FLAT
                    )
            self.rand_obj = self.parent_canvas.create_window(
                0,
                0,
                anchor=N,
                window=self.rand_button
                )

        # Next button
        self.next_button = Button(
                self.parent,
                text="Next",
                command=(lambda: self.load("next"))
                )
        self.next_button.configure(
                width=5,
                activebackground=active_bg,
                relief=FLAT
                )
        self.next_obj = self.parent_canvas.create_window(
            0,
            0,
            anchor=N,
            window=self.next_button
            )

        # Previous button
        self.prev_button = Button(
                self.parent,
                text="Prev",
                command=(lambda: self.load("prev"))
                )
        self.prev_button.configure(
                width=5,
                activebackground=active_bg,
                relief=FLAT
                )
        self.prev_obj = self.parent_canvas.create_window(
            0,
            0,
            anchor=N,
            window=self.prev_button
            )

        # Max button
        if comic.max_link:
            self.max_button = Button(
                self.parent,
                text="Max",
                command=(lambda: self.load("max"))
                )
            self.max_button.configure(
                width=5,
                activebackground=active_bg,
                relief=FLAT
                )
            self.max_obj = self.parent_canvas.create_window(
                0,
                0,
                anchor=N,
                window=self.max_button
                )

        # Min button
        if comic.min_link:
            self.min_button = Button(
                self.parent,
                text="Min",
                command=(lambda: self.load("min"))
                )
            self.min_button.configure(
                width=5,
                activebackground=active_bg,
                relief=FLAT
                )
            self.min_obj = self.parent_canvas.create_window(
                0,
                0,
                anchor=N,
                window=self.min_button
                )

    """
    ComicGUI.clear_gui()
    takes: none
    Clears the GUI for the user
    Public
    """
    def clear_gui(self):
        self.parent_canvas.delete(self.name_text)
        self.parent_canvas.delete(self.drawn_image)
        self.parent_canvas.delete(self.title_text)
        self.parent_canvas.delete(self.drawn_add_image)

    """
    ComicGUI.draw_gui(height,center)
    Takes:
        height: the starting height for where to draw the comic
        center: the center line to draw around
    Draws the comic and buttons
    Public
    """
    # Draw the gui
    def draw_gui(self, height, center):

        # Space for comic name
        self.name_text = self.parent_canvas.create_text(
            center,
            height,
            text=self.comic.name,
            font=name_font,
            anchor=N
            )
        height += int(name_font[1] * 1.5)

        # Draw the new comic
        self.drawn_image = self.parent_canvas.create_image(
            center,
            height,
            image=self.comic_image_obj,
            anchor=N
            )

        # Get comic size and adjust for height
        (comic_width, comic_height) = self.comic_image.size
        height += comic_height

        # Load additional image
        if self.comic.add_image:
            self.drawn_add_image = self.parent_canvas.create_image(
                center,
                height,
                image=self.add_image_obj,
                anchor=N
                )

            # Get additional image size and adjust for height
            (add_width, add_height) = self.add_image.size
            height += add_height

        if self.comic.title:

            # Space for comic name

            self.title_text = self.parent_canvas.create_text(
                center,
                height,
                text=self.comic.title_text,
                font=title_font, anchor=N,
                width=center * 1.8,
                justify=CENTER
                )

            width_by_char = int(center*1.8/(title_font[1]/1.5))
            lines = int(len(self.comic.title_text) / width_by_char)
            if int(len(self.comic.title_text) % width_by_char) > 0:
                lines += 1
            height += lines * int(title_font[1] * 1.5)

        next_spacing = 40
        prev_spacing = 40

        # Move buttons
        if self.comic.rand_link:
            self.parent_canvas.coords(self.rand_obj, (center, height+5))
            next_spacing = 80
            prev_spacing = 80

        self.parent_canvas.coords(
            self.prev_obj,
            (center - prev_spacing, height+5)
            )
        self.parent_canvas.coords(
            self.next_obj,
            (center + next_spacing, height+5)
            )

        if self.comic.max_link:
            self.parent_canvas.coords(
                self.max_obj,
                (center + prev_spacing + 80, height+5)
                )
        if self.comic.min_link:
            self.parent_canvas.coords(
                self.min_obj,
                (center - next_spacing - 80, height+5)
                )

        height += 45
        self.new_height = height

    """
        ComicGUI.load(arg)
        takes:
            arg: what this function should do to the comic object
        Performs an action on the comic object
        Then loads from the file into memory.
        Public
    """
    # The load function for the ComicGUI class
    # get the previous, next or random comic
    # and load it into memory from the file
    def load(self, arg):
        if arg == "prev":
            self.comic.prev()
        elif arg == "next":
            self.comic.next()
        elif arg == "rand":
            self.comic.random()
        elif arg == "max":
            self.comic.max()
        elif arg == "min":
            self.comic.min()

        self.comic.read()
        self.comic_image = Image.open(join(
            self.comic.path,
            self.comic.name + ".png"
            ))
        self.comic_image_obj = ImageTk.PhotoImage(self.comic_image)

        if self.comic.add_image:
            self.add_image = Image.open(join(
                self.comic.path,
                self.comic.name + "_ai.png"
                ))
            self.add_image_obj = ImageTk.PhotoImage(self.add_image)

        # Refresh the page so that the changes are loaded.
        self.funnies.refresh(self.index)


"""
The main application.
Launches funnies by making the comic directory,
reading the config file,
and then creating the window.
"""


def main():

    # Create the new directory.
    if comic_path is not None:
        if not exists(join(comic_path, "Comics")):
            makedirs(join(comic_path, "Comics"))
    else:
        if not exists(join(".", "Comics")):
            makedirs(join(".", "Comics"))

    # Read/split config file as a list of 3-tuples (Name,URL,info_string).
    config_list = ComicLib.read_config()

    # Create a list holding all the comic objects
    comic_list = []

    for comic in config_list:
        x = ComicLib.ComicObj(comic[0], comic[1], comic[2], comic[3])
        comic_list.append(x)
        x.read()

    top = Tk()
    top.geometry("{0}x{1}".format(
        top.winfo_screenwidth(),
        top.winfo_screenheight()
        ))
    top.update()

    Funnies = FunniesGUI(top, comic_list)
    top.mainloop()


if __name__ == '__main__':
    main()
