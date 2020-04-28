import os
import requests
import random
from Phyme import Phyme

from flask import Flask, request, jsonify
CHANNEL_NAME = os.environ.get('LTR_CHANNEL_NAME')
API_TOKEN = os.environ.get('LTR_SLACK_API_TOKEN')
LOCAL_TOKEN = os.environ.get('LTR_LOCAL_TOKEN')
RHYME_AVOID_LIST = os.environ.get('LTR_AVOID_LIST').split(',') if 'LTR_AVOID_LIST' in os.environ else []
BOT_IGNORE_LIST = os.environ.get('BOT_IGNORE_LIST').split(',') if 'BOT_IGNORE_LIST' in os.environ else []

app = Flask(__name__)
ph = Phyme()

@app.route('/', methods=['POST', 'GET'])
def respond():
    # Retrieve the name from url parameter
    incoming_token = request.args.get("token", None)
    # Check if user sent a name at all
    if not incoming_token or incoming_token != LOCAL_TOKEN:
        raise Exception("local key error")

    channels = requests.post('https://slack.com/api/conversations.list', data={
        'token': API_TOKEN,
        'types': 'private_channel'
    }).json()['channels']

    for channel in channels:
        if channel['name'] == CHANNEL_NAME:
            channel_id = channel['id']

    members = requests.post('https://slack.com/api/conversations.members', data={
        'token': API_TOKEN,
        'channel': channel_id,
    }).json()['members']

    users = []
    for member in members:
        name = requests.post('https://slack.com/api/users.info', data={
            'token': API_TOKEN,
            'user': member,
        }).json()['user']['real_name']
        if name in BOT_IGNORE_LIST:
            continue
        users.append(name)

    random.shuffle(users)
    transform_roulette = random.randint(0, 3)
    users = [transformation_router(transform_roulette, user) for user in users]

    requests.post('https://slack.com/api/chat.postMessage', data={
        'token': API_TOKEN,
        'channel': CHANNEL_NAME,
        'text': ", ".join(users)
    })

    return "names calculated"


def get_random_rhyme(word):
    try:
        all_rhymes = ph.get_perfect_rhymes(word)
        rhymes = [r for s in all_rhymes for r in all_rhymes[s]]
        rhyme = random.choice(rhymes)
        tries = 0

        while (rhyme in RHYME_AVOID_LIST or rhyme.lower() == word.lower() or '(' in rhyme) and tries < 10:
            rhyme = random.choice(rhymes) or None
            tries += 1
        return rhyme
    except KeyError:
        return None

def nickname(name):
    mobster_nicknames = ["Joe Bananas", "Ice Pick Willie", "Johnny Sausage", "Baby Shanks", "Whack-Whack", "Tick–Tock",
                         "Quack Quack", "The Wizard of Odds", "Louie Bagels", "Tommy Sneakers", "Pat the Cat",
                         "Chee-Chee", "Tommy Karate", "Willie Potatoes", "Bootsie", "Jimmy Dumps", "One Armed Ronnie",
                         "The Toupee", "Chicken Man", "Socks", "Jimmy Nap", "Charley Wagons", "Joe the Builder",
                         "Benny Squint", "Mr. Bread", "Dopey Benny", "The Typewriter", "The Artichoke King",
                         "Shellackhead", "The Owl", "Louie Eggs", "The Clutch Hand", "14th Street Steve", "Corky",
                         "Flipper", "Legs DiCocco", "The Golfer", "The Reluctant Prince", "Georgie Neck", "Baldy Dom",
                         "Larry Fab", "George from Canada"]
    nick_prefix = ["Sweet", "Swift", "Slick", "The", "The Mad", "Stylin'", "Big", "The Big", "Big City",
                   "Big Slack Attack", "Beast Mode", "Master", "Steel", "Diamond-Tipped", "Iron", "Cousin", "T-Tops",
                   "T-Bone", "Hackmaster", "Monster", "Grandmaster", "M.C.", "Poker Face", "Gold Tooth", "Maserati",
                   "Fast Talkin'", "Glam", "The Animal", "Maddog"]
    name_parts = name.split()
    if len(name_parts) < 2:
        nick = get_random_rhyme(name) or random.choice(mobster_nicknames)
        return "{}– A.K.A. \"{} {}\"".format(name, random.choice(nick_prefix), nick).title()
    else:
        name_parts_for_nick = name_parts.copy()
        random.shuffle(name_parts_for_nick)
        nick = None
        for nick_base in name_parts_for_nick:
            nick = get_random_rhyme(nick_base)
            if nick:
                continue
        if not nick:
            nick = get_random_rhyme(name_parts[1])

        if not nick:
            nick = random.choice(mobster_nicknames)
        else:
            if random.randint(0, 10) > 4:
                nick = "{} {}".format(random.choice(nick_prefix), nick)
        return "{} \"{}\" {}".format(name_parts[0], nick, " ".join(name_parts[1:])).title()

def shift_vowels(name):
    vowels = ["a", "e", "i", "o", "u", "y"]
    output = ''
    for char in name.lower():
        if char in vowels:
            output += random.choice(vowels)
        else:
            output += char
    return output.title()

# def umlauted(name):
#     backwards = " ".join(name.lower()[::-1].split()[::-1])
#     vowels = {'a': 'ä', 'e': 'ë', 'i': 'ï', 'o': 'ö', 'u': 'ü', 'y': 'ÿ'}
#     output = ''
#     translate = True
#     for char in backwards:
#         if translate and char in vowels:
#             output += vowels[char]
#             translate = False
#         elif char == ' ':
#             output += ' '
#             translate = True
#         else:
#             output += char
#     return output.title()

def leet_speak(name):
    leet = {'a': ['4', '@', 'Д'],
    'b': ['8', 'ß'],
    'c': ['©', '¢'],
    'd': ['D'],
    'e': ['3', '€'],
    'f': ['pH'],
    'g': ['6',],
    'h': ['H'],
    'i': ['1', '|', '!'],
    'j': ['J',],
    'k': ['K',],
    'l': ['1'],
    'm': ['|\/|'],
    'n': ['И'],
    'o': ['0', 'Ø'],
    'p': ['p'],
    'q': ['kw', 'Q'],
    'r': ['Я', '®'],
    's': ['5', '$', '§'],
    't': ['7', '+'],
    'u': ['U'],
    'v': ['\/'],
    'w': ['\X/', 'Ш'],
    'x': ['Ж'],
    'y': ['¥', 'Ч'],
    'z': ['2']}
    output = ''
    for char in name.split()[0].lower():
        if char in leet:
            output += random.choice(leet[char])
        else:
            output += char
    return "-= {} =-".format(output)

def transformation_router(index, input):
    #transformations = [leet_speak, umlauted, shift_vowels, nickname]
    transformations = [leet_speak, shift_vowels, nickname]
    if index < len(transformations):
        return transformations[index](input)
    else:
        return(input.split()[0])

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)