import cairo
import pango
import pangocairo
from kivy import utils


def render_text(txt, color='#2e3436', bg_color='#ffffff',
                font_name='Segoe UI', font_style='', font_size=9,
                out_width=24, out_height=24, padding_top=0,
                out_path='out.png'):

    color = utils.get_color_from_hex(color)[:3]
    bg_color = utils.get_color_from_hex(bg_color)[:3]

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, out_width, out_height)
    c_context = cairo.Context(surface)
    p_context = pangocairo.CairoContext(c_context)

    c_context.rectangle(0, 0, out_width, out_height)
    c_context.set_source_rgb(*bg_color)
    c_context.fill()

    font = pango.FontDescription('%s, %s %d' %
                                 (font_name, font_style, font_size))
    layout = p_context.create_layout()

    layout.set_font_description(font)
    layout.set_alignment(pango.ALIGN_CENTER)
    layout.set_width(out_width)
    layout.set_text(txt)

    c_context.translate(out_width * 0.5, padding_top)
    c_context.set_source_rgb(*color)
    p_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    p_context.update_layout(layout)
    p_context.show_layout(layout)

    with open(out_path, 'wb') as out:
        surface.write_to_png(out)

if __name__ == '__main__':
    for i in xrange(1, 17):
        render_text(str(i), font_name='Fira Mono OT', font_size=10,
                    out_width=23, out_height=19,
                    out_path='./media/tex/num_%d.png' % i)
