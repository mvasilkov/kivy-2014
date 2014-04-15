from kivy.graphics.instructions import RenderContext
from kivy.uix.widget import Widget


class Game(Widget):
    '''Game renderer'''

    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        Widget.__init__(self, **kwargs)
