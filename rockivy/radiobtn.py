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
        kwargs['background_normal'] = 'media/btn.png'

        if kwargs['group'] == 'notes':
            kwargs['background_down'] = 'media/btn_down_g.png'
        else:
            kwargs['background_down'] = 'media/btn_down.png'

        kwargs['border'] = (2,) * 4

        if kwargs.get('state') == 'down':
            kwargs['color'] = COLOR_DOWN
        else:
            kwargs['color'] = COLOR_NORMAL

        if kwargs['group'] == 'notes':
            kwargs['font_name'] = 'DroidSans-Regular.ttf'

        kwargs['font_size'] = 15
        kwargs['markup'] = False

        self.rel = kwargs['rel']
        del kwargs['rel']

        ToggleButton.__init__(self, **kwargs)

        self.bind(state=state_change)

    def _do_press(self):
        if self.state == 'normal':
            ToggleButtonBehavior._do_press(self)
