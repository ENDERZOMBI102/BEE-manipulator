import pyglet

window = pyglet.window.Window()

@window.event
def on_key_press(symbol, modifiers):
    print('key {symbol} was pressed'.format(symbol = modifiers))

@window.event
def on_draw():
    window.clear()

pyglet.app.run()