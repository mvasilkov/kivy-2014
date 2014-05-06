from kivy import utils
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton

COLOR_DOWN = utils.get_color_from_hex('#ffffff')
COLOR_NORMAL = utils.get_color_from_hex('#2e3436')


def state_change(btn, state):
    if state == 'down':
        btn.color = COLOR_DOWN
    else:
        btn.color = COLOR_NORMAL


class Radio(ToggleButton):
    '''Radio button'''

    def __init__(self, **kwargs):
        kwargs['background_normal'] = 'media/ui/btn.png'
        kwargs['background_down'] = 'media/ui/btn_down.png'
        kwargs['border'] = (0,) * 4

        if kwargs.get('state') == 'down':
            kwargs['color'] = COLOR_DOWN
        else:
            kwargs['color'] = COLOR_NORMAL

        kwargs['markup'] = False

        ToggleButton.__init__(self, **kwargs)

        self.bind(state=state_change)

    def _do_press(self):
        if self.state == 'normal':
            ToggleButtonBehavior._do_press(self)
