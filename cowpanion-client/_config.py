
import os
import json
import random

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.cowpanion_profile')


config = {}

hats = """\
^__^
{__}
}__{
^🎩^
^🧢^
^👒^
^🪖^
^🎓^
^⛑^
^🐄^
^🇫🇷^
^🇮🇹^
^🇪🇸^
^🇮🇪^
^🏳️‍🌈^
^🏴‍☠️^
^🦆^
^🛹^
^☕️^
^🍄^
^🔥^
^🚨^
^⚽️^
""".splitlines()



def load():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        # @@@ augment config with default values if missing
    else:
        username = os.environ.get("USER")
        if not username:
            username = os.environ.get("USERNAME")
        if not username:
            username = 'User'

        config = {
            "cows": [
                {
                    "name": f"{username}'s cow",
                    "color": "#000000", # @@@ random color!
                    "hat": random.choice(hats),
                    "fontFamily": "Cascadia Code",
                    "fontSize": 14,
                    "fontStyle": "",
                    "walkSpeed": 30
                },
            ],
            "settings": {}
        }
        save(config)
    return config

def save(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)


quotes = """\
moo
moooooooooo
moooooooooooooooooooooooooooo
i'm hungry
you can do it!
i am a cow.

why do cows have hooves instead of feet? because they lactose.
what do you call the greatest milk ever produced? legendairy.
sweet dreams are made of cheese, who am I to diss a brie?
where do you find a cow with no legs? wherever you left it.
why did the cow cross the road? to get to the udder side.

i think, therefore i am.
muddy water is best cleared by leaving it alone.
the most common way people give up their power is by thinking they don’t have any.
life shrinks or expands in proportion to one’s courage.
perfection is achieved not when there is nothing more to add, but when there is nothing left to take away.
happiness does not consist in pastimes and amusements, but in virtuous activities.
never leave that till tomorrow which you can do today.
all that we are is the result of what we have thought.
the most powerful control we can ever attain, is to be in control of ourselves.
there is only one success-to be able to spend your life in your own way.
the superior man is modest in his speech, but exceeds in his actions.
whatever you think the world is withholding from you, you are withholding from the world.
learn from the mistakes of others. you can’t live long enough to make them all yourself.
good manners will often take people where neither money nor education will take them.
inaction will cause a man to sink into the slough of despond and vanish without a trace.
by constant self-discipline and self-control, you can develop greatness of character.
optimism is the faith that leads to achievement. nothing can be done without hope and confidence.
avoiding danger is no safer in the long run than outright exposure. the fearful are caught as often as the bold.
our truest life is when we are in dreams awake.
in character, in manner, in style, in all things, the supreme excellence is simplicity.
rule your mind, or it will rule you.
no matter how big a nation is, it is no stronger than its weakest people.
true freedom is impossible without a mind made free by discipline.
you create opportunities by performing, not complaining.
if you can't do great things, do small things in a great way.
idleness is only the refuge of weak minds, and the holiday of fools.
if you do not have courage, you may not have the opportunity to use any of your other virtues.
tomorrow is often the busiest day of the week.
at the end of the day, let there be no excuses, no explanations, no regrets.
if we don't discipline ourselves, the world will do it for us.
we are still masters of our fate. we are still captains of our souls.
do, or do not. there is no try.

may the force be with you.
there's no place like home.
i'm the king of the world!
carpe diem. seize the day, boys. make your lives extraordinary.
elementary, my dear watson.
it's alive! it's alive!!
my mama always said life was like a box of chocolates. you never know what you're gonna get.
i'll be back.
you're gonna need a bigger boat.
here's looking at you, kid.
my precious.
houston, we have a problem.
there's no crying in baseball!
e.t. phone home.
you can't handle the truth!
a martini. shaken, not stirred.
life is a banquet, and most poor suckers are starving to death!
if you build it, he will come.
the stuff that dreams are made of.
magic cow on the wall, who is the fairest one of all?
keep your friends close, but your enemies closer.
i am your father.
just keep swimming.
today, i consider myself the luckiest man on the face of the earth.
you is kind. you is smart. you is important.
hasta la vista, baby.
you don't understand! i coulda had class. i coulda been a contender. i could've been somebody, instead of a cow, which is what i am.
you talking to me?
roads? where we're going, we don't need roads.
that'll do, pig. that'll do.
i'm walking here! i'm walking here!
stella! hey, stella!
here's johnny!
inconceivable!
all right, mr. demille, i'm ready for my close-up.
fasten your seatbelts. it's going to be a bumpy night.
nobody puts baby in a corner.
well, nobody's perfect.
snap out of it!
you had me at 'moo.'
they may take our lives, but they'll never take our freedom!
you're killin' me, smalls.
toto, i've a feeling we're not in kansas anymore.

here come dat boi!!
*slaps roof of cow* this bad boy can fit so many phrases
to be fair, you have to have a very high iq to understand rick and morty. the humour is extremely subtle, and without a solid grasp of theoretical physics most of the jokes will go over a typical viewer's head.
according to all known laws of aviation, there is no way a bee should be able to fly. its wings are too small to get its fat little body off the ground. the bee, of course, flies anyway
wanna go skateboards?
i like trains.
i'm blue, da ba dee da ba dye, da ba dee da ba dye da ba dee da ba dye, da ba dee da ba dye da ba dee da ba dye, da ba dee da ba dye da ba dee da ba dye
if you ask rick astley for a copy of the movie “up”, he cannot give you it as he can never give you up. but, by doing that, he is letting you down, and thus, is creating something known as the astley paradox.
leeeeeeroyyyyy jjjjjennnnkinnnssssss!!!!!!

so you just gonna bring me a birthday gift on my birthday to my birthday party on my birthday with a birthday gift?
they ask you how you are, and you just have to say that you're fine, when you're not really fine, but you just can't get into it because they would never understand.
look at all those chickens!
it is wednesday, my dudes.
and they were roommates!
(oh my god, they were roommates...)
waiiiiiit a minute... who are you?
in the heat of battle he don't miss. in the heat of controversy he don't miss.
it's friday, friday; gotta get down on friday; everybody's lookin' forward to the weekend, weekend.
kickin' in the front seat. sittin' in the back seat. gotta make my mind up, which seat can i take?

""".splitlines()
quotes = list(filter(lambda s:s!='', quotes))

# quotes=[""]
