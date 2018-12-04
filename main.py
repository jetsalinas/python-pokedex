"""
Main file for python-pokedex

:Author:    Daniel Montecastro
:Author:    Jose Enrico Salinas
:Version:   20181204
"""

import pyglet
from pyglet.window import key
from interface.processes import vertex_change
from database.database import Database
from database.fav import Favorites
from interface.colors import Color
from interface.panels import InformationPanel, Browser, SearchPanel, ScrollBar

# Get resources
database = Database()
favorites = Favorites()
current_pokemon = 0
pyglet.font.add_file("resources/fonts/pkmndp.ttf")
icon   = pyglet.image.load("resources/tiles/icon.png")
cursor = pyglet.image.load("resources/tiles/cursor.png")

# Load music
try:
    music = pyglet.resource.media("resources/media/music.mp3")
    looper = pyglet.media.SourceGroup(music.audio_format, None)
    looper.loop = True
    looper.queue(music)
    player = pyglet.media.Player()
    player.queue(looper)
    player.play()
except pyglet.media.sources.riff.WAVEFormatException:
    pass

# Initialize windows
window = pyglet.window.Window(caption='Pokedex V1.0', width=640, height=480, icon=icon)
window.set_mouse_cursor(cursor)

# Set blending modes
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

# Load gui panels
information = InformationPanel(database.index(current_pokemon))
browser = Browser(database, favorites, x=information.width+30, y=window.height-90)
search_panel = SearchPanel(database, x=information.width, y=window.height-60, window=window)
scroll_bar = ScrollBar(database, window.height-80, 10, window.width-30, window.width-20)

# Initialize states
previous_stats = information.current_stats
scroll_state   = False

def update_hexagon(dt):
    """
    Utility function to update pokemon stats hexagon
    """
    global previous_stats
    previous_stats = vertex_change(previous_stats, information.current_stats)

@window.event
def on_key_press(symbol, mod):
    """
    Event handler function for keyboard input
    """
    global database, browser, previous_stat

    key_shifts = {key.DOWN: 1, key.UP: -1, key.RIGHT: 10, key.LEFT: -10, key.PAGEDOWN: 50, key.PAGEUP: -50}
    if symbol in key_shifts:
        # Select a new pokemon
        current_pokemon = browser.update_data(key_shifts[symbol])
        information.update(database.index(current_pokemon))
        scroll_bar.update_from_key(browser.top)
    elif symbol == key.SPACE:
        # Toggle favorite on currently selected pokemon
        browser.update_favs()
    elif symbol == key.BACKSPACE:
        # Remove last character from search input string
        search_panel.handle_backspace()
    elif symbol == key.ENTER:
        # Toggle search function and update panels
        database = search_panel.handle_enter()
        current_pokemon = database.first().index
        information.update(database.first())
        browser.update_database(database)
    elif str.isalpha(chr(symbol)):
        # Append search input string
        search_panel.handle_char(chr(symbol))

@window.event
def on_mouse_scroll(x, y, dx, dy):
    """
    Event handler function for mouse scrolling
    """
    current_pokemon = browser.update_data(int(-dy))
    information.update(database.index(current_pokemon))
    scroll_bar.update(browser.top)

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifier):
    """
    Event handler function for mouse dragging on scroll bar
    Updates the browser view and information view to new pokemon
    """
    global scroll_state
    if scroll_bar.bar.x - scroll_bar.bar.width/2 <= x <= scroll_bar.bar.x + scroll_bar.bar.width/2:
        if scroll_bar.bar.y - scroll_bar.bar.height/2 <= y <= scroll_bar.bar.y + scroll_bar.bar.height/2:
            scroll_state = True
    if scroll_state:
        if scroll_bar.minimum <= scroll_bar.bar.y + int(dy) <= scroll_bar.maximum:
            shift = int(len(database)-(dy*scroll_bar.ratio))
        elif scroll_bar.bar.y + int(dy) > scroll_bar.maximum or scroll_bar.bar.y + int(dy) < scroll_bar.minimum:
            shift = 0
        current_pokemon = browser.update_data(shift)
        information.update(database.index(current_pokemon))
        scroll_bar.update(browser.top)

@window.event
def on_mouse_release(x, y, button, modifier):
    """
    Event handler function for mouse dragging on scroll bar
    Sets scrolling to false on release
    """
    global scroll_state
    if scroll_state: scroll_state = False

@window.event
def on_draw():
    """
    Redraws the view periodically
    """
    window.clear()
    information.draw_self()
    browser.draw_self()
    search_panel.draw_self()
    scroll_bar.draw_self()

    # Draw the pokemon stats hexagon
    vertices = [information.hexagon_sprite.x, information.hexagon_sprite.y] + previous_stats
    pyglet.graphics.draw_indexed(7, pyglet.gl.GL_TRIANGLES,
                            [0, 6, 1, 0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6],
                            ('v2f', tuple(vertices)), ('c4B', (Color.WHITE + tuple([150])) * 7))
    pyglet.graphics.draw(6, pyglet.gl.GL_LINE_LOOP, ('v2f', previous_stats), ('c3B', (Color.BLACK* 6)))

if __name__ == "__main__":
    # Set view to update periodically
    pyglet.clock.schedule_interval(update_hexagon, 1/120.0)
    pyglet.app.run()
