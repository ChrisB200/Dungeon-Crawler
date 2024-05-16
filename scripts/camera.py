import pygame
from pygame.constants import *
    
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

class Camera(pygame.sprite.Group):
    def __init__(self, resolution, scale, offset=(0, 0)):
        super().__init__(self)
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

    # combines all sprite groups into one and draw by x, y, or layer
    def draw_sprite_groups(self, *args):
        for group in args:
            group.draw(self.screen)

    # combines all rects into one
    def draw_rects(self, *args):
        for arg in args:
            colour = arg[1]
            rect = arg[0]
            pygame.draw.rect(self.screen, colour, rect)

    # combines all surfaces into one
    def draw_surfaces(self, *args):
        for arg in args:
            pos = arg[1]
            surface = arg[0]
            self.screen.blit(surface, pos)

    def draw(self, *args, **kwargs):
        if "fill" in kwargs:
            self.screen.fill(kwargs["fill"])
        
        for group in args:
            for sprite in group:
                allSprites.add(sprite)
        
        if self.renderOrder["layer"]:
            allSprites = sorted(allSprites, key=lambda sprite: sprite.layer)
        elif self.renderOrder["x"]:
            allSprites = sorted(allSprites, key=lambda sprite: sprite.rect.x)
        elif self.renderOrder["y"]:
            allSprites = sorted(allSprites, key=lambda sprite: sprite.rect.y)

        allSprites.draw(self.screen)
        allSprites.clear()
