import kivy
kivy.require('1.8.0')

from kivy import utils
from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config
from kivy.resources import resource_find

from rockivy.game import Game
from rockivy.ui import init_ui, pygame_set_cursor


class KivyApp(App):
    '''Application class'''

    def build(self):
        EventLoop.ensure_window()
        EventLoop.window.title = self.title = 'Rockivy | Kivy App Contest 2014'

        if EventLoop.window.__class__.__name__.endswith('Pygame'):
            try:
                # because pygame hates nice cursors
                pygame_set_cursor()
            except:
                pass

        game = Game()
        self.on_start = game.on_start
        return init_ui(game)

if __name__ == '__main__':
    Config.set('graphics', 'width', '960')
    Config.set('graphics', 'height', '540')  # 16:9
    Config.set('graphics', 'resizable', '0')

    Config.set('kivy', 'window_icon', resource_find('icon.png'))

    if Game.REPLACE_CURSOR:
        Config.set('graphics', 'show_cursor', '0')

    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    from kivy.core.window import Window
    Window.clearcolor = utils.get_color_from_hex('#ffffff')

    app = KivyApp()
    app.load_config()
    app.root = app.build()
    app.built = True
    app.run()
