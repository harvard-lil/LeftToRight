import random
import string


transformations = dict()


def register(transformation):
    """
    Register a transformation function
    """
    transformations[transformation.__name__] = transformation
    return transformation


@register
def normal(name):
    return name


@register
def nicknames(name):
    mobster_nicknames = ["Joe Bananas", "Ice Pick Willie", "Johnny Sausage",
                         "Baby Shanks", "Whack-Whack", "Tick–Tock",
                         "Quack Quack", "The Wizard of Odds", "Louie Bagels",
                         "Tommy Sneakers", "Pat the Cat", "Chee-Chee",
                         "Tommy Karate", "Willie Potatoes", "Bootsie",
                         "Jimmy Dumps", "One Armed Ronnie", "The Toupee",
                         "Chicken Man", "Socks", "Jimmy Nap", "Charley Wagons",
                         "Joe the Builder", "Benny Squint", "Mr. Bread",
                         "Dopey Benny", "The Typewriter", "The Artichoke King",
                         "Shellackhead", "The Owl", "Louie Eggs",
                         "The Clutch Hand", "14th Street Steve", "Corky",
                         "Flipper", "Legs DiCocco", "The Golfer",
                         "The Reluctant Prince", "Georgie Neck", "Baldy Dom",
                         "Larry Fab", "George from Canada",
                         "Master of Disaster", "Dr. Doom", "Zero Cool",
                         "Crash Override", "Acid Burn", "The Phantom Phreak",
                         "Cereal Killer", "Lord Nikon", "The Plague",
                         "The Gibson Killer", "Da Vinci"]
    nick_prefix = ["Sweet", "Swift", "Slick", "The", "The Mad", "Stylin'",
                   "Big", "The Big", "Big City", "Big Slack Attack",
                   "Beast Mode", "Master", "Steel", "Diamond-Tipped", "Iron",
                   "Cousin", "T-Tops", "T-Bone", "Hackmaster", "Monster",
                   "Grandmaster", "M.C.", "Poker Face", "Gold Tooth",
                   "Maserati", "Fast Talkin'", "Glam", "The Animal",
                   "Maddog", "Doctor"]
    name_parts = name.split(' ', 1)
    if len(name_parts) < 2:
        if random.randint(0, 10) > 4:
            nick = f"{name} {random.choice(nick_prefix)}"
        else:
            nick = random.choice(mobster_nicknames)
        return f"{name}– A.K.A. \"{nick}\""
    else:
        name_parts_for_nick = name_parts.copy()
        random.shuffle(name_parts_for_nick)
        nick = random.choice(mobster_nicknames)
        if random.randint(0, 10) > 4:
            nick = f"{random.choice(nick_prefix)} {nick}"
        return f'{name_parts[0]} \"{nick}\" {" ".join(name_parts[1:])}'


@register
def shifted(name):
    vowels = ["a", "e", "i", "o", "u", "y"]
    output = ''
    for char in name.lower():
        if char in vowels:
            output += random.choice(vowels)
        else:
            output += char
    return output.title()


@register
def umlauted(name):
    backwards = " ".join(name.lower()[::-1].split()[::-1])
    vowels = {'a': 'ä', 'e': 'ë', 'i': 'ï', 'o': 'ö', 'u': 'ü', 'y': 'ÿ'}
    output = ''
    translate = True
    for char in backwards:
        if translate and char in vowels:
            output += vowels[char]
            translate = False
        elif char == ' ':
            output += ' '
            translate = True
        else:
            output += char
    return output.title()


@register
def leet(name):
    leet = {'a': ['4', '@', 'Д'],
            'b': ['8', 'ß'],
            'c': ['©', '¢'],
            'd': ['D'],
            'e': ['3', '€'],
            'f': ['pH'],
            'g': ['6', ],
            'h': ['H'],
            'i': ['1', '|', '!'],
            'j': ['J', ],
            'k': ['K', ],
            'l': ['1'],
            'm': ['|\/|'],  # noqa
            'n': ['И'],
            'o': ['0', 'Ø'],
            'p': ['p'],
            'q': ['kw', 'Q'],
            'r': ['Я', '®'],
            's': ['5', '$', '§'],
            't': ['7', '+'],
            'u': ['U'],
            'v': ['\/'],  # noqa
            'w': ['\X/', 'Ш'],  # noqa
            'x': ['Ж'],
            'y': ['¥', 'Ч'],
            'z': ['2']}
    output = ''
    for char in name.split(' ', 1)[0].lower():
        if char in leet:
            output += random.choice(leet[char])
        else:
            output += char
    return "-= {} =-".format(output)


