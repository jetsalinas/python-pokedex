import pyglet
from database.database import Database
from interface.colors import Color
from interface.panels import InformationPanel

# Get database
database = Database()

# Initialize windows
window = pyglet.window.Window(caption='Pokedex V1.0', width=640, height=480)

# Set blending modes
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

information = InformationPanel(database[3])

@window.event
def on_draw():
    window.clear()
    information.draw_self()

if __name__ == "__main__":
    pyglet.app.run()