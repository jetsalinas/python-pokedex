import pyglet
from database.database import Database
from helpers.colors import Color

# Get database
database = Database()

# Initialize windows
window = pyglet.window.Window(caption='Pokedex V1.0', width=800, height=600)

# Set blending modes
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

@window.event
def on_draw():
    window.clear()

if __name__ == "__main__":
    # pyglet.app.run()
    print(database.first().name)