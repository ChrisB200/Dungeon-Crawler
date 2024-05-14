# Modules
import pygame
import logging
from pygame.constants import *

# Scripts
from scripts.framework import get_center, collision_test
from scripts.input import Controller, Keyboard
from scripts.animation import Animation

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos:list[int, int], size:list[int, int], tag:str, assets:dict[str, Animation]):
        super().__init__()
        # parameters
        self.pos = pygame.math.Vector2(pos)
        self.size = size
        self.tag = tag
        self.assets = assets

        # movement
        self.flip = False
        self.directions: dict[str, bool] = {"left" : False, "right": False, "up": False, "down": False}
        self.movement: list[float, float] = [0, 0] # [x, y]

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