from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex as css_color

from .radiobtn import Radio

PADDING = 4
SIZE = (110, 40)


def init_ui(game):
    tun_label = Label(text='Tuning', color=css_color('#2e3436'), markup=False)
    tun_default = Radio(text='Standard', group='tun', state='down')
    tun_drop_d = Radio(text='Drop D', group='tun')
    tun_d_standard = Radio(text='D Standard', group='tun')

    view = Widget()

    for i, w in enumerate([tun_label, tun_default, tun_drop_d,
                           tun_d_standard]):
        w.pos = (i * SIZE[0] + (i + 1) * PADDING, PADDING)
        w.size = SIZE
        view.add_widget(w)

    view.add_widget(game)
    return view
