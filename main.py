# Modules
import pygame
import sys
import logging
from pygame.constants import *

# Scripts
from scripts.camera import Window
from scripts.settings import Settings
from scripts.entities import Entity

logger = logging.getLogger(__name__)

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
        self.clock = pygame.time.Clock()
        self.state = "running"

        # game properties
        self.entityTest = Entity((20, 20), (20, 20), "test", None)
        self.entities = pygame.sprite.Group()
        self.entities.add(self.entityTest)
        self.window = Window(self.settings.resolution, 2)
        
    def draw(self):
        self.window.draw(self.entities)
        pygame.display.update()
        
    def update(self):
        self.window.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = ""

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
        


