from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

from .radiobtn import Radio
from .scales import SCALES
from .tuning import NOTES, TUNING

PADDING = 4
HEIGHT = 40
HEADING_COLOR = get_color_from_hex('#4b4d49')
LABEL_COLOR = get_color_from_hex('#2e3436')
LABEL_SIZE = 110


def _heading(game, view):
    heading = Label(font_name='DroidSans-Regular.ttf', font_size=18,
                    color=HEADING_COLOR, markup=False)
    heading.pos = (PADDING, 500 - PADDING)
    heading.size = (960 - PADDING * 2, HEIGHT)
    view.add_widget(heading)

    game._heading = heading
    game.update_heading()


def _add_widgets(view, label, widgets, line, size):
    y = line * HEIGHT + (line + 1) * PADDING

    label.pos = (PADDING, y)
    label.size = (LABEL_SIZE, HEIGHT)
    view.add_widget(label)

    for i, w in enumerate(widgets):
        w.pos = (LABEL_SIZE + i * size + (i + 1) * PADDING, y)
        w.size = (size, HEIGHT)
        view.add_widget(w)


def _notes(game, view):
    label = Label(text='Root Note', color=LABEL_COLOR, markup=False)
    widgets = []

    def state_change(btn, state):
        if state == 'down':
            game.set_root_note(btn.rel)

    for i, note in enumerate(NOTES):
        kwargs = {
            'text': note.replace('#', u'\u266f'),
            'group': 'notes',
            'rel': note,
        }

        if not i:
            kwargs['state'] = 'down'

        btn = Radio(**kwargs)
        btn.bind(state=state_change)
        widgets.append(btn)

    _add_widgets(view, label, widgets, 2, 50)


def _scales(game, view):
    label = Label(text='Scale', color=LABEL_COLOR, markup=False)
    widgets = []

    def state_change(btn, state):
        if state == 'down':
            game.set_scale_class(btn.rel)

    for i, seq in enumerate(SCALES):
        kwargs = {
            'text': seq.name,
            'group': 'seq',
            'rel': seq,
        }

        if not i:
            kwargs['state'] = 'down'

        btn = Radio(**kwargs)
        btn.bind(state=state_change)
        widgets.append(btn)

    _add_widgets(view, label, widgets, 1, 140)


def _tuning(game, view):
    label = Label(text='Tuning', color=LABEL_COLOR, markup=False)
    widgets = []

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
        widgets.append(btn)

    _add_widgets(view, label, widgets, 0, 110)


def init_ui(game):
    view = Widget()

    _heading(game, view)
    _notes(game, view)
    _scales(game, view)
    _tuning(game, view)

    view.add_widget(game)
    return view

CURSOR = (
    '@                       ',
    '@@                      ',
    '@-@                     ',
    '@--@                    ',
    '@---@                   ',
    '@----@                  ',
    '@-----@                 ',
    '@------@                ',
    '@-------@               ',
    '@--------@              ',
    '@---------@             ',
    '@----------@            ',
    '@------@@@@@            ',
    '@---@--@                ',
    '@--@ @--@               ',
    '@-@  @--@               ',
    '@@    @--@              ',
    '      @--@              ',
    '       @@               ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
    '                        ',
)


def pygame_set_cursor():
    from platform import system
    from pygame import cursors, mouse

    kwargs = dict(black='@', white='-', xor='$')

    if system() == 'Windows':
        # https://bitbucket.org/pygame/pygame/issue/200
        kwargs['black'], kwargs['white'] = kwargs['white'], kwargs['black']

    a, b = cursors.compile(CURSOR, **kwargs)
    mouse.set_cursor((24, 24), (0, 0), a, b)
