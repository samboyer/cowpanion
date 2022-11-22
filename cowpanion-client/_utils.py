

import subprocess
import tkinter as tk

from typing import Tuple


def get_screen_coords_of_window(window)->Tuple[str, int,int]:
    geom = window.geometry().split('+')

    return geom[0], int(geom[1]), int(geom[2])


def create_tk_window(root) -> tk.Tk:
    root = tk.Toplevel(root)
    root.geometry("300x200")
    root.resizable(False, False)
    # Hide the root window drag bar and close button
    root.overrideredirect(True)
    # Make the root window always on top
    root.wm_attributes("-topmost", True)
    # Turn off the window shadow
    root.wm_attributes("-transparent", True)
    # Set the root window background color to a transparent color
    root.config(bg='systemTransparent')
    # hide from taskbar
    root.wm_attributes("-type", 'toolsip')
    return root

def run_cowsay(msg:str)->str:
    (retcode, stdout) = subprocess.getstatusoutput(f"cowsay \"{msg}\"")
    return stdout


from io import StringIO

from cowsay import read_dot_cow, cowsay

_cowfile_empty = read_dot_cow(StringIO("""
$the_cow = <<EOC;
         $thoughts
          $thoughts
EOC
"""))

def get_speech_bubble(msg:str)->str:
    return cowsay(msg, cowfile=_cowfile_empty)

