# coding: utf8
from build.numbers import render_text
from rockivy.tuning import NOTES

if __name__ == '__main__':
    for n in NOTES:
        u = n.replace('#', u'♯')
        render_text(u, color='#ffffff', bg_color=None, font_size=11,
                    padding_top=-1, out_width=24, out_height=20,
                    out_path=u'./media/tex/note_%s.png' % n, tolsto=True)
