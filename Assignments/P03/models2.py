from pygame.math import Vector2
from pygame import transform
import json
import time
import sys
import pygame
import random
from utils import get_random_velocity, load_sound, load_sprite, wrap_position, distance
import math
import os

from rich import print
from threading import Thread
# necessary libs for rabbitmq
from comms import CommsListener
from comms import CommsSender

UP = Vector2(0, -1)

# Color library
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Add the ships to a list
ships = ["space_ship1", "space_ship2", "space_ship3", 
         "space_ship4", "space_ship5", "space_ship6", 
         "space_ship7", "space_ship8", "space_ship9", 
         "space_ship10"]

# Animate images in a list of images
Portal1_paths = ["sprites/Portal/portal01.png", "sprites/Portal/portal02.png",
                     "sprites/Portal/portal03.png", "sprites/Portal/portal04.png",
                     "sprites/Portal/portal05.png", "sprites/Portal/portal06.png",
                     "sprites/Portal/portal07.png", "sprites/Portal/portal08.png",
                     "sprites/Portal/portal09.png", "sprites/Portal/portal10.png",
                     "sprites/Portal/portal11.png", "sprites/Portal/portal12.png",
                     "sprites/Portal/portal13.png", "sprites/Portal/portal14.png",
                     "sprites/Portal/portal15.png", "sprites/Portal/portal16.png",
                     "sprites/Portal/portal17.png", "sprites/Portal/portal18.png",
                     "sprites/Portal/portal19.png", "sprites/Portal/portal20.png",
                     "sprites/Portal/portal21.png", "sprites/Portal/portal22.png",
                     "sprites/Portal/portal23.png", "sprites/Portal/portal24.png",
                     "sprites/Portal/portal25.png", "sprites/Portal/portal26.png",
                     "sprites/Portal/portal27.png", "sprites/Portal/portal28.png",
                     "sprites/Portal/portal29.png", "sprites/Portal/portal30.png",
                     "sprites/Portal/portal31.png", "sprites/Portal/portal32.png",
                     "sprites/Portal/portal33.png", "sprites/Portal/portal34.png",
                     "sprites/Portal/portal35.png", "sprites/Portal/portal36.png",
                     "sprites/Portal/portal37.png", "sprites/Portal/portal38.png",
                     "sprites/Portal/portal39.png", "sprites/Portal/portal40.png",
                     "sprites/Portal/portal41.png", "sprites/Portal/portal42.png",
                     "sprites/Portal/portal43.png", "sprites/Portal/portal44.png",
                     "sprites/Portal/portal45.png", "sprites/Portal/portal46.png",
                     "sprites/Portal/portal47.png", "sprites/Portal/portal48.png",
                     "sprites/Portal/portal49.png", "sprites/Portal/portal50.png",
                     "sprites/Portal/portal51.png", "sprites/Portal/portal52.png",
                     "sprites/Portal/portal53.png", "sprites/Portal/portal54.png",
                     "sprites/Portal/portal55.png", "sprites/Portal/portal56.png",
                     "sprites/Portal/portal57.png", "sprites/Portal/portal58.png",
                     "sprites/Portal/portal59.png", "sprites/Portal/portal60.png",
                     "sprites/Portal/portal61.png", "sprites/Portal/portal62.png",
                     "sprites/Portal/portal63.png", "sprites/Portal/portal64.png"]

