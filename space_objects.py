import pyglet, math
from pyglet.window import key

ROTATION_SPEED = 90  # radians per second
ACCELERATION = 100

class Spaceship():
    def __init__(self,image_path, x = 0, y = 0, rotation = 0 ):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = rotation
        self.image_path = image_path

    def load_sprite(self,batch):
        image = pyglet.image.load(self.image_path)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        self.sprite = pyglet.sprite.Sprite(image, batch=batch)

    def tick(self,dt,window_size,keys_pressed):
        rotation_speed = 0

        # Adjust speed and rotation based on keys pressed
        if key.LEFT in keys_pressed:
            rotation_speed = ROTATION_SPEED * dt
        if key.RIGHT in keys_pressed:
            rotation_speed = ROTATION_SPEED * -dt
        if key.UP in keys_pressed:
            self.x_speed += dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed += dt * ACCELERATION * math.sin(self.rotation)

        # Movement and rotation of object and its sprite
        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed
        self.rotation = self.rotation + dt * rotation_speed
        self.sprite.rotation = 90 - math.degrees(self.rotation)
        self.sprite.x = self.x
        self.sprite.y = self.y

        # Object leaving the window appears on the other side
        if self.x < 0:
            self.x = self.x + window_size[0]
        if self.x > window_size[0]:
            self.x = self.x - window_size[0]
        if self.y < 0:
            self.y = self.y + window_size[1]
        if self.y > window_size[1]:
            self.y = self.y - window_size[1]
