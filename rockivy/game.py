from kivy.clock import Clock
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext, Callback
from kivy.graphics.opengl import (glBlendFunc,
                                  GL_ONE, GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA)
from kivy.resources import resource_find
from kivy.uix.widget import Widget

from .fretboard import update_tex_uv, build_fretboard
from .scales import SCALES
from .tuning import NOTES, TUNING_DEFAULT
from .util import Quad, load_tex_uv

CURSOR_OFFSET_X = 16
CURSOR_OFFSET_Y = -16

VERTEX_FORMAT = (
    ('vCenter', 2, 'float'),
    ('vRotation', 1, 'float'),
    ('vScale', 1, 'float'),
    ('vOpacity', 1, 'float'),
    ('vPosition', 2, 'float'),
    ('vTexCoords0', 2, 'float'),
)

VERTEX_SIZE = 9

g_window = None


@Callback
def select_blend_func(instr):
    '''Premultiplied alpha'''
    glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)


@Callback
def reset_blend_func(instr):
    '''Normal alpha'''
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


class Game(Widget):
    '''Game renderer'''

    REPLACE_CURSOR = False

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = resource_find('game.glsl')

        Widget.__init__(self, **kwargs)

        self.tex, self.tex_uv = load_tex_uv('a.atlas')
        update_tex_uv(self.tex_uv)

        self.root_note = NOTES[0]
        self.scale_class = SCALES[0]
        self.scale = self.scale_class(self.root_note)
        self.tuning = TUNING_DEFAULT
        self.build()

        from kivy.core.window import Window
        global g_window
        g_window = Window

    def build(self):
        fretboard = build_fretboard(self.scale, self.tuning)

        if Game.REPLACE_CURSOR:
            self.begin_cursor = len(fretboard) * VERTEX_SIZE * 4
            fretboard += [Quad(x=0, y=0, rot=0, size=1, op=1, tex='cursor')]

        self.indices = []
        ix = self.indices.extend
        for c in xrange(0, len(fretboard) << 2, 4):
            ix((c, c + 1, c + 2, c + 2, c + 3, c))

        self.vertices = []
        vx = self.vertices.extend
        for o in fretboard:
            uv = self.tex_uv[o[5]]
            vx((
                o[0], o[1], o[2], o[3], o[4], -uv[4], -uv[5], uv[0], uv[1],
                o[0], o[1], o[2], o[3], o[4],  uv[4], -uv[5], uv[2], uv[1],
                o[0], o[1], o[2], o[3], o[4],  uv[4],  uv[5], uv[2], uv[3],
                o[0], o[1], o[2], o[3], o[4], -uv[4],  uv[5], uv[0], uv[3],
            ))

        self.update_heading()

    def on_start(self):
        Clock.schedule_interval(self.update_glsl, 60 ** -1)

    def update_glsl(self, nap):
        if Game.REPLACE_CURSOR:
            cur_x, cur_y = g_window.mouse_pos
            cur_x += CURSOR_OFFSET_X
            cur_y += CURSOR_OFFSET_Y

            for c in (self.begin_cursor,
                      self.begin_cursor + VERTEX_SIZE,
                      self.begin_cursor + VERTEX_SIZE * 2,
                      self.begin_cursor + VERTEX_SIZE * 3):

                self.vertices[c] = cur_x
                self.vertices[c + 1] = cur_y

        self.canvas.clear()
        self.canvas.before.add(select_blend_func)
        self.canvas.add(Mesh(indices=self.indices, vertices=self.vertices,
                             fmt=VERTEX_FORMAT, mode='triangles',
                             texture=self.tex))
        self.canvas.after.add(reset_blend_func)

    def set_root_note(self, root_note):
        self.root_note = root_note
        self.scale = self.scale_class(self.root_note)
        self.build()

    def set_scale_class(self, scale_class):
        self.scale_class = scale_class
        self.scale = self.scale_class(self.root_note)
        self.build()

    def set_tuning(self, tuning):
        self.tuning = tuning
        self.build()

    _heading = None

    def update_heading(self):
        if self._heading:
            self._heading.text = u'%s \u2013 %s tuning' % (unicode(self.scale),
                                                           self.tuning['name'])
