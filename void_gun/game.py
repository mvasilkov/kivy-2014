import math
from random import random as rand, choice as randc

from kivy.clock import Clock
from kivy.graphics import Mesh
from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget

from .util import load_tex_uv


class Game(Widget):
    '''Game renderer'''

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'multiquad.glsl'
        Widget.__init__(self, **kwargs)

        self.vertex_format = (
            ('vCenter', 2, 'float'),
            ('vRotation', 1, 'float'),
            ('vPosition', 2, 'float'),
            ('vTexCoords0', 2, 'float'),
        )
        self.tex, self.tex_uv = load_tex_uv('test.atlas')

        Clock.schedule_interval(self.update_glsl, 60 ** -1)

    def update_glsl(self, nap):
        self.canvas.clear()
        self.random_fill(96)
        Clock.unschedule(self.update_glsl)

    def random_fill(self, count):
        width, height = self.size
        tex_list = self.tex_uv.keys()
        objects = [(rand() * width, rand() * height, rand() * math.pi * 2,
                    randc(tex_list)) for c in xrange(count)]
        self.render(objects)

    def render(self, objects):
        indices = []
        ix = indices.extend
        for c in xrange(0, len(objects) << 2, 4):
            ix((c, c + 1, c + 2, c + 2, c + 3, c))

        vertices = []
        vx = vertices.extend
        for obj in objects:
            uv = self.tex_uv[obj[3]]
            vx((
                obj[0], obj[1], obj[2], -uv[4], -uv[5], uv[0], uv[1],
                obj[0], obj[1], obj[2],  uv[4], -uv[5], uv[2], uv[1],
                obj[0], obj[1], obj[2],  uv[4],  uv[5], uv[2], uv[3],
                obj[0], obj[1], obj[2], -uv[4],  uv[5], uv[0], uv[3],
            ))

        self.canvas.add(Mesh(indices=indices, vertices=vertices,
                             fmt=self.vertex_format, mode='triangles',
                             texture=self.tex))
