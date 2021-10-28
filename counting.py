def yan_tan(n):
    """
    from https://en.wikipedia.org/wiki/Yan_tan_tethera
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
        return str(n)
