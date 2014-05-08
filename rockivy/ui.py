from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex as css_color

from .radiobtn import Radio
from .tuning import TUNING

PADDING = 4
SIZE = (110, 40)


def init_ui(game):
    tun_label = Label(text='Tuning', color=css_color('#2e3436'), markup=False)
    tun_widgets = [tun_label]

    def state_change(btn, state):
        if state == 'down':
            game.set_tuning(btn.rel)

    for i, tun in enumerate(TUNING):
        kwargs = {
            'text': tun['name'],
            'group': 'tun',
            'rel': tun,
        }

        if not i:
            kwargs['state'] = 'down'

        btn = Radio(**kwargs)
        btn.bind(state=state_change)
        tun_widgets.append(btn)

    view = Widget()

    for i, w in enumerate(tun_widgets):
        w.pos = (i * SIZE[0] + (i + 1) * PADDING, PADDING)
        w.size = SIZE
        view.add_widget(w)

    view.add_widget(game)
    return view
