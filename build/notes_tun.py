# coding: utf8
from build.numbers import render_text
from rockivy.tuning import NOTES

if __name__ == '__main__':
    for n in NOTES:
        u = n.replace('#', u'♯')
        render_text(u, font_size=11, padding_top=-1, out_width=23,
                    out_height=19, out_path=u'./build/tex/tun_%s.png' % n)
