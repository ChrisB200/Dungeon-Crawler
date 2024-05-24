# Modules
import pygame
import math
import logging
from pygame.constants import *

# Scripts
from scripts.entities import Entity, ModifiedSpriteGroup, PhysicsEntity
from scripts.framework import blit_rotate, get_center
from scripts.camera import Camera


logger = logging.getLogger(__name__)

class Weapon(Entity):
    def __init__(self, transform, muzzleTransform, size, tag, assets, bullet, camLayer=3, isScroll=True, animation="idle", pivot=(0, 0)):
        super().__init__(transform, size, tag, assets, camLayer, isScroll, animation)
        self.bullet = bullet
        self.pivot = pygame.math.Vector2(pivot)
        self.rotation = 0
        self.localRotation = 0
        self.muzzleTransform = pygame.math.Vector2(muzzleTransform)

        # magazine
        self.maxMagazine = 200
        self.magazine = self.maxMagazine
        self.reloadTime = 1
        self.currentReloadTime = 0
        self.canReload = True
        self.isAutomatic = True

        # time between shots
        self.shootTime = 0.1
        self.currentShootTime = 0
        self.canShoot = True
        self.shooting = False

    def copy(self):
        return Weapon(self.transform, self.muzzleTransform, self.size, self.tag, self.assets, self.bullet, self.camLayer, self.isScroll, self.anim, self.pivot)

    @property
    def image(self) -> pygame.Surface:
        img = pygame.transform.rotate(pygame.transform.flip(self.animation.img(), False, self.flip), self.localRotation)
        rotated_img = blit_rotate(img, self.transform, self.pivot, self.rotation)
        self.transform = pygame.math.Vector2(rotated_img[1].x, rotated_img[1].y)
        self.rect = rotated_img[1]
        return rotated_img[0].convert_alpha()
    
    # rotates the weapon at the cursors center
    def rotate_at_cursor(self, cursor, camera:Camera) -> None:
        weapon = self.transform - camera.scroll
        self.flip = False if cursor.location.x > weapon.x else True
        self.rotation = self.get_point_angle(get_center(cursor.location, cursor.size), camera.scroll)

    def get_muzzle_transform(self):
        # calculate the offset from the pivot to the muzzle in the rotated image
        offset = self.muzzleTransform - self.pivot
        if self.flip: 
            offset.x = -offset.x
            rotated_offset = offset.rotate(180-self.rotation)
        else:
            rotated_offset = offset.rotate(-self.rotation)

        # calculate the global position of the muzzle
        muzzle_position = self.transform + rotated_offset
        return muzzle_position

    # shoot bullets
    def shoot(self, game):
        if self.canShoot and self.magazine > 0:
            # create bullet at muzzle transform
            bullet = self.bullet.copy()
            muzzleTransform = self.get_muzzle_transform()
            bullet.start(muzzleTransform, self.rotation)

            # add to world and camera
            game.bullets.add(bullet)
            game.add_to_world(bullet)

            # start timer
            self.currentShootTime = self.shootTime
            self.magazine -= 1

    def reload(self):
        if self.canReload:
            self.currentReloadTime = self.reloadTime

    def update_timers(self, dt):
        # reload time
        if self.currentReloadTime <= 0:
            if self.canReload == False:#
                self.magazine = self.maxMagazine
            self.canReload = True
            self.localRotation = 0
            # time between shots timer
            if self.currentShootTime <= 0 and self.currentReloadTime <=0:
                self.canShoot = True
            elif self.currentShootTime > 0:
                self.currentShootTime -= 1 * dt
                self.canShoot = False
            else:
                self.canShoot = False
        elif self.currentReloadTime > 0:
            self.currentReloadTime -= 1 * dt
            self.canReload = False
            self.localRotation += 360 * (dt / self.reloadTime)
            self.localRotation %= 360
            self.canShoot = False

    # update the position of the weapon to the players 
    def update(self, entity, camera:Camera, dt, game):
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
        self.timeAlive = 2
        self.currentTimeAlive = self.timeAlive

    # calculate the direction vector
    def calculate_direction(self) -> pygame.math.Vector2:
        return super().calculate_direction() * self.speed
    
    def copy(self):
        return Bullet(self.transform, self.size, self.tag, self.assets, self.rotation, self.camLayer, self.isScroll, self.anim)

    def start(self, transform, rotation):
        self.startTransform = transform.copy()
        self.rotation = rotation
        self.transform = self.startTransform
        self.direction = self.calculate_direction()

    def update_timer(self, dt):
        self.currentTimeAlive -= dt * 1
        if self.currentTimeAlive < 0:
            self.kill()
            self.remove()

    def update(self, dt):
        self.move(self.direction, [], dt)
        self.animation.update(dt)
        self.update_timer(dt)
        
