import pyglet, math
from pyglet.window import key
from random import choice, randrange
import glob
from pyglet import gl
from distance import distance, overlaps


ROTATION_SPEED = 90  # radians per second
ACCELERATION = 100
ASTEROIDS_PATH = "PNG\\Meteors\\"
ASTEROID_MAX_SPEED = 50
ASTEROID_MAX_ROTATION = 5
LASER_PATH = "PNG\Lasers\laserBlue06.png"
LASER_MIN_SPEED = 50

class SpaceObject():
    def __init__(self,image_path, window_size, batch, x = 0, y = 0, rotation = 0  ):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = rotation
        self.image_path = image_path
        self.window_size =  window_size
        self.load_sprite(batch)
        self.batch = batch

    def load_sprite(self,batch):
        image = pyglet.image.load(self.image_path)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        self.radius = (image.width + image.height)/4
        self.sprite = pyglet.sprite.Sprite(image, batch=batch)

    def tick(self,dt,objects):
        # Movement and rotation of object and its sprite
        self.x = self.x + dt * self.x_speed
        self.y = self.y + dt * self.y_speed
        self.sprite.rotation = 90 - math.degrees(self.rotation)
        self.sprite.x = self.x
        self.sprite.y = self.y

        # Object leaving the window appears on the other side
        if self.x < 0:
            self.x = self.x + self.window_size[0]
        if self.x > self.window_size[0]:
            self.x = self.x - self.window_size[0]
        if self.y < 0:
            self.y = self.y + self.window_size[1]
        if self.y > self.window_size[1]:
            self.y = self.y - self.window_size[1]

    def delete_object(self,objects):
        self.sprite.delete()
        objects.remove(self)

    def hit_by_spaceship(self,spaceship,objects):
        pass

    def hit_by_laser(self,laser,objects):
        pass

class Spaceship(SpaceObject):
    def __init__(self, image_path,window_size,batch, keys_pressed,x = 0, y = 0, rotation = 0  ):
        super().__init__(image_path,window_size,batch,x, y, rotation)
        self.keys_pressed = keys_pressed
        self.time_till_shoot = 0.3

    def tick(self,dt,objects):
        rotation_speed = 0
        # Adjust speed and rotation based on keys pressed
        if key.LEFT in self.keys_pressed:
            rotation_speed = ROTATION_SPEED * dt
        if key.RIGHT in self.keys_pressed:
            rotation_speed = ROTATION_SPEED * -dt
        if key.UP in self.keys_pressed:
            self.x_speed += dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed += dt * ACCELERATION * math.sin(self.rotation)

        self.rotation = self.rotation + dt * rotation_speed
        self.time_till_shoot -= dt

        super().tick(dt,objects)

        for object in objects:
            if overlaps(self,object,self.window_size):
                object.hit_by_spaceship(self,objects)
        if key.SPACE in self.keys_pressed:
            if self.time_till_shoot<0:
                objects.append(Laser(self.window_size,self.batch, self.x, self.y, self.rotation, self.x_speed, self.y_speed))
                self.time_till_shoot = 0.3

class Asteroid(SpaceObject):
    def __init__(self, window_size, batch):
        side = choice([0,1])
        if side==0:
            x = 0
            y = randrange(1,window_size[1])
        else:
            x = randrange(1,window_size[0])
            y = 0
        rotation = randrange(0,360)
        super().__init__(choice(glob.glob(ASTEROIDS_PATH + "*.png")),window_size,batch,x,y,rotation)
        self.x_speed = randrange(0,ASTEROID_MAX_SPEED)
        self.y_speed = randrange(0,ASTEROID_MAX_SPEED)

    def tick(self,dt,objects):
        rotation_speed = randrange(0,ASTEROID_MAX_ROTATION)
        self.rotation = self.rotation + dt * rotation_speed
        super().tick(dt,objects)

    def hit_by_spaceship(self,spaceship,objects):
        spaceship.delete_object(objects)

    def hit_by_laser(self,laser,objects):
        self.delete_object(objects)
        laser.delete_object(objects)

class Laser(SpaceObject):
    def __init__(self, window_size, batch,x, y, rotation, x_speed, y_speed ):
        image_path = LASER_PATH
        super().__init__(image_path, window_size, batch, x, y, rotation )
        speed = math.sqrt(x_speed**2+y_speed**2)
        if speed<LASER_MIN_SPEED:
            speed = LASER_MIN_SPEED
        else:
            speed = speed * 2
        self.x_speed = speed * math.cos(self.rotation)
        self.y_speed = speed * math.sin(self.rotation)
        self.lifetime = max(window_size)/(speed + LASER_MIN_SPEED)

    def tick(self,dt,objects):
        self.lifetime -= dt
        super().tick(dt,objects)
        for object in objects:
            if overlaps(self,object,self.window_size):
                object.hit_by_laser(self,objects)
        if self.lifetime<0:
            self.delete_object(objects)
