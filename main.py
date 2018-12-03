import pyglet
from pyglet.window import key
from database.database import Database
from interface.colors import Color
from interface.panels import InformationPanel, Browser

# Get resources
database = Database()
current_pokemon = database.first()
pyglet.font.add_file("resources/fonts/pkmndp.ttf")

# Initialize windows
window = pyglet.window.Window(caption='Pokedex V1.0', width=640, height=480)

# Set blending modes
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

information = InformationPanel(current_pokemon)
browser = Browser(database, x=information.width+30, y=window.height-90)

def update_information_panel(dt):
    information.update(current_pokemon)

@window.event
def on_key_press(symbol, mod):
    key_shifts = {key.DOWN: 1, key.UP: -1, key.RIGHT: 10, key.LEFT: -10, key.PAGEDOWN: 50, key.PAGEUP: -50}
    if symbol in key_shifts:
        browser.update_data(key_shifts[symbol])

@window.event
def on_draw():
    window.clear()
    information.draw_self()
    browser.draw_self()

if __name__ == "__main__":
    pyglet.app.run()