
import time
import _utils, _ascii_cow, _config
import tkinter as tk
import random

FRAME_RATE = 10
TALK_CHARS_PER_FRAME = 5
TALK_LINGER_SECS = 3
BLINK_PROBABILITY = 0.1
STATE_DURATION_SECS_MIN = 3.0
STATE_DURATION_SECS_MAX = 6.0
ANIM_FRAMES_PER_FRAME = 2


# @@@ adjust window size based on font size

# @@@ refactoring
# - make 'dragging' a state?
# - kill off self.cowstr
# - random messgae must't be the previous 3ish phrases

# states that the cow can move into.
# COW_STATES = ['idle', 'walk', 'lie', 'talk', 'talk_lie']

COW_STATE_TRANSITIONS = {
    'idle' : ['idle','walk','walk','lie','talk','eat_grass'],
    'walk' : ['idle'],
    'talk' : ['idle'],
    'eat_grass':['idle'],
    'lie'  : ['talk_lie', 'lie', 'idle', 'idle'],
    'talk_lie' : ['lie'],
}
# you can weight the transitions by duplicating the entries. this is cursed and i hate it

class Cow():
    pos_x = 0
    pos_y = 0

    is_being_dragged = False

    message_to_say = ""

    frames_until_next_state = 1
    state = 'idle'

    is_flipped = False


    def create_cow_window(self, root, cow_config):
        window = _utils.create_tk_window(root)
        window.title(cow_config['name'])

        COW_ART_WIDTH = 16
        COW_ART_HEIGHT = 5

        # declaring the speech canvas before the cow canvas so it doesn't draw over it:)
        self.tk_canvas_speech = tk.Canvas(
            window,
            bg='systemTransparent' if _utils.is_osx() else _utils.TK_WINDOWS_BG_COLOR,
            width=0,
            height=0,
            highlightthickness=0,
        )
        self.tk_text_id_speech = self.tk_canvas_speech.create_text(
            0,
            0,
            text='',
            font=(
                cow_config['fontFamily'],
                cow_config['fontSize'],
                cow_config['fontStyle'],
            ),
            fill=cow_config['color'],
            anchor=tk.NW,
        )
        self.tk_canvas_speech.place(anchor=tk.NW)

        # COW CANVAS
        canvas = tk.Canvas(
            window,
            bg='systemTransparent' if _utils.is_osx() else _utils.TK_WINDOWS_BG_COLOR,
            width=100,
            height=100,
            highlightthickness=0,
        )

        # window.config(highlightthickness=5)

        cowstr = _ascii_cow.base_cow

        self.tk_text_id_cow = canvas.create_text(
            0,
            0,
            text=_ascii_cow.apply_hat(cowstr, cow_config['hat']),
            font=(
                cow_config['fontFamily'],
                cow_config['fontSize'],
                cow_config['fontStyle'],
            ),
            fill=cow_config['color'],
            anchor=tk.NW,
        )


        # Set correct window height/width/initial position
        bounds = canvas.bbox(self.tk_text_id_cow)  # returns a tuple like (x1, y1, x2, y2)
        cow_width = bounds[2] - bounds[0]
        cow_height = bounds[3] - bounds[1]
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        RANDOM_INITIAL_POSITION = 100
        window.geometry("%dx%d+%d+%d" % (
            cow_width,
            cow_height,
            screen_width//2 + random.uniform(-RANDOM_INITIAL_POSITION, RANDOM_INITIAL_POSITION),
            screen_height//2 + random.uniform(-RANDOM_INITIAL_POSITION, RANDOM_INITIAL_POSITION)
        ))
        canvas.config(width=cow_width, height=cow_height)
        canvas.place(rely=1.0, relx=0.0, x=0, y=0, anchor=tk.SW)
        # print(cow_height, cow_width)


        coords = {}

        # see https://stackoverflow.com/a/50129744
        def click(e):
            # define start point for drag (in screen space to prevent stuttering)
            size, wx, wy = _utils.get_screen_coords_of_window(window)

            coords["sx"] = wx+e.x
            coords["sy"] = wy+e.y

        def drag(e):
            cx2 = e.x
            cy2 = e.y

            # Reset the the state, so when we let go we can choose a new state.
            self.is_being_dragged = True
            self.frames_until_next_state = 0
            self.state = 'idle'


            size, wx, wy = _utils.get_screen_coords_of_window(window)

            dx = wx+cx2-coords['sx']
            dy = wy+cy2-coords['sy']

            wx2 = wx+dx
            wy2 = wy+dy
            window.geometry(f"{size}+{wx2}+{wy2}")

            # update old vals to prevent stuttering
            coords['sx'] = wx+cx2
            coords['sy'] = wy+cy2

            # canvas.itemconfigure(text_id, text=cowstr.replace('oo','OO'))
            self.tk_canvas_speech.itemconfigure(self.tk_text_id_speech, text='')


        def release(e):
            self.is_being_dragged = False
            self.frames_until_next_state = 5
            self.resize_window()

            # canvas.itemconfigure(text_id, text=cowstr)


        window.bind("<ButtonPress-1>", click)
        window.bind("<B1-Motion>", drag)
        window.bind('<ButtonRelease-1>', release)


        self.tk_canvas = canvas
        self.cowstr = cowstr

        return window

    last_extra_y = 0

    def resize_window(self, min_width=0, extra_y=0):
        # bounds = self.tk_canvas.bbox(self.tk_text_id_cow)  # returns a tuple like (x1, y1, x2, y2)
        # print(bounds)
        cow_width = self.tk_canvas.winfo_reqwidth()
        cow_height =  self.tk_canvas.winfo_reqheight()

        # (also offset the window position by the bonus height so cow doesn't pop downwards)
        size, wx, wy = _utils.get_screen_coords_of_window(self.cow_window)
        if extra_y != 0:
            y_offset = -extra_y
        else:
            y_offset = self.last_extra_y

        cow_width = max(cow_width,min_width)

        self.cow_window.geometry("%dx%d+%d+%d" % (
            cow_width,
            cow_height+extra_y,
            wx,
            wy+ y_offset
        ))
        self.last_extra_y = extra_y

    def __init__(self, config, root, remote_message_to_say=""):

        self.config = config
        self.cow_window = self.create_cow_window(root, config)

        size, wx, wy = _utils.get_screen_coords_of_window(self.cow_window)
        self.pos_x = wx
        self.pos_y = wy



        if remote_message_to_say != "":
            self.message_to_say = remote_message_to_say
            self.state = 'talk'
        else:
            self.state = 'idle'
            self.frames_until_next_state = 1 * FRAME_RATE

    def main_loop(self):
        print(f"Cow {self.config['name']} is online")
        cw = self.cow_window.winfo_width()
        ch = self.cow_window.winfo_height()

        t0 = time.time()
        frame = 0
        talk_i = 0 #counter for speaking messages.
        message_finished = False

        while True:
            t1 = time.time()
            delta_time = t0 - t1
            size, wx, wy = _utils.get_screen_coords_of_window(self.cow_window)
            self.pos_x = wx
            self.pos_y = wy

            cowstr = self.cowstr


            if self.is_being_dragged:
                cowstr = _ascii_cow.surprised(cowstr)

            if self.state == 'idle':
                if random.random() < BLINK_PROBABILITY:
                    cowstr = _ascii_cow.blink(cowstr)

            elif self.state == 'walk':
                self.pos_x += delta_time*self.config['walkSpeed'] * (-1 if self.is_flipped else 1)

                self.pos_x = max(0, min(self.pos_x, self.cow_window.winfo_screenwidth()))

                self.cow_window.geometry('%s+%d+%d' % (size, self.pos_x, self.pos_y))

                cowstr = (_ascii_cow.walk(cowstr, (frame//ANIM_FRAMES_PER_FRAME) % 2)
                        if self.frames_until_next_state > 1
                        else cowstr)

            elif self.state == 'lie' or self.state == 'talk_lie':
                cowstr = _ascii_cow.base_cow_lying
            elif self.state == 'eat_grass':
                cowstr = _ascii_cow.base_cow_eat(frame//ANIM_FRAMES_PER_FRAME)

            if self.state == 'talk' or self.state =='talk_lie':
                talk_i += TALK_CHARS_PER_FRAME
                talk_i = min(talk_i, len(self.message_to_say))

                msg_truncated = self.message_to_say[:talk_i]

                talkstr = _utils.get_speech_bubble(msg_truncated)
                self.tk_canvas_speech.itemconfigure(self.tk_text_id_speech, text=talkstr)

                if talk_i == len(self.message_to_say) and not message_finished:
                    self.frames_until_next_state = TALK_LINGER_SECS * FRAME_RATE
                    message_finished = True # so as not to keep triggering the above line
                elif talk_i < len(self.message_to_say):
                    self.frames_until_next_state +=1 # so message gets to finish.

            if self.is_flipped:
                cowstr = _ascii_cow.flip(cowstr)
            self.tk_canvas.itemconfigure(
                self.tk_text_id_cow,
                text=_ascii_cow.apply_hat(cowstr, self.config['hat']))

            self.frames_until_next_state -=1
            if self.frames_until_next_state == 0 and not self.is_being_dragged:
                self.tk_canvas_speech.itemconfigure(self.tk_text_id_speech, text='')

                # Move to new state
                self.state = random.choice(COW_STATE_TRANSITIONS[self.state])
                self.frames_until_next_state = int(random.uniform(
                    STATE_DURATION_SECS_MIN,
                    STATE_DURATION_SECS_MAX
                ) * FRAME_RATE)

                if self.state == 'walk' and random.random() < 0.5:
                    self.is_flipped = not self.is_flipped

                if self.state == 'talk' or self.state == 'talk_lie':
                    self.message_to_say = random.choice(_config.quotes)
                    print(self.message_to_say)
                    talk_i = 0
                    message_finished = False
                    # @@@ ensure random messgae isn't one of the previous 3ish phrases

                    # work out the correct new window size by testing the whole message, then removing it.
                    talkstr = _utils.get_speech_bubble(self.message_to_say)
                    self.tk_canvas_speech.itemconfigure(self.tk_text_id_speech, text=talkstr)
                    bounds = self.tk_canvas_speech.bbox(self.tk_text_id_speech)
                    msg_width = bounds[2] - bounds[0]
                    msg_height = bounds[3] - bounds[1]
                    self.tk_canvas_speech.config(width=msg_width,height=msg_height)
                    self.resize_window(
                        min_width = msg_width + 50,  #extra x padding is because some of the truncated messages actually have longer speecy bubbles than the originals
                        extra_y = msg_height
                    )
                    self.tk_canvas_speech.itemconfigure(self.tk_text_id_speech, text='')
                else:
                    self.resize_window()
                # print(f"Moving to state {self.state} for {self.frames_until_next_state} frames")

            t0 = t1
            time.sleep(1/FRAME_RATE)
            frame+=1
