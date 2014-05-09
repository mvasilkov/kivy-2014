from itertools import cycle, dropwhile, islice

NOTES = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
C, Cd, D, Dd, E, F, Fd, G, Gd, A, Ad, B = NOTES

TUNING_DEFAULT = {
    'name': 'Standard',
    'notes': (E, B, G, D, A, E),
}
TUNING_DROP_D = {
    'name': 'Drop D',
    'notes': (E, B, G, D, A, D),
}
TUNING_DROP_C = {
    'name': 'Drop C',
    'notes': (D, A, F, C, G, C),
}
TUNING_Eb = {
    'name': u'\u00bd Step Down',
    'notes': (Dd, Ad, Fd, Cd, Gd, Dd),
}
TUNING_D = {
    'name': '1 Step Down',
    'notes': (D, A, F, C, G, D),
}
TUNING_OPEN_D = {
    'name': 'Open D',
    'notes': (D, A, Fd, D, A, D),
}
TUNING_OPEN_G = {
    'name': 'Open G',
    'notes': (D, B, G, D, G, D),
}
TUNING = (TUNING_DEFAULT, TUNING_DROP_D, TUNING_DROP_C, TUNING_OPEN_D,
          TUNING_OPEN_G, TUNING_Eb, TUNING_D)


def get_seq(start_note):
    seq = dropwhile(lambda n: n != start_note, cycle(NOTES))
    next(seq)
    return seq


def get_string(start_note, count):
    return tuple(islice(get_seq(start_note), count))
