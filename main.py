import kivy
kivy.require('1.8.0')

from kivy import utils
from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config

from rockivy.game import Game


class KivyApp(App):
    '''Application class'''

    def build(self):
        EventLoop.ensure_window()
        EventLoop.window.title = self.title = 'Rockivy | Kivy App Contest 2014'
        return Game()

if __name__ == '__main__':
    Config.set('graphics', 'width', '960')
    Config.set('graphics', 'height', '540')  # 16:9
    Config.set('graphics', 'resizable', '0')
    Config.set('graphics', 'show_cursor', '0')
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    from kivy.core.window import Window
    Window.clearcolor = utils.get_color_from_hex('#ffffff')

    app = KivyApp()
    app.load_config()
    app.root = app.build()
    app.built = True
    app.run()