@register
def jargon(name):
    verbs = ["reinvent", "unpack", "pencil-in", "touch base on", "maximize",
             "resonate with", "preplan", "preschedule", "push the envelope on",
             "ideate about", "reincentivize", "deincentivize", "incentivize",
             "get on-board with", "come up-to-speed on", "reprioritize",
             "deprioritize", "prioritize", "fish or cut bait with",
             "evangelize", "circle the wagons on", "circle back around to",
             "do a deep dive on", "innovate on", "enact change with",
             "give 110% using", "leverage", "take it to the next level with",
             "get buy-in from key stakeholders about", "make hay using",
             "move the needle on", "scale", "vertically integrate",
             "rearchitect", "punt on", "make a business case for",
             "be a change agent for", "champion",
             "proactively guesstimate about",
             "heard cats for", "raise the bar with",
             "maintain radio silence on", "reach out about",
             "avoid reinventing the wheel with", "take strides on",
             "task team members with", "add value to",
             "become a key stakeholder in", "implement solutions for",
             "monetize", "bake in", "champion", "avoid boiling the ocean with",
             "gain traction with", "utilize", "herd cats for",
             "make informed guesstimates about", "re-evaluate",
             "incorporate feedback about", "minimize the impact of",
             "let the chips fall where they may with",
             "wrap their brain around", "do some blue sky thinking about",
             "move the goalposts on", "drill-down on",
             "avoid dropping the ball on", "review", "facilitate",
             "get in-the-loop about", "engage thought leaders on",
             "eat our own dogfood for",
             "be in a holding pattern until key stakeholders approve",
             "iron out", "ideate best approaches to", "blueprint",
             "free up some cycles for"]

    adjectives = ["full-service", "robust", "high-price-point",
                  "best-of-breed", "frictionless", "turn-key", "game-changing",
                  "mission-critical", "proactive", "seamless", "soup-to-nuts",
                  "value-added", "win-win", "world-class", "bleeding-edge",
                  "the highest bang for our buck", "zero-sum",
                  "belt-and-suspenders", "above-board", "restructured",
                  "user-focused", "risk-managing", "disruptive",
                  "high-granularity", "critical", "key"]

    plural_nouns = ["hard stops", "solutions", "learnings", "best practices",
                    "cost analyses", "core competencies", "ecosystems",
                    "800lb gorilla issues", "action items", "spinning plates",
                    "bells and whistles", "brain dumps", "business cases",
                    "stakeholders", "moving parts", "best practices",
                    "change agents", "deliverables", "evangelism",
                    "guesstimates", "human capital", "rocket science",
                    "brain surgery", "valued partners", "low-hanging fruit",
                    "magic bullets", "next steps", "pain points",
                    "paradigm shifts", "secret sauce", "litmus tests",
                    "bio breaks", "life cycles", "markets", "timelines",
                    "strategies", "benchmarks", "paradigms", "metrics",
                    "red tape", "business practices", "corporate messaging",
                    "institutional learnings", "institutional knowlege",
                    "key players"]

    prefix = ["Going forward", "Moving forward", "At the end of the day",
              "While key players are in a holding pattern",
              "While we're all on the same page",
              "While things are still up in the air", "Across the board"]

    suffix = ["utilizing feedback from the big wigs",
              "in partnership with the c-suite",
              "on a level playing field", "with a sense of urgency",
              "embracing out-of-the-box approaches",
              "and run it up the flagpole",
              "in partnership with key stakeholders",
              "without just throwing it over-the-fence afterwards",
              "with an eye towards best practices",
              "where the rubber hits the road"]

    adjective = ""
    if random.random() > 0.5:
        adjective = f"{random.choice(adjectives)} "
    j = "{} will {} {}{}".format(
        name.split(' ', 1)[0].capitalize(),
        random.choice(verbs),
        adjective,
        random.choice(plural_nouns)
    )
    prefix_suffix_seed = random.random()

    if prefix_suffix_seed < 0.15:
        j = f"{j} {random.choice(suffix)}"
    elif prefix_suffix_seed > 0.75:
        j = f"{random.choice(prefix).capitalize()}, {j}"

    return f"{name.title()}: {j}."


@register
def cats(name):
    catname = random.choice([
        {"name": "Asparagus", "nickname": "Theatre Cat"},
        {"name": "Bombalurina"},
        {"name": "Bustopher Jones", "nickname": "Cat About Town"},
        {"name": "Demeter"},
        {"name": "Grizabella"},
        {"name": "Jellylorum"},
        {"name": "Sillabub"},
        {"name": "Jennyanydots", "nickname": "Old Gumbie Cat"},
        {"name": "Macavity", "nickname": "Mystery Cat"},
        {"name": "Mr. Mistoffelees"},
        {"name": "Mungojerrie"},
        {"name": "Munkustrap"},
        {"name": "Old Deuteronomy"},
        {"name": "Rumpleteazer"},
        {"name": "Rum Tum Tugger"},
        {"name": "Skimbleshanks", "nickname": "Railway Cat"},
        {"name": "Victoria"}
    ])
    namelist = [namepart.title() for namepart in name.split(' ', 1)]
    n = namelist[0]
    cat = catname['name']
    if "nickname" in catname and len(namelist) == 1:
        return f"{n}, known to be the {catname['nickname']}, is {cat}"
    elif len(namelist) == 1:
        return f"{n} a.k.a. {cat}"
    elif "nickname" in catname:
        return f"{n} \"{cat}\" {namelist[1]} is the {catname['nickname']}"
    else:
        return f"{n} \"{cat}\" {namelist[1]}"


@register
def experiment(name):
    return ''.join(sorted(name.lower().replace(' ', '').translate(str.maketrans('', '', string.punctuation))))  # noqa
