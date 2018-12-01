import pyglet
from database.database import Database
from interface.colors import Color
from interface.panels import InformationPanel

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

def update_information_panel(dt):
    current_pokemon = database[3]
    information.update(current_pokemon)

@window.event
def on_draw():
    window.clear()
    information.draw_self()

if __name__ == "__main__":
    pyglet.clock.schedule_once(update_information_panel, 3.0)
    pyglet.app.run()