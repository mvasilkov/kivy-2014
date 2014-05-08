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
TUNING_Eb = {
    'name': u'\u00bd Step Down',
    'notes': (Dd, Ad, Fd, Cd, Gd, Dd),
}
TUNING_D = {
    'name': '1 Step Down',
    'notes': (D, A, F, C, G, D),
}
TUNING = (TUNING_DEFAULT, TUNING_DROP_D, TUNING_Eb, TUNING_D)


def get_string(start_note, count):
    seq = dropwhile(lambda n: n != start_note, cycle(NOTES))
    next(seq)
    return islice(seq, count)