Portal2_paths = ["sprites/Portal2/portal01.png", "sprites/Portal2/portal02.png",
                    "sprites/Portal2/portal03.png", "sprites/Portal2/portal04.png",
                    "sprites/Portal2/portal05.png", "sprites/Portal2/portal06.png",
                    "sprites/Portal2/portal07.png", "sprites/Portal2/portal08.png",
                    "sprites/Portal2/portal09.png", "sprites/Portal2/portal10.png",
                    "sprites/Portal2/portal11.png", "sprites/Portal2/portal12.png",
                    "sprites/Portal2/portal13.png", "sprites/Portal2/portal14.png",
                    "sprites/Portal2/portal15.png", "sprites/Portal2/portal16.png",
                    "sprites/Portal2/portal17.png", "sprites/Portal2/portal18.png",
                    "sprites/Portal2/portal19.png", "sprites/Portal2/portal20.png",
                    "sprites/Portal2/portal21.png", "sprites/Portal2/portal22.png",
                    "sprites/Portal2/portal23.png", "sprites/Portal2/portal24.png",
                    "sprites/Portal2/portal25.png", "sprites/Portal2/portal26.png",
                    "sprites/Portal2/portal27.png", "sprites/Portal2/portal28.png",
                    "sprites/Portal2/portal29.png", "sprites/Portal2/portal30.png",
                    "sprites/Portal2/portal31.png", "sprites/Portal2/portal32.png",
                    "sprites/Portal2/portal33.png", "sprites/Portal2/portal34.png",
                    "sprites/Portal2/portal35.png", "sprites/Portal2/portal36.png",
                    "sprites/Portal2/portal37.png", "sprites/Portal2/portal38.png",
                    "sprites/Portal2/portal39.png", "sprites/Portal2/portal40.png",
                    "sprites/Portal2/portal41.png", "sprites/Portal2/portal42.png",
                    "sprites/Portal2/portal43.png", "sprites/Portal2/portal44.png",
                    "sprites/Portal2/portal45.png", "sprites/Portal2/portal46.png",
                    "sprites/Portal2/portal47.png", "sprites/Portal2/portal48.png",
                    "sprites/Portal2/portal49.png", "sprites/Portal2/portal50.png",
                    "sprites/Portal2/portal51.png", "sprites/Portal2/portal52.png",
                    "sprites/Portal2/portal53.png", "sprites/Portal2/portal54.png",
                    "sprites/Portal2/portal55.png", "sprites/Portal2/portal56.png",
                    "sprites/Portal2/portal57.png", "sprites/Portal2/portal58.png",
                    "sprites/Portal2/portal59.png", "sprites/Portal2/portal60.png",
                    "sprites/Portal2/portal61.png", "sprites/Portal2/portal62.png",
                    "sprites/Portal2/portal63.png", "sprites/Portal2/portal64.png"]

explosion_paths = ["sprites/Explosion/1.png", "sprites/Explosion/2.png",
                    "sprites/Explosion/3.png", "sprites/Explosion/4.png", 
                    "sprites/Explosion/5.png", "sprites/Explosion/6.png",
                    "sprites/Explosion/7.png", "sprites/Explosion/8.png",
                    "sprites/Explosion/9.png", "sprites/Explosion/10.png",
                    "sprites/Explosion/11.png", "sprites/Explosion/12.png",
                    "sprites/Explosion/13.png", "sprites/Explosion/14.png",
                    "sprites/Explosion/15.png", "sprites/Explosion/16.png",
                    "sprites/Explosion/17.png", "sprites/Explosion/18.png",
                    "sprites/Explosion/19.png", "sprites/Explosion/20.png",
                    "sprites/Explosion/21.png", "sprites/Explosion/22.png",
                    "sprites/Explosion/23.png", "sprites/Explosion/24.png",
                    "sprites/Explosion/25.png", "sprites/Explosion/26.png",
                    "sprites/Explosion/27.png", "sprites/Explosion/28.png",
                    "sprites/Explosion/29.png", "sprites/Explosion/30.png"]


# Choose a random bullet sprite
bullet = random.randrange(10, 66, 1)

current_image = 0
current_image_1 = 0
current_image_2 = 0

class Messenger:
    """
    - Handles messaging (sending and receiving) for each player.
    - Requires a callback to be passed in so received messages can be handled.
    """

    def __init__(self, creds, callback=None):
        self.creds = creds
        self.callBack = callback

        if not self.creds:
            print(
                "Error: Message handler needs `creds` or credentials to log into rabbitmq. "
            )
            sys.exit()

        if not self.callBack:
            print(
                "Error: Message handler needs a `callBack` function to handle responses from rabbitmq. "
            )
            sys.exit()

        # Identify the user
        self.user = self.creds["user"]

        # create instances of a comms listener and sender
        # to handle message passing.
        self.commsListener = CommsListener(**self.creds)
        self.commsSender = CommsSender(**self.creds)

        # Start the comms listener to listen for incoming messages
        self.commsListener.threadedListen(self.callBack)

    def send(self, **kwargs):
        """Sends the message to a target or broadcasts to all."""
        target = kwargs.get("target", "broadcast")
        self.commsSender.threadedSend(
            target=target, sender=self.user, body=json.dumps(kwargs), debug=False
        )

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)
        # print(f"pos: {self.position}")

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

    def collides_withPos(self, other_obj,pos):
        distance = self.position.distance_to(pos)
        return distance < self.radius + other_obj.radius


# def callback(ch, method, properties, body):
#     """This method gets run when a message is received. You can alter it to
#     do whatever is necessary.
#     """
#     #body = body.decode("utf-8")
#     print(body)

