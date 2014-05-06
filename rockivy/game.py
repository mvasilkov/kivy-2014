from kivy.clock import Clock
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget

from .fretboard import update_tex_uv, build_fretboard
from .tuning import TUNING_DEFAULT
from .util import R9, load_tex_uv

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


class Game(Widget):
    '''Game renderer'''

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'multiquad.glsl'

        Widget.__init__(self, **kwargs)

        self.tex, self.tex_uv = load_tex_uv('a.atlas')
        update_tex_uv(self.tex_uv)

        self.tuning = TUNING_DEFAULT
        self.build()

        from kivy.core.window import Window
        global g_window
        g_window = Window

    def build(self):
        fretboard = build_fretboard(self.tuning)
        self.begin_cursor = len(fretboard) * VERTEX_SIZE * 4
        fretboard += [R9(x=0, y=0, rot=0, size=1, op=1, tex='cursor')]

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

    def on_start(self):
        Clock.schedule_interval(self.update_glsl, 60 ** -1)

    def update_glsl(self, nap):
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
        self.canvas.add(Mesh(indices=self.indices, vertices=self.vertices,
                             fmt=VERTEX_FORMAT, mode='triangles',
                             texture=self.tex))

    def set_tuning(self, tuning):
        self.tuning = tuning
        self.build()
