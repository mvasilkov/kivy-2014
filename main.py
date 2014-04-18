import kivy
kivy.require('1.8.0')

from kivy import utils
from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config

from void_gun.game import Game


class KivyApp(App):
    '''Application class'''

    def build(self):
        EventLoop.ensure_window()
        EventLoop.window.title = self.title = 'Kivy App Contest 2014'
        return Game()

if __name__ == '__main__':
    Config.set('graphics', 'width', '960')
    Config.set('graphics', 'height', '540')  # 16:9
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    from kivy.core.window import Window
    Window.clearcolor = utils.get_color_from_hex('#242424')

    KivyApp().run()
