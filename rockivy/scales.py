from abc import ABCMeta, abstractproperty

from .tuning import get_seq

(S, T, I3) = range(3)


def get_notes(root_note, size):
    notes = get_seq(root_note)
    res = [root_note]
    for sz in size:
        for c in xrange(sz):
            next(notes)
        res.append(next(notes))
    return res


class BaseSeq(object):
    __metaclass__ = ABCMeta

    def __init__(self, root_note):
        self.root_note = root_note
        self.notes = set(get_notes(root_note, self.size))

    def nop(self):
        pass

    name = abstractproperty(nop)
    size = abstractproperty(nop)


class Major(BaseSeq):
    name = 'Major Scale'
    size = (T, T, S, T, T, T, S)


class Minor(BaseSeq):
    name = 'Minor Scale'
    size = (T, S, T, T, S, T, T)


class Blues(BaseSeq):
    name = 'Blues Scale'
    size = (I3, T, S, S, I3, T)

SCALES = (Major, Minor, Blues)
