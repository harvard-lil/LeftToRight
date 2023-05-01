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


def count(ns):
    """
    Manager for randomizing counting systems;
    input is expected to be zero-based, and output is
    one-based.
    """
    r = random.random()
    if r < 0.2:
        return [str(n + 1) for n in ns]
    elif r < 0.4:
        return [yan_tan(n) for n in ns]
    else:
        while True:
            try:
                language = random.choice(languages)
                return [num2words(n + 1, lang=language) for n in ns]
            except NotImplementedError:
                pass


def yan_tan(n):
    """
    from https://en.wikipedia.org/wiki/Yan_tan_tethera
    input is expected to be zero-based
    """
    systems = {
        'lincolnshire': [
            'yan',
            'teyan',
            'tethera',
            'methera',
            'tic',
            'yan-a-tic',
            'teyan-a-tic',
            'tethera-tic',
            'methera-tic',
            'bub',
            'yan-a-bub',
            'teyan-a-bub',
            'tethera-bub',
            'methera-bub',
            'tic-a-bub',
            'yan-tic-a-bub',
            'teyan-tic-a-bub',
            'tethera-tic-a-bub',
            'methera-tic-a-bub',
            'gigget'
        ]
    }
    try:
        return systems['lincolnshire'][n]
    except IndexError:
        return str(n + 1)
