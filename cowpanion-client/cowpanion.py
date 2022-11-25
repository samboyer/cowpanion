
import tkinter as tk
from tkinter import ttk

from threading import Thread

from _cow import Cow
import _config, _utils, _ascii_cow


root = tk.Tk()
root.title("cowpanion")
root.withdraw()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


config = _config.load()

# NUM_COWS = 190
# for i in range(NUM_COWS):
#     cow = Cow(config['cows'][i%2], root)
#     Thread(target=cow.main_loop).start()
# root.mainloop()


for i in range(len(config['cows'])):
    cow = Cow(config['cows'][i], root)
    Thread(target=cow.main_loop).start()

root.mainloop()
