
def blink(cowstr:str)->str:
    return cowstr.replace('o', '-')


def walk(cowstr: str, frame: int) -> str:
    subst = '|\\     \\|' if frame == 0 else '\\|     |\\'
    return cowstr.replace('||     ||', subst, 1)


def apply_hat(cowstr:str, hatstr:str) -> str:
    return hatstr.join(cowstr.rsplit('^__^', 1))

def surprised(cowstr:str)->str:
    return cowstr.replace('oo','OO')


def flip(cowstr: str) -> str:
    def flip_line(s):
        x = list(s)
        x.reverse()
        s = ''.join(x)
        s = s.replace('/', '\x01').replace('\\', '/').replace('\x01', '\\')
        s = s.replace('(', '\x01').replace(')', '(').replace('\x01', ')')
        s = s.replace('<', '\x01').replace('>', '<').replace('\x01', '>')
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


base_cow = """\
^__^
(oo)\\_______
(__)\\       )\\/\\
    ||----w |
    ||     ||"""

base_cow_lying = """\
\n
^__^________
(uu)\\       )\\/\\
(__)<==---w<=="""


_cow_monch_frames = [
    """
     _______
^__^/       )\\/\\
(oo)||----w |
(__)||     ||""",
    """
     _______
^__^/       )\\/\\
(oo)||----w |
(mm)||     ||"""
]

def base_cow_eat(frame:int)->str:
    return _cow_monch_frames[frame % 2]
