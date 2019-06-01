import space_objects, distance
import pyglet
from pyglet import gl

START_ASTEROIDS = 8
objects = []
keys_pressed = set()
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(1000, 600)
window_size = [window.width,window.height]

def tick_all(dt):
    for object in objects:
        object.tick(dt,objects)

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
            # for object in objects:
            #     distance.draw_circle(object.x, object.y, object.radius)

            # Restore remembered state (this cancels the glTranslatef)
            gl.glPopMatrix()

@window.event
def on_key_press(symbol, modifiers):
    keys_pressed.add(symbol)

@window.event
def on_key_release(symbol, modifiers):
    keys_pressed.remove(symbol)


player_ship = space_objects.Spaceship("PNG\playerShip1_orange.png",window_size,batch,keys_pressed, window.width // 2, window.height // 2)

objects = [player_ship]
for i in range(START_ASTEROIDS):
    objects.append(space_objects.Asteroid(window_size,batch))

pyglet.clock.schedule_interval( tick_all, 1/30)

pyglet.app.run()
