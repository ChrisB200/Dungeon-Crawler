import pygame
from pygame.constants import *

class ModifiedGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()


class Window():
    def __init__(self, resolution, fullscreen=FULLSCREEN):
        self.resolution = resolution
        self.display = pygame.display.set_mode(resolution)

        self.cameras = [Camera(self.resolution, 2), Camera(self.resolution, 4), Camera(self.resolution, 6), Camera(self.resolution, 8)]
        self.currentCameraIndex = 0
    
    @property
    def camera(self):
        return self.cameras[self.currentCameraIndex]
    
    @property
    def screen(self):
        return self.camera.screen
    
    def update(self):
        #self.camera.update()
        pass

    def draw(self, *args, **kwargs):
        self.camera.draw(*args, **kwargs)

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
        # scroll
        self.trueScroll = [0, 0]
        # tracking
        self.isFollowing = None  # [target, [offsetX, offsetY]]
        self.isPanning = False
        self.panStrength = 5
        self.offset = (0, 0)
        # scaling
        self.desired_scale = scale
        self.min_scale = 1.5  
        self.max_scale = 2 
        self.zoom_speed = 1
        # other
        self.renderOrder = {"x": False, "y": False, "layer": True}
        self.screen = pygame.Surface((self.resolution[0] / self.scale, self.resolution[1] / self.scale))
        self.targets = ()

    def draw(self, *args, **kwargs):
        if "fill" in kwargs:
            self.screen.fill(kwargs["fill"])
        for arg in args:
            # For sprite groups: pygame.sprite.Group
            if isinstance(arg, pygame.sprite.Group) or isinstance(arg, ModifiedGroup):
                arg.draw(self.screen)
            
            elif isinstance(arg, tuple):
                # For rects: (Rect, Colour)
                if isinstance(arg[0], pygame.Rect):
                    pygame.draw.rect(self.screen, arg[1], arg[0])
                # For surfaces: (Rect, Colour)
                elif isinstance(arg[0], pygame.Surface):
                    self.screen.blit(arg[0], arg[1])