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
window = pyglet.window.Window(caption='Pokedex V1.0', width=640, height=480)

# Set blending modes
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

information = InformationPanel(database.index(current_pokemon))
browser = Browser(database, favorites, x=information.width+30, y=window.height-90)
search_panel = SearchPanel(database, x=information.width+30, y=window.height+15)
scroll_bar = ScrollBar(database, window.height-80, 10, window.width-30, window.width-20)

previous_stats = information.current_stats
scroll_state   = False

def update_hexagon(dt):
    global previous_stats
    previous_stats = vertex_change(previous_stats, information.current_stats)

def update_information_panel(dt):
    information.update(database[0])

@window.event
def on_key_press(symbol, mod):
    global database, browser, previous_stat
    key_shifts = {key.DOWN: 1, key.UP: -1, key.RIGHT: 10, key.LEFT: -10, key.PAGEDOWN: 50, key.PAGEUP: -50}
    if symbol in key_shifts:
        current_pokemon = browser.update_data(key_shifts[symbol])
        information.update(database.index(current_pokemon))
        scroll_bar.update_from_key(browser.top)
    elif symbol == key.SPACE:
        browser.update_favs()
    elif symbol == key.BACKSPACE:
        search_panel.handle_backspace()
    elif symbol == key.ENTER:
        database = search_panel.handle_enter()
        current_pokemon = database.first().index
        information.update(database.first())
        browser.update_database(database)
    elif str.isalpha(chr(symbol)):
        search_panel.handle_char(chr(symbol))

@window.event
def on_mouse_scroll(x, y, dx, dy):
    current_pokemon = browser.update_data(int(-dy))
    information.update(database.index(current_pokemon))
    scroll_bar.update_from_key(browser.top)

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifier):
    global scroll_state
    if scroll_bar.bar.x - scroll_bar.bar.width/2 <= x <= scroll_bar.bar.x + scroll_bar.bar.width/2:
        if scroll_bar.bar.y - scroll_bar.bar.height/2 <= y <= scroll_bar.bar.y + scroll_bar.bar.height/2:
            scroll_state = True
    if scroll_state:
        check = int(scroll_bar.bar.y + dy)
        if  scroll_bar.minimum < check < scroll_bar.maximum:
            scroll_bar.update_from_scroll(dy)
            shift = int(len(database)-(dy*scroll_bar.ratio)) #Specifically this line Jose
            current_pokemon = browser.update_data(shift)     #if it goes below 0, currrent_pokemon
            information.update(database.index(current_pokemon)) #goes over 900.

@window.event
def on_mouse_release(x, y, button, modifier):
    global scroll_state
    if scroll_state: scroll_state = False

@window.event
def on_draw():
    window.clear()
    information.draw_self()
    browser.draw_self()
    search_panel.draw_self()
    scroll_bar.draw_self()
    vertices = [information.hexagon_sprite.x, information.hexagon_sprite.y] + previous_stats
    pyglet.graphics.draw_indexed(7, pyglet.gl.GL_TRIANGLES,
                            [0, 6, 1, 0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6],
                            ('v2f', tuple(vertices)), ('c4B', (Color.WHITE + tuple([150])) * 7))
    pyglet.graphics.draw(6, pyglet.gl.GL_LINE_LOOP, ('v2f', previous_stats), ('c3B', (Color.BLACK* 6)))

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update_hexagon, 1/120.0)
    pyglet.app.run()
