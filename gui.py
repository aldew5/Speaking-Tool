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

#images
pizza = Image.open("_data/pizza.jpg")
pizza = pizza.resize((200, 200), Image.ANTIALIAS)
#pizza = ImageTk.PhotoImage(pizza)

hotdog = Image.open("_data/hotdog.jpg")
hotdog = hotdog.resize((200, 200), Image.ANTIALIAS)
#hotdog = ImageTk.PhotoImage(hotdog)

images = {}
images["Hotdog"] = hotdog
images["Pizza"] = pizza

class Console():
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.window = window
        self.widgets = []
        self.pressed = False
        self.display = "console"

        self.widgets.append(scrolledtext.ScrolledText(self.window,  
                                      wrap = tk.WORD,  
                                      width = 30,  
                                      height = 27,  
                                      font = ("Times New Roman", 
                                              15)))

        OPTIONS = ["Pizza", "Hotdog"]

        self.food_var = tk.StringVar(self.window)
        self.food_var.set(OPTIONS[0])

        w = tk.OptionMenu(self.window, self.food_var, *OPTIONS)
        w.config(width=40)
        
        start = tk.Button(self.window,
                    text="Confirm Selection",
                    command=self.reset_window,
                    bg="green")
        
        self.widgets.append(w)
        self.widgets.append(start)
        self.widgets.append(None)


    def reset_window(self):
        for widget in self.widgets:
            widget.place_forget()
            
        self.pressed = True
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

            self.widgets[2].place(relx=0.68, rely=0.6)
            self.widgets[0].place_forget()
            self.display = "food"
            
        elif (op == "main"):
            self.widgets[0].place(relx=self.x, rely=self.y)
            self.display = "console"
            
    

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
    def __init__(self, window, vs, menu, images):
        self.window = window
        self.vs = vs
        self.images = images
        self.frames = [0, 0]
        self.thread = None
        self.stopEvent = None
        self.panel1 = None
        self.panel2 = None
        self.console = Console(0.6, 0.15, self.window)
        self.markers = []
        self.image = ""
        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        


    def show(self):
        title = tk.Label(self.window, text="ARCVision",
                         anchor="center",
                         font=("Times New Roman", 20))
        title.place(relx=0.4, rely=0.05)
        subtitle = tk.Label(self.window, text="Commands",
                            font=("Time New Roman", 15))
        subtitle.place(relx=0.65, rely=0.1)

        if (self.console.display == "food"):
            self.console.display_menu("food")
        else:
            self.console.display_menu("main")


    def videoLoop(self):

        try:
            while not self.stopEvent.is_set():
                self.frames[0], self.frames[1], self.markers = get_frames(self.vs, aruco_dict, parameters, detected,
                                         foods, timeout, updated, self.console)

                if (self.console.pressed and len(self.markers)):
                    self.markers[-1].type = self.console.food_var.get()
        
                for marker in self.markers:
                    if (type(marker) is Food):
                        marker.type = self.console.food_var.get()
                    #print("HERE")
                    marker.display()
                    

            
                if (self.console.display == "food"):
                    # init the image
                                                
                    if (self.console.food_var.get() != self.image):
                        self.image = self.console.food_var.get()
                        
                    img = ImageTk.PhotoImage(self.images[self.image])

                    if (self.console.widgets[3] == None):
                        self.console.widgets[3] = tk.Label(self.window, image=img)
                        self.console.widgets[3].place(relx=0.63, rely=0.25)

                    else:
                        self.console.widgets[3].configure(image=img)
                                         
                        
                    
                    
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
    
    app = App(window, cap, "main", images)
    
    app.show()
    app.window.mainloop()
    


