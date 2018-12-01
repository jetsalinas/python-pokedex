import pyglet

# Initialize windows
window = pyglet.window.Window(caption='Pokedex V1.0', width=800, height=600)

# Set blending modes
pyglet.gl.glEnable(p.gl.GL_BLEND)
pyglet.gl.glBlendFunc(p.gl.GL_SRC_ALPHA, p.gl.GL_ONE_MINUS_SRC_ALPHA)


@window.event
def on_draw():
    window.clear()

if __name__ == "__main__":
    pyglet.app.run()