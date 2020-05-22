import os
import requests
import random
from Phyme import Phyme

from flask import Flask, request, jsonify
API_TOKEN = os.environ.get('LTR_SLACK_API_TOKEN')
LOCAL_TOKEN = os.environ.get('LTR_LOCAL_TOKEN')
RHYME_AVOID_LIST = os.environ.get('LTR_AVOID_LIST').split(',') if 'LTR_AVOID_LIST' in os.environ else []
BOT_IGNORE_LIST = os.environ.get('BOT_IGNORE_LIST').split(',') if 'BOT_IGNORE_LIST' in os.environ else []

app = Flask(__name__)
ph = Phyme()

@app.route('/', methods=['POST'])
def respond():
    """
        token = gIkuvaNzQIHg97ATvDxqgjtO
        & team_id = T0001
        & team_domain = example
        & enterprise_id = E0001
        & enterprise_name = Globular % 20
        Construct % 20
        Inc
        & channel_id = C2147483705
        & channel_name = test
        & user_id = U2147483697
        & user_name = Steve
        & command = / weather
        & text = 94070
    """
    channel_id = request.form['channel_id']
    command = request.form['command']
    text = request.form['text'].lower() if 'text' in request.form else 'random'
    if 'help' in text:
        return jsonify({
            "response_type": "in_channel",
            "text": "usage",
            "attachments": [
                {"text": "{0} executed without arguments will present the scrum order, and with a 60% probability of " 
                         "applying a randomly chosen text transformation.".format(command)},
                {"text": "{0} (normal | 1337 | shifted | nicknames | jargon | random)".format(command)},
                {"text": "{0} help (displays this message)".format(command)},
            ]
        })

    incoming_token = request.args.get("token", None)
    if not incoming_token or incoming_token != LOCAL_TOKEN:
        raise Exception("local key error")

    members_list = requests.post('https://slack.com/api/conversations.members', data={
        'token': API_TOKEN,
        'channel': channel_id,
    }).json()

    if not members_list['ok']:
        return "This is probably a private channel that I'm not invited to. Invite me if you want me to work here."

    users = []
    for member in members_list['members']:
        name = requests.post('https://slack.com/api/users.info', data={
            'token': API_TOKEN,
            'user': member,
        }).json()
        if name['user']['real_name'] in BOT_IGNORE_LIST or not name['ok']:
            continue
        users.append(name['user']['real_name'])

    random.shuffle(users)

    if not text or 'random' in text or text == '':
        # rather than just randomly selecting between the transformations, let make it only half-likely you'll get a
        # transformation to make it feel more special
        transform_roulette = random.randint(0, 2)
        users = [transformation_router(transform_roulette, user) for user in users]
    elif '1337' in text:
        users = [leet_speak(user) for user in users]
    elif 'shifted' in text:
        users = [shift_vowels(user) for user in users]
    elif 'nicknames' in text:
        users = [nickname(user) for user in users]
    elif 'jargon' in text:
        users = [jargon(user) for user in users]

    response = {
        "response_type": "in_channel",
        "text": "Scrum Order: ",
        "attachments":
            [{"text": "{}: {}".format(k + 1, v)} for k, v in enumerate(users)]
    }

    return jsonify(response)


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
                         "Larry Fab", "George from Canada", "Master of Disaster", "Dr. Doom", "Zero Cool",
                         "Crash Override", "Acid Burn", "The Phantom Phreak", "Cereal Killer", "Lord Nikon",
                         "The Plague", "The Gibson Killer", "Da Vinci"]
    nick_prefix = ["Sweet", "Swift", "Slick", "The", "The Mad", "Stylin'", "Big", "The Big", "Big City",
                   "Big Slack Attack", "Beast Mode", "Master", "Steel", "Diamond-Tipped", "Iron", "Cousin", "T-Tops",
                   "T-Bone", "Hackmaster", "Monster", "Grandmaster", "M.C.", "Poker Face", "Gold Tooth", "Maserati",
                   "Fast Talkin'", "Glam", "The Animal", "Maddog", "Doctor"]
    name_parts = name.split()
    if len(name_parts) < 2:
        nick = get_random_rhyme(name)

        if not nick:
            return "{}– A.K.A. \"{}\"".format(name, random.choice(mobster_nicknames)).title()
        if random.randint(0, 10) > 4:
            nick = "{} {}".format(name, random.choice(nick_prefix))
        return "{}– A.K.A. \"{}\"".format(name, nick).title()
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
    transformations = [leet_speak, shift_vowels, nickname, jargon]
    return transformations[index](input)


def jargon(name):
    verbs = ["reinvent", "unpack", "pencil-in", "touch base on", "maximize", "resonate with", "preplan", "preschedule",
             "push the envelope on", "ideate about", "reincentivize", "deincentivize", "incentivize",
             "get on board with",
             "come up to speed on", "reprioritize", "deprioritize", "prioritize"
                                                                    "fish or cut bait with", "evangelize",
             "circle the wagons on", "circle back around to", "do a deep dive on",
             "innovate on", "enact change on", "give 110% on", "leverage", "take it to the next level with",
             "get buy-in on", "make hay with", "move the needle on", "scale", "vertically integrate", "rearchitect",
             "punt on", "make a business case for", "be a change agent for", "champion",
             "proactively guesstimate about",
             "heard cats for", "raise the bar on", "maintain radio silence on", "reach out about",
             "avoid reinventing the wheel with", "take strides on", "task", "add value to", "become a stakeholder in",
             "implement solutions", "monetize", "say \"it is what it is\" about", "bake in", "champion",
             "avoid boiling the ocean with", "gain traction on", "utilize"]

    adjectives = ["full-service", "robust", "high price-point", "best of breed", "frictionless", "turnkey",
                  "game changing", "mission-critical", "proactive", "seamless", "soup-to-nuts", "value-added",
                  "win-win", "world class", "bleeding-edge"]

    plural_nouns = ["dogfood", "hard stops", "solutions", "key learnings", "best practices", "core competencies",
                    "Kool-Aid", "ecosystems", "800lb gorillas", "action items", "spinning plates",
                    "bells and whistles", "brain dumps", "business cases", "stakeholders", "moving parts",
                    "best practices",
                    "change agents", "deliverables", "evangelists", "guesstimates", "hearded cats", "human capital",
                    "rocket science", "brain surgery", "skin in the game", "valued partners",
                    "bang for your buck", "low-hanging fruit", "magic bullets", "next steps",
                    "pain points", "paradigm shifts", "secret sauce", "zero-sum games"]

    prefix = ["Going forward", "At the end of the day", "Where the rubber hits the road",
              "While we're all on the same page", "While things are still up in the air"]

    suffix = ["with the big wigs", "in the c-suite", ", and throw it over the fence", "on a level playing field",
              "with a sense of urgency", "with an outside-of-the-box approach", "and run it up the flagpole"]

    adjective = "" if random.random() > 0.5 else "{} ".format(random.choice(adjectives))
    j = "{} will {} {}{}".format(
        name,
        random.choice(verbs),
        adjective,
        random.choice(plural_nouns)
    )
    prefix_suffix_seed = random.random()

    if prefix_suffix_seed < 0.25:
        j = "{} {}".format(j, random.choice(suffix))
    elif prefix_suffix_seed > 0.75:
        j = "{}, {}".format(random.choice(prefix), j)

    return "{}.".format(j.capitalize())


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)