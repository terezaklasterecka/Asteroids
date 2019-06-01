import space_objects
import pyglet
from pyglet import gl

objects = []
keys_pressed = set()
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(1000, 600)

@window.event()
def on_draw():
    window.clear()

    for x_offset in (-window.width, 0, window.width):
        for y_offset in (-window.height, 0, window.height):
            # Remember the current state
            gl.glPushMatrix()
            # Move everything drawn from now on by (x_offset, y_offset, 0)
            gl.glTranslatef(x_offset, y_offset, 0)

            # Draw
            batch.draw()

            # Restore remembered state (this cancels the glTranslatef)
            gl.glPopMatrix()

@window.event
def on_key_press(symbol, modifiers):
    keys_pressed.add(symbol)

@window.event
def on_key_release(symbol, modifiers):
    keys_pressed.remove(symbol)

player_ship1 = space_objects.Spaceship("PNG\playerShip1_orange.png", window.width // 2, window.height // 2)
player_ship2 = space_objects.Spaceship("PNG\playerShip1_green.png",50, 50, 90)
player_ship3 = space_objects.Spaceship("PNG\playerShip1_red.png",150, 150, 120)
objects = [player_ship1, player_ship2, player_ship3]

for object in objects:
    object.load_sprite(batch)
    pyglet.clock.schedule_interval( object.tick, 1/30, keys_pressed=keys_pressed, window_size = (window.width,window.height) )

pyglet.app.run()
