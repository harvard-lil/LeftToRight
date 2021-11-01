import random
from num2words import num2words


# maintaining this list should not be necessary once
# https://github.com/savoirfairelinux/num2words/pull/208,
# which implements supported_lang, is merged and released
languages = [
    'en',
    'ar',
    'cz',
    'de',
    'dk',
    'en_GB',
    'en_IN',
    'es',
    'es_CO',
    'es_VE',
    # 'eu',  # not implemented
    'fi',
    'fr',
    'fr_CH',
    'fr_BE',
    'fr_DZ',
    'he',
    'id',
    'it',
    'ja',
    'kn',
    'ko',
    'lt',
    'lv',
    'no',
    'pl',
    'pt',
    'pt_BR',
    'sl',
    'sr',
    'ro',
    'ru',
    'sl',
    'tr',
    'th',
    'vi',
    'nl',
    'uk'
]


def count(n):
    """
    Manager for randomizing counting systems;
    input is expected to be zero-based, and output is
    one-based.
    """
    r = random.random()
    if r < 0.2:
        return str(n + 1)
    elif r < 0.4:
        return yan_tan(n)
    else:
        try:
            return num2words(n + 1, lang=random.choice(languages))
        except NotImplementedError:
            return str(n + 1)


def yan_tan(n):
    """
    from https://en.wikipedia.org/wiki/Yan_tan_tethera
    input is expected to be zero-based
    """
    systems = {
        'derbyshire_dales': [
            'yan',
            'tan',
            'tethera',
            'methera',
            'pip',
            'sethera',
            'lethera',
            'hovera',
            'dovera',
            'dick'
        ]
    }
    try:
        return systems['derbyshire_dales'][n]
    except IndexError:
        return str(n + 1)
