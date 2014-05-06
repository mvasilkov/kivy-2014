from itertools import cycle, dropwhile, islice

NOTES = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
C, Cd, D, Dd, E, F, Fd, G, Gd, A, Ad, B = NOTES

TUNING_DEFAULT = {
    'notes': (E, B, G, D, A, E),
}
TUNING_DROP_D = {
    'notes': (E, B, G, D, A, D),
}
TUNING_D_STANDARD = {
    'notes': (Dd, Ad, Fd, Cd, Gd, Dd),
}


def get_string(start_note, count):
    seq = dropwhile(lambda n: n != start_note, cycle(NOTES))
    next(seq)
    return islice(seq, count)
