import json
import subprocess
import os
import tkinter as tk
from tkinter import ttk

from threading import Thread

str = """
 ______
| hello |
  =====
   \\
    \\
      ^🎩^
      (oo)\_______
      (__)\       )\/\\
          ||----w |
          ||     ||
"""

hats = ['^__^', '{__}', '}__{', '^🎩^', '^🦆^']


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


def create_cow_window(root, cow_config):
    window = create_tk_window(root)
    window.title(cow_config['name'])
    canvas = tk.Canvas(
        window,
        bg='systemTransparent',
        width=300,
        height=300,
        highlightthickness=0,
    )

    cowstr = make_cow_hat(run_cowsay('.'), cow_config['hat'])

    text_id = canvas.create_text(
        16,
        16,
        text=cowstr,
        font=(
            cow_config['font_family'],
            cow_config['font_size'],
            cow_config['font_style'],
        ),
        fill=cow_config['color'],
        anchor=tk.NW,
    )
    canvas.pack()

    coords = {}

    # see https://stackoverflow.com/a/50129744
    def click(e):
        # define start point for drag (in screen space to prevent stuttering)
        geom = window.geometry().split('+')
        wx = int(geom[1])
        wy = int(geom[2])
        coords["sx"] = wx+e.x
        coords["sy"] = wy+e.y

    def drag(e):
        cx2 = e.x
        cy2 = e.y

        geom = window.geometry().split('+')
        wx = int(geom[1])
        wy = int(geom[2])

        dx = wx+cx2-coords['sx']
        dy = wy+cy2-coords['sy']

        wx2 = wx+dx
        wy2 = wy+dy
        window.geometry(f"{geom[0]}+{wx2}+{wy2}")

        # update old vals to prevent stuttering
        coords['sx'] = wx+cx2
        coords['sy'] = wy+cy2

        canvas.itemconfigure(text_id, text=cowstr.replace('oo','OO'))

    def release(e):
        canvas.itemconfigure(text_id, text=cowstr)


    canvas.bind("<ButtonPress-1>", click)
    canvas.bind("<B1-Motion>", drag)
    canvas.bind('<ButtonRelease-1>', release)

    return window


def make_cow_blink(cowstr):
    return cowstr.replace('o', '_')


def make_cow_walk(cowstr: str, frame: int) -> str:
    subst = '|\\     \\|' if frame == 0 else '\\|     |\\'
    return cowstr.replace('||     ||', subst, 1)


def make_cow_hat(cowstr, hatstr) -> str:
    return hatstr.join(cowstr.rsplit('^__^', 1))


def run_cowsay(msg):
    (retcode, stdout) = subprocess.getstatusoutput(f"cowsay \"{msg}\"")
    return stdout


def flip_cow(cowstr: str) -> str:
    def flip_line(s):
        x = list(s)
        x.reverse()
        s = ''.join(x)
        s = s.replace('/', '\x01').replace('\\', '/').replace('\x01', '\\')
        s = s.replace('(', '\x01').replace(')', '(').replace('\x01', ')')
        return s

    # add trailing spaces to all lines
    lines = cowstr.splitlines()
    longest_len = max(map(len, lines))
    pad = ' ' * longest_len
    lines = map(lambda l: (l + pad)[:longest_len], lines)

    return '\n'.join(map(flip_line, lines))


def pad(cowstr: str, amount: int) -> str:
    pad = ' ' * amount
    return pad + cowstr.replace('\n', '\n' + pad)


import time


def anim_test_speak(flip=False):
    msg = (
        "hello world this is a long message idk how it will look. hello world this is a long message idk how it will look. hello world this is a long message idk how it will look."
        "hello world this is a long message idk how it will look. hello world this is a long message idk how it will look. hello world this is a long message idk how it will look."
        "hello world this is a long message idk how it will look. hello world this is a long message idk how it will look. hello world this is a long message idk how it will look."
    )
    step = 5

    frame_time = 1 / 60

    for i in range(1, len(msg), step):
        msg_truncated = msg[:i]
        cowstr = run_cowsay(msg_truncated)
        if i % 150 <= 25:
            cowstr = make_cow_blink(cowstr)
        if flip:
            cowstr = flip_cow(cowstr)
        print(cowstr)

        time.sleep(frame_time)

    c = run_cowsay(msg)
    if flip:
        c = flip_cow(c)
    print(c)
    time.sleep(1)


def anim_test_walk():
    frame_time = 1 / 5

    for frame in range(10):
        cowstr = run_cowsay('.')
        cowstr = make_cow_walk(cowstr, frame % 2)
        cowstr = flip_cow(cowstr)
        cowstr = pad(cowstr, frame)
        print(cowstr)
        time.sleep(frame_time)

    print(pad(flip_cow(run_cowsay('.')), 10))
    time.sleep(frame_time * 5)

    for frame in range(10):
        cowstr = run_cowsay('.')
        cowstr = make_cow_walk(cowstr, frame % 2)
        cowstr = pad(cowstr, 10 - frame)
        print(cowstr)
        time.sleep(frame_time)

    print(run_cowsay('.'))
    time.sleep(frame_time * 3)


CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.cowpanion_profile')


def load_config():
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            config = json.load(f)
    # @@@ augment config with default values if missing
    return config


def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)


root = tk.Tk()
root.title("cowpanion")
root.withdraw()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


config = load_config()

for cow in config['cows']:
    cow_window = create_cow_window(root, cow)

    cw = cow_window.winfo_width()
    ch = cow_window.winfo_height()

    cow_window.geometry('%dx%d+%d+%d' % (cw, ch, screen_width//2-cw//2, screen_height//2-ch//2))

root.mainloop()
