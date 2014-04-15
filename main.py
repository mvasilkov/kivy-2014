import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config

from game import Game


class KivyApp(App):
    '''Application class'''

    def build(self):
        EventLoop.ensure_window()
        EventLoop.window.title = self.title = 'Kivy App Contest 2014'
        return Game()

if __name__ == '__main__':
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    KivyApp().run()
