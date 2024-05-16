# Modules
import pygame
import json
import os

# Animation System
class Animation:
    def __init__(self, images, img_dur=0.2, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
        self.time_elapsed = 0
    
    # Returns a copy of itself
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    # Updates the current frame (uses deltatime)
    def update(self, dt):
        self.time_elapsed += dt
        while self.time_elapsed >= self.img_duration:
            self.time_elapsed -= self.img_duration
            if self.loop:
                self.frame = (self.frame + 1) % len(self.images)
            else:
                self.frame = min(self.frame + 1, len(self.images) - 1)
                if self.frame == len(self.images) - 1:
                    self.done = True
    
    # Returns the current frame
    def img(self):
        return self.images[self.frame]
    
# Loads an image using its location   
def load_image(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0, 0, 0))
    return img
    
# Loads a group of images in a allocation
def load_images(path):
    images = []
    for img_name in sorted(os.listdir(path)):
        images.append(load_image(path + '/' + img_name))
    return images

    
def load_animations(base_path, data="data/animation_data.json"):
    assets = {}
    with open(data, "rb") as file:
        data = json.load(file)

    for group in os.listdir(base_path):
        for folder in os.listdir(base_path+group):
            for animation in os.listdir(base_path+group+"/"+folder):
                name = f"{folder}/{animation}"
                if name in data:
                    assets[name] = Animation(load_images(f"{base_path}{group}/{folder}/{animation}"), data[name]["img_dur"], data[name]["loop"])
                else:
                    assets[name] = Animation(load_images(f"{base_path}{group}/{folder}/{animation}"))

    return assets