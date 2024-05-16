# Modules
import pygame
import sys
import logging
from pygame.constants import *

# Scripts
from scripts.camera import Window
from scripts.settings import Settings
from scripts.entities import Player
from scripts.animation import load_animations
from scripts.input import Controller, Keyboard, controller_check

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
        self.assets = load_animations(BASE_IMG_PATH)
        self.inputDevices = []

        # game properties
        self.entities = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.state = "running"
    
    # creates a player and assigns them a controller
    def create_player(self, pos, input=0, layer=0):
        numOfPlayers = len(self.entities.sprites())
        player = Player(numOfPlayers, pos, [8, 13], "player", self.assets, layer)
        player.input = self.inputDevices[input]
        self.players.add(player)

    # detects input devices and appends them
    def detect_inputs(self):
        self.inputDevices = []
        self.inputDevices.append(Keyboard(self.settings.keyboard))

        try:
            self.joysticks = controller_check()
            for controller in self.joysticks:
                self.inputDevices.append(Controller(self.settings.controller, controller)) 
        except:
            print("no controllers detected")
    
    # draws the window
    def draw(self):
        self.window.draw(self.players, fill=(100, 100, 100))
        pygame.display.update()
    
    def update(self):
        self.window.update()

        player: Player
        for player in self.players.sprites():
            player.update([], 1, self.window.camera)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = ""
            if event.type == pygame.KEYDOWN:
                if event.key == K_RIGHT:
                    self.window.currentCameraIndex += 1
                    print(self.players.layers)
                    self.players.change_layer(self.players.get_sprite(0), self.players.get_sprite(0)._layer + 1)
                if event.key == K_LEFT:
                    self.window.currentCameraIndex -= 1
                    print(self.players.layers)
                    self.players.change_layer(self.players.get_sprite(0), self.players.get_sprite(0)._layer - 1)
            
            for player in self.players.sprites():
                player.input_events(event)

    def run(self):
        self.detect_inputs()
        self.create_player((40, 20), layer=6)
        self.create_player((20, 20), 1, layer=4)
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
        


