# Modules
import pygame
import math
import logging
from pygame.constants import *

# Scripts
from scripts.entities import Entity, ModifiedSpriteGroup, PhysicsEntity
from scripts.framework import blit_rotate

logger = logging.getLogger(__name__)

class Weapon(Entity):
    def __init__(self, transform, size, tag, assets, bullet, camLayer=3, isScroll=True, animation="idle", pivot=(0, 0)):
        super().__init__(transform, size, tag, assets, camLayer, isScroll, animation)
        self.bullet = bullet
        self.pivot = pygame.math.Vector2(pivot)
        self.rotation = 0

        # magazine
        self.maxMagazine = 200
        self.magazine = self.maxMagazine
        self.reloadTime = 0.5
        self.currentReloadTime = 0
        self.canReload = True
        self.isAutomatic = True

        # time between shots
        self.shootTime = 0.1
        self.currentShootTime = 0
        self.canShoot = True
        self.shooting = False

    def copy(self):
        return Weapon(self.transform, self.size, self.tag, self.assets, self.bullet, self.camLayer, self.isScroll, self.anim, self.pivot)

    @property
    def image(self) -> pygame.Surface:
        img = pygame.transform.flip(self.animation.img(), False, self.flip)
        rotated_img = blit_rotate(img, self.transform, self.pivot, self.rotation)
        self.transform = pygame.math.Vector2(rotated_img[1].x, rotated_img[1].y)
        self.rect = rotated_img[1]
        return rotated_img[0].convert_alpha()

    # rotates the weapon at the cursor
    def rotate_at_cursor(self, cursor, camera) -> None:
        weapon = self.transform - camera.scroll
        self.flip = (False if cursor.location.x > weapon.x else True)
        self.rotation = self.get_point_angle(cursor.location, camera.scroll)

    # shoot bullets
    def shoot(self, game):
        if self.canShoot and self.magazine > 0:
            bullet = self.bullet.copy()
            bullet.start(self.transform, self.rotation)
            game.bullets.add(bullet)
            self.currentShootTime = self.shootTime
            self.magazine -= 1
            print("shot bullet")

    def reload(self):
        if self.canReload:
            self.currentReloadTime = self.reloadTime
            print("reloading")

    def update_timers(self, dt):
        # reload time
        if self.currentReloadTime <= 0:
            if self.canReload == False:#
                self.magazine = self.maxMagazine
                print("replenished magazine")
            self.canReload = True
            # time between shots timer
            if self.currentShootTime <= 0:
                self.canShoot = True
            elif self.currentShootTime > 0:
                self.currentShootTime -= 1 * dt
                self.canShoot = False
        elif self.currentReloadTime > 0:
            self.currentReloadTime -= 1 * dt
            self.canReload = False
            print("cant reload")

    # update the position of the weapon to the players 
    def update(self, entity, camera, dt, game):
        self.transform = entity.get_center().copy()
        self.rotate_at_cursor(entity.cursor, camera)
        self.animation.update(dt)
        self.update_timers(dt)

        if self.shooting:
            self.shoot(game)



class Bullet(PhysicsEntity):
    def __init__(self, transform, size, tag, assets, rotation, camLayer=1, isScroll=True, animation="idle"):
        super().__init__(transform, size, tag, assets, camLayer, isScroll, animation)
        self.rotation = rotation
        self.speed = 300

    def copy(self):
        return Bullet(self.transform, self.size, self.tag, self.assets, self.rotation, self.camLayer, self.isScroll, self.anim)

    def start(self, transform, rotation):
        self.startTransform = transform.copy()
        self.rotation = rotation
        self.transform = self.startTransform
        self.direction = self.calculate_direction()

    # calculate the direction vector
    def calculate_direction(self) -> pygame.math.Vector2:
        direction = pygame.math.Vector2()
        direction.x = math.cos(math.radians(self.rotation)) 
        direction.y = -math.sin(math.radians(self.rotation))
        direction = direction.normalize() * self.speed
        return direction

    def update(self, dt):
        self.move(self.direction, [], dt)
        self.animation.update(dt)
