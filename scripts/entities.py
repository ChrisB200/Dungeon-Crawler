# Modules
import pygame
import logging
from pygame.constants import *

# Scripts


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, size, tag, assets):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.size = pygame.math.Vector2(size)
        self.tag = tag
        self.assets = assets
        self.flip = False
        self.image = pygame.Surface(size)
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()