import pygame
from pygame.constants import *

class Window():
    def __init__(self, resolution, fullscreen=FULLSCREEN):
        self.resolution = resolution
        self.display = pygame.display.set_mode(resolution)

        self.cameras = [Camera(self.resolution, 2), Camera(self.resolution, 4), Camera(self.resolution, 10)]
        self.currentCameraIndex = 0
    
    @property
    def camera(self):
        return self.cameras[self.currentCameraIndex]
    
    @property
    def screen(self):
        return self.camera.screen
    
    def update(self):
        pass

    def draw(self, entities):
        self.screen.fill((100, 100, 100))
        entities.draw(self.screen)
        self.display.blit(pygame.transform.scale(self.screen, self.resolution), (0, 0))
        
    def add_camera(self, camera):
        self.cameras.append(camera)

    def set_camera(self, index):
        self.currentCameraIndex = index

class Camera():
    def __init__(self, resolution, scale, offset=(0, 0)):
        self.resolution = resolution
        self.scale = scale
        self.offset = offset
        self.screen = pygame.Surface((self.resolution[0] / self.scale, self.resolution[1] / self.scale))

