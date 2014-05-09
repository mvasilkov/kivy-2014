from __future__ import division

from collections import namedtuple
import json
from os.path import join as path_join, realpath, dirname

from kivy.core.image import Image

PATH = realpath(path_join(dirname(__file__), '..', 'media'))

Quad = namedtuple('Quad', 'x y rot size op tex')


def load_tex_uv(atlas_name):
    with open(path_join(PATH, atlas_name), 'rb') as istream:
        atlas_obj = json.load(istream)

    tex_name, mapping = atlas_obj.popitem()
    tex = Image(path_join(PATH, tex_name)).texture
    tex_width, tex_height = tex.size

    res = {}
    for name, val in mapping.iteritems():
        x1, y1 = val[:2]
        x2, y2 = x1 + val[2], y1 + val[3]
        res[name] = (x1 / tex_width, 1 - y1 / tex_height,
                     x2 / tex_width, 1 - y2 / tex_height,
                     val[2] * 0.5, val[3] * 0.5)

    return tex, res


def mutate(t, changes):
    res = list(t)
    for idx, val in changes.iteritems():
        res[idx] = val
    return tuple(res)
