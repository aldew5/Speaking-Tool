import tkinter as tk
from PIL import Image
from PIL import ImageTk
import threading
import cv2
from cv2 import aruco
from frames import get_frames
from tkinter import scrolledtext
from markers import *
import keyboard


"""
Error with loading image
"""


cap = cv2.VideoCapture(0)

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

# store a dictionary of detected markers outside the main loop
# so we can store their values 
detected = {}

# inintialize the dictionary
for i in range(50):
    detected[i] = False

# keep lists of different markers
foods = {}
# keep track of whether or not an operation has been performed
# and set a timer between them
timeout = 0
updated = False

WINDOW = "main"

class Console():
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.cursor = '> '
        self.window = window
        self.widgets = []

        self.widgets.append(scrolledtext.ScrolledText(self.window,  
                                      wrap = tk.WORD,  
                                      width = 30,  
                                      height = 27,  
                                      font = ("Times New Roman", 
                                              15)))

        OPTIONS = ["Pizza", "Hotdog"]

        var = tk.StringVar(self.window)
        var.set(OPTIONS[0])

        w = tk.OptionMenu(self.window, var, *OPTIONS)
        
        start = tk.Button(self.window,
                    text="Confirm",
                    command=self.reset_window,
                    bg="green")
        
        self.widgets.append(w)
        self.widgets.append(start)


    def reset_window(self):
        for widget in self.widgets:
            widget.place_forget()
        self.display_menu("main")


    def get_text(self):
        a = self.textfield.get('1.0', 'end-1c')
        return a

    def get_input(self, text):
        self.textfield.delete('1.0', 'end')
        self.update(text)
        # must then wait for enter key to be pressed
        while True:
            if keyboard.is_pressed('enter'):
                break
            
        val = self.get_text()
        ind = len(text) + 1

        
        self.textfield.delete('1.0', 'end')
        #print("returning ", val[ind:], len(val[ind:]), "END")
        return val[ind:]

    def display_menu(self, op):
        if (op == "food"):
            self.widgets[1].place(relx=self.x, rely=self.y)

            self.widgets[2].place(relx=0.45, rely=0.5)
            self.widgets[0].place_forget()
        elif (op == "main"):
            self.widgets[0].place(relx=self.x, rely=self.y)

            
    

class Menu(tk.Frame):
    def __init__(self, window):
        self.window = window

    def show(self):
        title = tk.Label(self.window, text="ARCVision",
                         anchor="center",
                         font=("Times New Roman", 20))
        title.place(relx=0.35, rely=0.3)

        checked = tk.IntVar()
        box = tk.Checkbutton(self.window, text="Enable descriptors", variable=checked)
        box.place(relx=0.35, rely=0.4)

        start = tk.Button(self.window,
                          text="Start Application",
                          command=self.destroy,
                          bg="green")
        start.place(relx=0.35, rely=0.5)

    def destroy(self):
        self.window.destroy()
    
        


class App():
    def __init__(self, window, vs):
        self.window = window
        self.vs = vs
        self.frames = []
        self.thread = None
        self.stopEvent = None
        self.panel1 = None
        self.panel2 = None
        self.console = Console(0.6, 0.15, self.window)
        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()


    def show(self, menu):
        title = tk.Label(self.window, text="ARCVision",
                         anchor="center",
                         font=("Times New Roman", 20))
        title.place(relx=0.4, rely=0.05)
        subtitle = tk.Label(self.window, text="Commands",
                            font=("Time New Roman", 15))
        subtitle.place(relx=0.65, rely=0.1)

        if (menu == "food"):
            self.console.display_menu("food")
        else:
            self.console.display_menu("main")
        
        


    def videoLoop(self):

        try:
            while not self.stopEvent.is_set():
                self.frames = get_frames(self.vs, aruco_dict, parameters, detected,
                                         foods, timeout, updated, self.console)
                if (len(foods) > 0):
                    WINDOW = "food"
                    
                self.frames[0] = cv2.resize(self.frames[0], (300,300))
                self.frames[1] = cv2.resize(self.frames[1], (300,300))

                # swap the channels becuase openCV uses BGR whereas PIL
                # uses RGB
                image1 = cv2.cvtColor(self.frames[0], cv2.COLOR_BGR2RGB)
                image1 = Image.fromarray(image1)
                image1 = ImageTk.PhotoImage(image1)

                image2 = cv2.cvtColor(self.frames[1], cv2.COLOR_BGR2RGB)
                image2 = Image.fromarray(image2)
                image2 = ImageTk.PhotoImage(image2)

                if self.panel1 is None:
                    self.panel1 = tk.Label(image=image1)
                    self.panel1.image = image1
                    self.panel1.place(relx=0.05, rely=0.15)

                else:
                    self.panel1.configure(image=image1)
                    self.panel1.image = image1

                if self.panel2 is None:
                    self.panel2 = tk.Label(image=image2)
                    self.panel2.image = image2
                    self.panel2.place(relx=0.05, rely=0.55)
                else:
                    self.panel2.configure(image=image2)
                    self.panel2.image = image2

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

        


if (__name__ == "__main__"):
    window = tk.Tk()
    window.title("ARCVision")
    window.geometry("500x500")
    
    menu = Menu(window)
    menu.show()
    menu.window.mainloop()

    # new window
    window = tk.Tk()

    window.title("ARCVision")
    window.geometry("800x800")
    
    app = App(window, cap)
    
    app.show(WINDOW)
    app.window.mainloop()
    


