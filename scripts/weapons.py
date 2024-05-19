# Modules
import pygame
import math
import logging
from pygame.constants import *

# Scripts
from scripts.entities import Entity, ModifiedSpriteGroup, PhysicsEntity
from scripts.animation import Animation
from scripts.framework import blit_rotate

logger = logging.getLogger(__name__)

class Weapon(Entity):
    def __init__(self, transform, size, tag, assets, camLayer=3, isScroll=True, animation="idle", pivot=(0, 0), rotationOffset=0):
        super().__init__(transform, size, tag, assets, camLayer, isScroll, animation)#
        self.pivot = pygame.math.Vector2(pivot)
        self.rotationOffset = rotationOffset
        self.rotation = 0

    @property
    def image(self):
        img = pygame.transform.flip(self.animation.img(), self.flip, False)
        rotated_img = blit_rotate(img, self.transform, self.pivot, self.rotation)
        self.transform = pygame.math.Vector2(rotated_img[1].x, rotated_img[1].y)
        return rotated_img[0].convert_alpha()


    def rotate_at_cursor(self, cursor, camera):
        # Adjust weapon position by considering camera scrolling
        weapon = self.transform - camera.scroll

        # Flip weapon position based on x axis
        if cursor.location.x > weapon.x:
            self.flip = False
        else:
            self.flip = True

        self.rotation = self.get_point_angle(cursor.location, camera.scroll, self.rotationOffset)

    def shoot(self, bullets):
        print(self.transform)
        bullets.add(Bullet(self.transform, (5, 5), "bullet1", self.assets, self.rotation))

    def player_update(self, entity, camera):
        self.transform = entity.get_center()
        self.rotate_at_cursor(entity.cursor, camera)

class Bullet(PhysicsEntity):
    def __init__(self, transform, size, tag, assets, rotation, camLayer=5, isScroll=True, animation="idle", rotationOffset=0):
        super().__init__(transform, size, tag, assets, camLayer, isScroll, animation)
        self.rotation = rotation
        self.speed = 200
        self.rotationOffset = -90
        
    def update(self, dt):
        dx = int(math.cos(math.radians(self.rotation + self.rotationOffset)) * self.speed)
        dy = int(-math.sin(math.radians(self.rotation + self.rotationOffset)) * self.speed)
        self.move(pygame.math.Vector2(dx, dy), [], dt)
        print(dx, dy)