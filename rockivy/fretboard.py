from .tuning import get_string
from .util import Quad, mutate

FRET_COUNT = 16
FRET_SPACING = 55

STRING_COUNT = 6
STRING_SPACING = 30

FRET_LENGTH = (STRING_COUNT - 1) * STRING_SPACING
STRING_LENGTH = FRET_COUNT * FRET_SPACING

LEGEND_OFFSET_X = 20
LEGEND_OFFSET_Y = 25

FB_LEFT = (960 - STRING_LENGTH) * 0.5 + LEGEND_OFFSET_X * 0.5 + 5
FB_BOTTOM = (540 - FRET_LENGTH) * 0.5 + LEGEND_OFFSET_Y + 40

g_animooted = True

try:
    _test = xrange(0)
    del _test
except NameError:
    xrange = range


def set_ani(val):
    global g_animooted
    g_animooted = val


def update_tex_uv(tex_uv):
    tex_uv['fret'] = mutate(tex_uv['fret'], {5: FRET_LENGTH * 0.5})

    tex_uv.update([('string_%d' % c,
                    mutate(tex_uv['string'],
                           {4: STRING_LENGTH * 0.5 + tex_uv['fret'][4],
                            5: (c >> 1) + 1})) for c in xrange(STRING_COUNT)])


def _frets():
    return [Quad(x=c * FRET_SPACING + FB_LEFT,
                 y=FRET_LENGTH * 0.5 + FB_BOTTOM,
                 size=1, tex='fret')
            for c in xrange(FRET_COUNT + 1)]


def _strings():
    return [Quad(x=STRING_LENGTH * 0.5 + FB_LEFT,
                 y=FRET_LENGTH - (c * STRING_SPACING) + FB_BOTTOM,
                 size=1, tex='string_%d' % c)
            for c in xrange(STRING_COUNT)]


def _numbers():
    return [Quad(x=(c - 0.5) * FRET_SPACING + FB_LEFT,
                 y=FB_BOTTOM + 0.5 - LEGEND_OFFSET_Y,
                 size=1, tex='num_%d' % c)
            for c in xrange(1, FRET_COUNT + 1)]


def _tuning(notes, scale_notes, root_note):
    res = [Quad(x=FB_LEFT - LEGEND_OFFSET_X,
                y=FRET_LENGTH - (c * STRING_SPACING) + FB_BOTTOM, size=1,
                tex='root_note_tun' if notes[c] == root_note else 'note_tun')
           for c in xrange(STRING_COUNT) if notes[c] in scale_notes]
    return res + [Quad(x=FB_LEFT - LEGEND_OFFSET_X,
                       y=FRET_LENGTH - (c * STRING_SPACING) + FB_BOTTOM,
                       size=1, tex='tun_%s' % notes[c])
                  for c in xrange(STRING_COUNT)]

_sz = lambda c: ((FRET_COUNT - c) / (FRET_COUNT * 10.0)
                 if g_animooted else 1)


def _notes(string, notes, scale_notes, root_note):
    y = FRET_LENGTH - (string * STRING_SPACING) + FB_BOTTOM
    res = [Quad(x=(c + 0.5) * FRET_SPACING + 0.5 + FB_LEFT, y=y, size=_sz(c),
                tex='root_note' if notes[c] == root_note else 'note')
           for c in xrange(FRET_COUNT) if notes[c] in scale_notes]
    return res + [Quad(x=(c + 0.5) * FRET_SPACING + 0.5 + FB_LEFT,
                       y=y, size=_sz(c), tex='note_%s' % notes[c])
                  for c in xrange(FRET_COUNT) if notes[c] in scale_notes]


def build_fretboard(scale, tuning):
    res = []
    rx = res.extend

    rx(_frets())
    rx(_strings())
    rx(_numbers())
    rx(_tuning(tuning['notes'], scale.notes, scale.root_note))
    for c in xrange(STRING_COUNT):
        string = get_string(tuning['notes'][c], FRET_COUNT)
        rx(_notes(c, string, scale.notes, scale.root_note))

    return res
