# Modules
import pygame
import math
import logging
from pygame.constants import *

# Scripts
from scripts.framework import get_center, collision_test, numCap
from scripts.input import Controller, Keyboard
from scripts.animation import Animation
from scripts.camera import Camera

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos:tuple[int, int], size:tuple[int, int], tag:str, assets:dict[str, Animation], layer=0):
        super().__init__()
        # parameters
        self.pos = pygame.math.Vector2(pos)
        self.size = size
        self.tag = tag
        self.assets = assets
        self._layer = layer

        # movement
        self.flip = False
        self.directions: dict[str, bool] = {"left" : False, "right": False, "up": False, "down": False}
        self.movement = pygame.math.Vector2() # [x, y]
        
        # animation
        self.action: str = ""
        self.anim_offset: tuple[int, int] = (0, 0)
        self.set_action("idle")
        
        self.rect: pygame.Rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])

    @property
    def x(self):
        return self.pos.x
    
    @property
    def y(self):
        return self.pos.y
    
    @property
    def width(self):
        return self.size[1]
    
    @property
    def height(self):
        return self.size[1]
    
    @property
    def image(self):
        return pygame.transform.flip(self.animation.img(), self.flip, False)
    
    # Sets an animation action
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.assets[self.tag + "/" + self.action].copy()

    # Updates the current frame of an animation
    def update_animation(self, dt):
        self.animation.update(dt)

    # Gets the center
    def get_center(self):
        x = self.pos.x - (self.width // 2)
        y = self.pos.y - (self.height // 2)
        return [x, y]
    
    # Gets the angle between 2 entities
    def get_entity_angle(self, entity_2):
        x1 = self.pos.x + int(self.width / 2)
        y1 = self.pos.y + int(self.height / 2)
        x2 = entity_2.x + int(entity_2.width / 2)
        y2 = entity_2.y + int(entity_2.height / 2)
        angle = math.atan((y2-y1) / (x2-x1))
        if x2 < x1:
            angle += math.pi
        return angle
    
    # Gets the angle between an entity and a point
    def get_point_angle(self, point, scroll=[0, 0], offset=0, centered=True):
        pos = [self.pos.x - scroll[0], self.pos.y - scroll[1]]
        if centered:
            pos = get_center(pos, self.size)
        radians = math.atan2(point[1] - pos[1], point[0] - pos[0])
        return -math.degrees(radians) + offset
    
    # Gets the distance between an entity and a point
    def get_distance(self, point):
        dis_x = point[0] - self.get_center()[0]
        dis_y = point[1] - self.get_center()[1]
        return math.sqrt(dis_x ** 2 + dis_y ** 2)
    
class PhysicsEntity(Entity):
    def __init__(self, pos:tuple[int, int], size:tuple[int, int], tag:str, assets:dict[str, Animation], layer=0):
        # Parameters
        super().__init__(pos, size, tag, assets, layer)
        # Rects and Collisions
        self.collisions: dict[str, bool] = {'bottom': False, 'top': False, 'left': False, 'right': False}

    # Checks for collisions based on movement direction
    def move(self, movement, tiles, dt):
        # x-axis
        self.pos.x += movement[0] * dt
        self.rect.x = int(self.pos.x)
        tileCollisions = collision_test(self.rect, tiles)
        objectCollisions = {'bottom': False, 'top': False, 'left': False, 'right': False}
        for tile in tileCollisions:
            if movement[0] > 0:
                self.rect.right = tile.left
                objectCollisions["right"] = True
            elif movement[0] < 0:
                self.rect.left = tile.right
                objectCollisions["left"] = True
        self.pos.x = self.rect.x

        # y-axis
        self.pos.y += movement[1] * dt
        self.rect.y = int(self.pos.y)
        tileCollisions = collision_test(self.rect, tiles)
        for tile in tileCollisions:
            if movement[1] > 0:
                self.rect.bottom = tile.top
                objectCollisions["bottom"] = True
            elif movement[1] < 0:
                self.rect.top = tile.bottom
                objectCollisions["top"] = True
        self.pos.y = self.rect.y
        self.collisions = objectCollisions


class Player(PhysicsEntity):
    def __init__(self, id:int, pos:tuple[int, int], size:tuple[int, int], tag:str, assets:dict[str, Animation], layer=0):
        super().__init__(pos, size, tag, assets, layer)
        self.id = id
        self.speed = 0
        self.cursor = UserCursor(pygame.mouse.get_pos(), [9, 9], "cursor1", assets)
        self.weapon = None
        self.directions = {"up": False, "down": False, "left": False, "right": False}
        self.input = None

    def input_events(self, event):
        if self.input is not None:
            if isinstance(self.input, Controller):
                self.controller_input(event)
            else:
                self.keyboard_input(event)

    def keyboard_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.input.controls.moveLeft:
                self.directions["left"] = True
            if event.key == self.input.controls.moveRight:
                self.directions["right"] = True

            if event.key == self.input.controls.moveUp:
                self.directions["up"] = True
            if event.key == self.input.controls.moveDown:
                self.directions["down"] = True

        elif event.type == pygame.KEYUP:
            if event.key == self.input.controls.moveLeft:
                self.directions["left"] = False
            if event.key == self.input.controls.moveRight:
                self.directions["right"] = False
            if event.key == self.input.controls.moveUp:
                self.directions["up"] = False
            if event.key == self.input.controls.moveDown:
                self.directions["down"] = False

    def controller_input(self, event):
        if self.input.leftStick.x > 0:
            self.directions["right"] = True
            self.directions["left"] = False
        elif self.input.leftStick.x < 0:
            self.directions["left"] = True
            self.directions["right"] = False
        else:
            self.directions["left"] = False
            self.directions["right"] = False

        if self.input.leftStick.y > 0:
            self.directions["down"] = True
            self.directions["up"] = False
        elif self.input.leftStick.y < 0:
            self.directions["up"] = True
            self.directions["down"] = False
        else:
            self.directions["down"] = False
            self.directions["up"] = False

    def update(self, tiles, dt, camera):
        if self.directions["left"]:
            self.movement.x = -1
            self.flip = True
        elif self.directions["right"]:
            self.movement.x = 1
            self.flip = False
        else:
            self.movement.x = 0

        if self.directions["up"]:
            self.movement.y = -1
        elif self.directions["down"]:
            self.movement.y = 1
        else:
            self.movement.y = 0

        if self.movement.length() > 0:
            self.movement.normalize()

        self.move(self.movement, tiles, dt)
        self.update_animation(dt)
        if self.input:
            self.input.update()

class UserCursor(Entity):
    def __init__(self, pos, size, tag, assets):
        super().__init__(pos, size, tag, assets)
        self.location = [1, 1]

    def set_pos(self, x, y):
        self.pos[0] = x
        self.pos[1] = y

    def update(self, player:Player, camera:Camera):
        x = self.pos[0]
        y = self.pos[1]
        if isinstance(player.input, Controller):
            x += round(player.input.rightStick[0] * 5)
            y += round(player.input.rightStick[1] * 5)
            self.pos[0] = self.pos[0]
            self.pos[1] = self.pos[1] 
            self.set_pos(x, y)
        else:
            x, y = pygame.mouse.get_pos()
            self.set_pos(x, y)
        self.cursor_in_space(camera.scale)

    def cursor_in_space(self, camera_scale):
        self.location[0] = self.pos[0] // camera_scale
        self.location[1] = self.pos[1] // camera_scale