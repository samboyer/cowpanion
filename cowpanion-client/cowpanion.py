
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


for i in range(len(config['cows'])):
    cow_config = config['cows'][i]

    # cw = cow_window.winfo_width()
    # ch = cow_window.winfo_height()
    # cow_window.geometry('%dx%d+%d+%d' % (cw, ch, screen_width//2-cw//2, screen_height//2-ch//2))

    cow = Cow(cow_config, root)

    Thread(target=cow.main_loop).start()


root.mainloop()

# anim_test_speak()
anim_test_walk()