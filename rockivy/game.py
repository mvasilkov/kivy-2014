from collections import namedtuple

from kivy.clock import Clock
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget

from .util import load_tex_uv

CURSOR_OFFSET_X = 16
CURSOR_OFFSET_Y = -16

FRET_COUNT = 16
FRET_SPACING = 55

STRING_COUNT = 6
STRING_SPACING = 30

FRET_LENGTH = (STRING_COUNT - 1) * STRING_SPACING
STRING_LENGTH = FRET_COUNT * FRET_SPACING

FB_OFFSET_LEFT = (960 - STRING_LENGTH) * 0.5
FB_OFFSET_BOTTOM = (540 - FRET_LENGTH) * 0.5

R9 = namedtuple('Renderable', 'x y rot size op tex')

g_window = None


def mutate(t, changes):
    res = list(t)
    for idx, val in changes.iteritems():
        res[idx] = val
    return tuple(res)


def update_tex_uv(tex_uv):
    tex_uv['fret'] = mutate(tex_uv['fret'], {5: FRET_LENGTH * 0.5})

    tex_uv.update([('string_%d' % c,
                    mutate(tex_uv['string'],
                           {4: STRING_LENGTH * 0.5 + tex_uv['fret'][4],
                            5: (c >> 1) + 1})) for c in xrange(STRING_COUNT)])


def init_frets():
    return [R9(x=c * FRET_SPACING + FB_OFFSET_LEFT,
               y=FRET_LENGTH * 0.5 + FB_OFFSET_BOTTOM,
               rot=0, size=1, op=1, tex='fret')
            for c in xrange(FRET_COUNT + 1)]


def init_strings():
    return [R9(x=STRING_LENGTH * 0.5 + FB_OFFSET_LEFT,
               y=FRET_LENGTH - (c * STRING_SPACING) + FB_OFFSET_BOTTOM,
               rot=0, size=1, op=1, tex='string_%d' % c)
            for c in xrange(STRING_COUNT)]


class Game(Widget):
    '''Game renderer'''

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'multiquad.glsl'

        Widget.__init__(self, **kwargs)

        self.vertex_format = (
            ('vCenter', 2, 'float'),
            ('vRotation', 1, 'float'),
            ('vScale', 1, 'float'),
            ('vOpacity', 1, 'float'),
            ('vPosition', 2, 'float'),
            ('vTexCoords0', 2, 'float'),
        )
        self.tex, self.tex_uv = load_tex_uv('a.atlas')
        update_tex_uv(self.tex_uv)

        self.frets = init_frets()
        self.strings = init_strings()

        Clock.schedule_interval(self.update_glsl, 60 ** -1)

        from kivy.core.window import Window
        global g_window
        g_window = Window

    def update_glsl(self, nap):
        self.canvas.clear()
        objects = self.frets + self.strings
        cur_x, cur_y = g_window.mouse_pos
        objects.append(R9(x=cur_x + CURSOR_OFFSET_X,
                          y=cur_y + CURSOR_OFFSET_Y,
                          rot=0, size=1, op=1, tex='cursor'))
        self.render(objects)

    def render(self, objects):
        indices = []
        ix = indices.extend
        for c in xrange(0, len(objects) << 2, 4):
            ix((c, c + 1, c + 2, c + 2, c + 3, c))

        vertices = []
        vx = vertices.extend
        for o in objects:
            uv = self.tex_uv[o[5]]
            vx((
                o[0], o[1], o[2], o[3], o[4], -uv[4], -uv[5], uv[0], uv[1],
                o[0], o[1], o[2], o[3], o[4],  uv[4], -uv[5], uv[2], uv[1],
                o[0], o[1], o[2], o[3], o[4],  uv[4],  uv[5], uv[2], uv[3],
                o[0], o[1], o[2], o[3], o[4], -uv[4],  uv[5], uv[0], uv[3],
            ))

        self.canvas.add(Mesh(indices=indices, vertices=vertices,
                             fmt=self.vertex_format, mode='triangles',
                             texture=self.tex))
