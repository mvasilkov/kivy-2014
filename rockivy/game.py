from kivy.clock import Clock
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext, Callback
from kivy.graphics.opengl import (glBlendFunc,
                                  GL_ONE, GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA)
from kivy.resources import resource_find
from kivy.uix.widget import Widget

from .fretboard import update_tex_uv, build_fretboard, set_ani
from .scales import SCALES
from .tuning import NOTES, TUNING_DEFAULT
from .util import Quad, load_tex_uv, blending_is_broken

CURSOR_OFFSET_X = 16
CURSOR_OFFSET_Y = -16

VERTEX_FORMAT = (
    (b'vCenter', 2, 'float'),
    (b'vScale', 1, 'float'),
    (b'vPosition', 2, 'float'),
    (b'vTexCoords0', 2, 'float'),
)

VERTEX_SIZE = 7

g_window = None

try:
    _test = unicode('')
    del _test
except NameError:
    unicode = lambda a: a.__unicode__()


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
        self.canvas = RenderContext(use_parent_modelview=True,
                                    use_parent_projection=True)
        self.canvas.shader.source = resource_find('game.glsl')

        Widget.__init__(self, **kwargs)

        self.blending_is_broken = blending_is_broken()

        self.tex, self.tex_uv = load_tex_uv('a.atlas')
        update_tex_uv(self.tex_uv)

        self.root_note = NOTES[0]
        self.scale_class = SCALES[0]
        self.scale = self.scale_class(self.root_note)
        self.tuning = TUNING_DEFAULT
        self.build(False)

        from kivy.core.window import Window
        global g_window
        g_window = Window

    def build(self, updating=True):
        fretboard = build_fretboard(self.scale, self.tuning)

        if Game.REPLACE_CURSOR:
            self.begin_cursor = len(fretboard) * VERTEX_SIZE * 4
            fretboard += [Quad(x=0, y=0, size=1, tex='cursor')]

        self.indices = []
        ix = self.indices.extend
        for c in range(0, len(fretboard) << 2, 4):
            ix((c, c + 1, c + 2, c + 2, c + 3, c))

        self.vertices = []
        vx = self.vertices.extend
        self.animate = set()
        for i, o in enumerate(fretboard):
            uv = self.tex_uv[o[3]]
            vx((
                o[0], o[1], o[2], -uv[4], -uv[5], uv[0], uv[1],
                o[0], o[1], o[2],  uv[4], -uv[5], uv[2], uv[1],
                o[0], o[1], o[2],  uv[4],  uv[5], uv[2], uv[3],
                o[0], o[1], o[2], -uv[4],  uv[5], uv[0], uv[3],
            ))
            if o[2] < 1:
                self.animate.add(i)

        if updating:
            self.set_updating()

        self.update_heading()

    def set_updating(self):
        Clock.unschedule(self.update_glsl)
        Clock.schedule_interval(self.update_glsl, 60 ** -1)

    on_start = set_updating

    def update_glsl(self, nap):
        '''
        https://github.com/kivy/kivy/issues/2178

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
        '''

        if self.animate:
            for i in self.animate.copy():
                idx = i * VERTEX_SIZE * 4 + 2
                val = self.vertices[idx] * (nap * 25 + 1)

                if val >= 1:
                    val = 1
                    self.animate.remove(i)

                for c in (idx,
                          idx + VERTEX_SIZE,
                          idx + VERTEX_SIZE * 2,
                          idx + VERTEX_SIZE * 3):

                    self.vertices[c] = val

        if not self.animate and not Game.REPLACE_CURSOR:
            Clock.unschedule(self.update_glsl)

        self.canvas.clear()

        if self.blending_is_broken:
            self.canvas.before.add(select_blend_func)
            self.canvas.after.add(reset_blend_func)

        self.canvas.add(Mesh(indices=self.indices, vertices=self.vertices,
                             fmt=VERTEX_FORMAT, mode='triangles',
                             texture=self.tex))

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

    set_animooted = lambda self, val: set_ani(val)
