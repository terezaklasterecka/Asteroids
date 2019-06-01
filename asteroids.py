import space_objects
import pyglet,math
from pyglet import gl
START_ASTEROIDS = 8
objects = []
keys_pressed = set()
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(1000, 600)
window_size = [window.width,window.height]

def draw_circle(x, y, radius):
    iterations = 20
    s = math.sin(2*math.pi / iterations)
    c = math.cos(2*math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    gl.glColor3d(255,0,0)
    for i in range(iterations+1):
        gl.glVertex2f(x+dx, y+dy)
        dx, dy = (dx*c - dy*s), (dy*c + dx*s)
    gl.glEnd()

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
            for object in objects:
                draw_circle(object.x, object.y, object.radius)

            # Restore remembered state (this cancels the glTranslatef)
            gl.glPopMatrix()

@window.event
def on_key_press(symbol, modifiers):
    keys_pressed.add(symbol)

@window.event
def on_key_release(symbol, modifiers):
    keys_pressed.remove(symbol)


player_ship = space_objects.Spaceship("PNG\playerShip1_orange.png",window_size,keys_pressed, window.width // 2, window.height // 2)

objects = [player_ship]
for i in range(START_ASTEROIDS):
    objects.append(space_objects.Asteroid(window_size))

for object in objects:
    object.load_sprite(batch)

pyglet.clock.schedule_interval( tick_all, 1/30)

pyglet.app.run()

# pyglet.clock.schedule_once(player_ship.delete(objects), 10)
