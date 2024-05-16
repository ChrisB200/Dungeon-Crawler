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
        self.camera.update()

    def draw(self, *args, **kwargs):
        self.camera.draw(*args, **kwargs)
        self.display.blit(pygame.transform.scale(self.screen, self.resolution), (0, 0))
        
    def add_camera(self, camera):
        self.cameras.append(camera)

    def change_camera(self, increment):
        self.currentCameraIndex += increment

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

    def draw_by_layers(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.camLayer):
            self.screen.blit(sprite.image, (sprite.pos.x, sprite.pos.y))

    def draw_by_x(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.pos.x):
            self.screen.blit(sprite.image, (sprite.pos.x, sprite.pos.y))

    def draw_by_y(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.pos.y):
            self.screen.blit(sprite.image, (sprite.pos.x, sprite.pos.y))

    def add_sprites(self, *args):
        for group in args:
            for sprite in group:
                self.add(sprite)

    def draw_background(self, **kwargs):
        if "fill" in kwargs:
            self.screen.fill(kwargs["fill"])

    def draw(self, *args, **kwargs):
        self.draw_background(**kwargs)
        self.add_sprites(*args)
        
        if self.renderOrder["layer"]:
            print("hi")
            self.draw_by_layers()
        elif self.renderOrder["x"]:
            self.draw_by_x
        elif self.renderOrder["y"]:
            self.draw_by_y

        self.empty()

    def update(self):
        pass
