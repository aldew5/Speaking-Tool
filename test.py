import tkinter as tk
from PIL import Image
from PIL import ImageTk

root = tk.Tk()
img = ImageTk.PhotoImage(Image.open("_data/pizza.jpg"))
panel = tk.Label(root, image = img)
panel.place(relx=0.5, rely=0.5)
root.mainloop()