class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0
    BULLET_SPEED = 10

    def __init__(self, position, create_bullet_callback, ship = random.choice(ships), **kwargs):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("PewFire2")
        self.explode_sound = load_sound("CrashKG")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)
        self.damage = 0
        self.kills = 0
        self.speed = 5

        super().__init__(position, load_sprite(ship), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.ACCELERATION = 0.1
        if self.ACCELERATION > 1:
            self.velocity -= self.direction * self.ACCELERATION
        self.velocity += self.direction * self.ACCELERATION

    def decelerate(self):
        self.ACCELERATION = 0.1
        self.velocity -= self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = transform.rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        angle = self.direction.angle_to(UP)
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity, angle, "player")
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    def brake(self):
        self.velocity = [0, 0]

    def explode(self, screen):
        global current_image
        self.damage = 100
        current_image_path = explosion_paths[current_image]
        current_image_surface = pygame.image.load(current_image_path)
        current_image_surface = pygame.transform.scale(current_image_surface, (200, 150))
        screen.blit(current_image_surface, self.position)
        self.destroyed = True
        self.explode_sound.play()

        current_image += 1
        if current_image >= len(explosion_paths):
            current_image = 0
 

class NPC(Spaceship):
    def __init__(
        self, position, create_bullet_callback, ship=random.choice(ships), targets=[]
    ):
        self.targets = targets
        self.damage = 0
        self.speed = 0.00001
        self.image = load_sprite(ship)
        self.rect = self.image.get_rect()
        self.countShootTime = 0

        super().__init__(position, create_bullet_callback, ship)

    def choose_target(self):
        closestDistance = pow(2, 20)
        closestTarget = None
        for target in self.targets:
            d = distance(target.position, self.position)
            if distance(target.position, self.position) < closestDistance:
                closestTarget = target
                closestDistance = d

        self.target = closestTarget

    def follow_target(self):
        if self.target:
            self.direction = Vector2(self.target.position.x - self.position.x, self.target.position.y - self.position.y)
            self.direction = self.direction.normalize()
            self.velocity = Vector2(self.direction.x, self.direction.y)

    def shoot(self):
        self.countShootTime += 0.016
        if self.countShootTime >= 3 and self.target:
            self.countShootTime = 0
            angle = self.direction.angle_to(UP)
            bullet_velocity = self.direction * self.BULLET_SPEED/2 + self.velocity
            bullet = Bullet(self.position, bullet_velocity, angle, "npc")
            self.create_bullet_callback(bullet)
            self.laser_sound.play()

    def damage_bar(self, screen):
        pygame.draw.rect(screen, (red), (self.position.x - 50, self.position.y - 60, 100, 10))
        pygame.draw.rect(screen, (green), (self.position.x - 50, self.position.y - 60, 100 - self.damage, 10))
        #screen.blit(current_image, (self.position.x - 50, self.position.y - 60))

    def remove(self):
        pass


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = transform.rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)


class Bullet(GameObject):
    def __init__(self, position, velocity, angle, belongTo):
        
        super().__init__(position, load_sprite(f"{bullet}"), velocity)
        #self.sprite = pygame.transform.scale(self.sprite, (30, 30))
        self.sprite = pygame.transform.rotozoom(self.sprite, angle, 0.3)
        self.radius = self.sprite.get_width() / 2
        # self.id = id
        self.belongTo = belongTo
        
    def move(self, surface):
        self.position = self.position + self.velocity


class Wormhole1(GameObject):

    def __init__(self,  screen, image_paths = Portal1_paths):
        # Load images as surfaces
        images = [pygame.image.load(path).convert_alpha() for path in image_paths]

        # Create sprite object and set initial image
        sprite = pygame.sprite.Sprite()
        sprite.image = images[0]
        sprite.rect = sprite.image.get_rect()
        self.countRandTime = 0
        self.countAvailableTime = 0
        self.available = True


        self.screen = screen
        
        self.pos1 = Vector2(random.randrange(0, 400), random.randrange(0, 450))

        self.radius = 40

        # Call the superclass constructor
        # for i in range(0, 64):
        # wormhole = images[i]
        # wormhole = pygame.transform.scale(wormhole, (200, 150))
        # screen.blit(wormhole, position)

    def drawHole(self, pos):
        global current_image_1
        current_image_path = Portal1_paths[current_image_1]
        current_image_surface = pygame.image.load(current_image_path)
        current_image_surface = pygame.transform.scale(current_image_surface, (200, 150))
        blitPos = pos - Vector2(self.radius)
        self.screen.blit(current_image_surface,blitPos)


        current_image_1 += 1
        if current_image_1 >= len(Portal1_paths):
            current_image_1 = 0

    def randomPos(self):
        self.countRandTime = 0
        self.pos1 = Vector2(random.randrange(0, 800 - 400), random.randrange(0, 600 - 150))

    def update(self):
        if not self.available:
            self.countAvailableTime += 0.016
            if self.countAvailableTime >= 3:
                self.countAvailableTime = 0
                self.available = True
                self.randomPos()

        self.countRandTime += 0.016
        if self.countRandTime >= 10:
            self.randomPos()

    def draw(self, surface):
        if self.available:
            self.drawHole(self.pos1)


        # pass
    

