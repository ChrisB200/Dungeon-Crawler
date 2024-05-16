# Modules
import pygame
from pygame.constants import *
    
class Window():
    def __init__(self, resolution, fullscreen=FULLSCREEN):
        self.resolution = resolution
        self.display = pygame.display.set_mode(resolution)

        self.cameras = [Camera(self.resolution, 4)]
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

    def get_camera(self, index):
        return self.cameras[index]

class Camera(pygame.sprite.Group):
    def __init__(self, resolution, scale, offset=(0, 0)):
        super().__init__(self)
        self.resolution = resolution
        self.scale = scale
        self.offset = offset
        self.screen = pygame.Surface((self.resolution[0] / self.scale, self.resolution[1] / self.scale))
        # scroll
        self.trueScroll = pygame.math.Vector2()
        # tracking
        self.target = None  # [target, [offsetX, offsetY]]
        self.isPanning = False
        self.panStrength = 20
        self.offset = (0, 0)
        # scaling
        self.desiredScale = scale
        self.minScale = scale - 0.5 
        self.maxScale = scale + 0.5
        self.zoomSpeed = 1
        # other
        self.renderOrder = {"x": False, "y": False, "layer": True}
        self.targets = ()

    @property
    def scroll(self):
        return pygame.math.Vector2([int(self.trueScroll.x), int(self.trueScroll.y)])
    
    # the rescaled screen size
    @property
    def screenSize(self):
        return self.screen.get_size()[0], self.screen.get_size()[1]
    
    def calculate_scroll(self, sprite):
        if sprite.isScroll:
            self.screen.blit(sprite.image, (sprite.transform.x - self.scroll.x, sprite.transform.y - self.scroll.y))
        else:
            self.screen.blit(sprite.image, (sprite.transform.x, sprite.transform.y))

    # orders sprite by layer value
    def draw_by_layers(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.camLayer):
            self.calculate_scroll(sprite)
            print(sprite.tag)

    # orders sprite by x value
    def draw_by_x(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.transform.x):
            self.calculate_scroll(sprite)
    
    # orders sprite by y value
    def draw_by_y(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.transform.y):
            self.calculate_scroll(sprite)

    # seperates sprites out of groups and adds them into a new group
    def add_sprites(self, *args):
        for group in args:
            for sprite in group:
                self.add(sprite)

    # draws the keyword arguments
    def draw_background(self, **kwargs):
        if "fill" in kwargs:
            self.screen.fill(kwargs["fill"])

    # sets a target sprite
    def set_target(self, target, offset=(0, 0)):
        self.target = target
        self.offset = offset

    # sets multiple target sprites
    def set_targets(self, *args, offset=(0, 0)):
        self.targets = args
        self.offset = offset

    # follows the center of a target 
    def follow_target(self):
        targetCenter = pygame.math.Vector2()
        # slowly pans
        if self.isPanning:
            targetCenter.x = (self.target.transform.x + self.target.size[0] // 2) + self.offset[0]
            targetCenter.y = (self.target.transform.y + self.target.size[1] // 2) + self.offset[1]
            self.trueScroll.x += ((targetCenter.x - self.trueScroll.x) - self.screenSize[0] / 2) / self.panStrength
            self.trueScroll.y += ((targetCenter.y - self.trueScroll.y) - self.screenSize[1] / 2) / self.panStrength
        # instantly follows
        else:
            targetCenter.x = (self.target.transform.x + self.target.size[0] // 2)
            targetCenter.y = (self.target.transform.y + self.target.size[1] // 2)
            self.trueScroll.x += ((targetCenter.x - self.trueScroll.x) - self.screenSize[0] / 2) / self.panStrength
            self.trueScroll.y += ((targetCenter.y - self.trueScroll.y) - self.screenSize[1] / 2) / self.panStrength

    # follows the center of multiple targets
    def follow_multiple_targets(self):
        # Get values for bounding box of all targets
        boundingMin = pygame.math.Vector2()
        boundingMin.x = min(target.transform.x for target in self.targets) - 100
        boundingMin.y = min(target.transform.y for target in self.targets) - 100

        boundingMax = pygame.math.Vector2()
        boundingMax.x = max(target.transform.x + target.width for target in self.targets) + 100
        boundingMax.y = max(target.transform.y + target.height for target in self.targets) + 100

        # calculate the size of the bounding box
        boxWidth = boundingMax.x - boundingMin.x
        boxHeight = boundingMax.y - boundingMin.y

        # calculate the required scale to fit the bounding box on the screen
        requiredScale = pygame.math.Vector2(self.resolution[0] / boxWidth, self.resolution[1] / boxHeight)
        minRequiredScale = min(requiredScale.x, requiredScale.y)

        # calculate the current distance between targets
        currentDistance = boundingMax - boundingMin

        # check if targets are moving away from each other
        if (currentDistance.x > boxWidth // requiredScale.x) or (currentDistance.y > boxHeight // requiredScale.y):
            # update the camera scale to fit the bounding box
            self.zoom(minRequiredScale - self.scale)
        else:
            # zoom back in towards the initial scale
            self.zoom(self.scale - self.scale)  # Equivalent to self.zoom(0)

        # center the camera on the center of the bounding box
        center = (boundingMin + boundingMax) / 2
        targetCenter = pygame.math.Vector2()
        targetCenter.x = center.x + self.offset[0]
        targetCenter.y = center.y + self.offset[1]
        self.trueScroll.x += ((targetCenter.x - self.trueScroll.x) - self.screenSize[0] / 2) / self.panStrength
        self.trueScroll.y += ((targetCenter.y - self.trueScroll.y) - self.screenSize[1] / 2) / self.panStrength

    # allows for zooming functionality
    def zoom(self, amount: float):
        # incrementally update the desired scale
        self.desiredScale += amount
        # clamp the desired scale to the defined range
        self.desiredScale = max(self.minScale, min(self.maxScale, self.desiredScale))
        # smoothly transition the current scale towards the desired scale
        self.scale += (self.desiredScale - self.scale) * self.zoomSpeed
        tempScreen = pygame.transform.scale(self.screen.copy(), (self.resolution[0] / self.scale, self.resolution[1] / self.scale))
        self.screen = tempScreen

    # handles all the drawing within the camera class
    def draw(self, *args, **kwargs):
        self.draw_background(**kwargs)
        self.add_sprites(*args)
        
        match self.renderOrder:
            case {"layer": True}:
                self.draw_by_layers()
            case {"x": True}:
                self.draw_by_x
            case {"y": True}:
                self.draw_by_y

        # empty sprites since they get re added
        self.empty()

    # handles all the updates within the camera class
    def update(self):
        if self.targets:
            self.follow_multiple_targets()
        elif self.target is not None:
            self.follow_target()
