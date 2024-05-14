# Modules
import pygame
import sys
import logging
from pygame.constants import *

# Scripts
from scripts.camera import Window, ModifiedGroup
from scripts.settings import Settings
from scripts.entities import Entity
from scripts.animation import load_animations

logger = logging.getLogger(__name__)

BASE_IMG_PATH = "data/images/"

class MainMenu():
    pass

class PauseMenu():
    pass

class Game():
    def __init__(self):
        # initialisation
        logging.basicConfig(filename="game.log", level=logging.INFO)
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.joystick.init()

        # core properties
        
        self.settings = Settings()
        self.window = Window(self.settings.resolution, 2)
        self.clock = pygame.time.Clock()
        self.state = "running"
        self.assets = load_animations(BASE_IMG_PATH)

        # game properties
        self.entityTest = Entity((20, 20), (20, 20), "player", self.assets)
        self.entities = ModifiedGroup()
        self.entities.add(self.entityTest)
        
        
    def draw(self):
        self.window.draw(self.entities, (self.entityTest.rect, (255, 0, 0)), fill=(100, 100, 100))
        pygame.display.update()
        
    def update(self):
        self.window.update()
        self.entityTest.update_animation(1)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = ""
            if event.type == pygame.KEYDOWN:
                if event.key == K_RIGHT:
                    self.window.currentCameraIndex += 1
                    self.entityTest.set_action("run")
                if event.key == K_LEFT:
                    self.window.currentCameraIndex -= 1 

    def run(self):
        while self.state == "running":
            self.clock.tick(self.settings.targetFPS)
            self.event_handler()
            self.update()
            self.draw()
            
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
        