class Wormhole2(GameObject):

    def __init__(self,  screen, image_paths = Portal2_paths):
        # Load images as surfaces
        images = [pygame.image.load(path).convert_alpha() for path in image_paths]

        # Create sprite object and set initial image
        sprite = pygame.sprite.Sprite()
        sprite.image = images[0]
        sprite.rect = sprite.image.get_rect()
        self.countRandTime = 0
        self.countAvailableTime = 0
        self.available = True


        self.screen = screen
        
        self.pos2 = Vector2(random.randrange(400, 600), random.randrange(0, 450))

        self.radius = 40

        # Call the superclass constructor
        # for i in range(0, 64):
        # wormhole = images[i]
        # wormhole = pygame.transform.scale(wormhole, (200, 150))
        # screen.blit(wormhole, position)

    def drawHole(self, pos):
        global current_image_2
        current_image_path = Portal2_paths[current_image_2]
        current_image_surface = pygame.image.load(current_image_path)
        current_image_surface = pygame.transform.scale(current_image_surface, (200, 150))
        blitPos = pos - Vector2(self.radius)
        self.screen.blit(current_image_surface,blitPos)


        current_image_2 += 1
        if current_image_2 >= len(Portal2_paths):
            current_image_2 = 0

    def randomPos(self):
        self.countRandTime = 0
        self.pos2 = Vector2(random.randrange(400, 800 - 200), random.randrange(0, 600 - 150))

    def update(self):
        if not self.available:
            self.countAvailableTime += 0.016
            if self.countAvailableTime >= 5:
                self.countAvailableTime = 0
                self.available = True
                self.randomPos()

        self.countRandTime += 0.016
        if self.countRandTime >= 10:
            self.randomPos()



    def draw(self, surface):
        if self.available:
            self.drawHole(self.pos2)


        # pass


class Damage_bar():
    def __init__(self, surface):
        super().__init__()
        self.damage_bar_width = 0
        self.damage_bar_height = 10
        self.font = pygame.font.SysFont("Arial", 15)
        self.surface = surface
        
    def update(self, damage, kills):
        width = self.damage_bar_width + damage
        pygame.draw.rect(self.surface, red, (10, 28, width, self.damage_bar_height))
        pygame.draw.rect(self.surface, white, (10, 28, 100, self.damage_bar_height), 2)
        damage_text = self.font.render("Damage" , True, white)
        kills_text = self.font.render("Kills: {}".format(kills), True, white)
        self.surface.blit(damage_text, (10, 5))
        self.surface.blit(kills_text, (10, 40))
        pygame.display.update()


class Explosion(GameObject):
    
    def __init__(self, position, screen, targets=[], explode_paths = explosion_paths):
        
        # Load images as surfaces
        images = [pygame.image.load(path).convert_alpha() for path in explode_paths]

        # Create sprite object and set initial image
        sprite = pygame.sprite.Sprite()
        sprite.image = images[0]
        sprite.rect = sprite.image.get_rect()

        self.targets = targets
        self.screen = screen
        self.position = position
        # Call the superclass constructor
        #for i in range(0, 64):
            #wormhole = images[i]
            #wormhole = pygame.transform.scale(wormhole, (200, 150))
            #screen.blit(wormhole, position)


    def update(self, pos):
        global current_image_2
        current_image_path = explosion_paths[current_image_2]
        current_image_surface = pygame.image.load(current_image_path)
        current_image_surface = pygame.transform.scale(current_image_surface, (200, 150))
        self.screen.blit(current_image_surface, pos)

        current_image_2 += 1
        if current_image_2 >= len(explosion_paths):
            current_image_2 = 0


class Barrel(GameObject):
    def __init__(self, position, create_barrel_callback, size=3):
        self.create_barrel_callback = create_barrel_callback
        self.size = size

        size_to_scale = {3: 0.01, 2: 0.001, 1: 0.0005}
        scale = size_to_scale[size]
        sprite = transform.rotozoom(load_sprite("Barrel"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 2))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                barrel = Barrel(
                    self.position, self.create_barrel_callback, self.size - 1
                )
                self.create_barrel_callback(barrel)