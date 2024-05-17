# Modules
import pygame
import sys
import logging
from pygame.constants import *

# Scripts
from scripts.camera import Window
from scripts.settings import Settings
from scripts.entities import Player, ModifiedSpriteGroup, UserCursor
from scripts.animation import load_animations
from scripts.input import Controller, Keyboard, controller_check
from scripts.constants import BASE_IMG_PATH

# configure the logger
logging.basicConfig(
    level=logging.INFO,  # set the log level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler("game.log"),  # Log to a file
        logging.StreamHandler()          # Also log to console
    ]
)

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
        self.window = Window(self.settings.resolution)
        self.clock = pygame.time.Clock()
        self.assets = load_animations(BASE_IMG_PATH)
        self.inputDevices = []

        # game properties
        self.entities = ModifiedSpriteGroup()
        self.players = ModifiedSpriteGroup()
        self.state = "running"
    
    # creates a player and assigns them a controller
    def create_player(self, pos, input=0, layer=0):
        numOfPlayers = len(self.players.sprites())

        # player properties
        player = Player(numOfPlayers, pos, [8, 13], "player2", self.assets, layer, animation="idle/down")
        cursor = UserCursor(pos, [9, 9], "cursor1", self.assets, layer=90, isScroll=False)
        input = self.inputDevices[input]

        # assignment of the properties
        player.input = input
        player.cursor = cursor
        self.players.add(player)
        self.entities.add(cursor)

    # detects input devices and appends them
    def detect_inputs(self):
        self.inputDevices = []
        self.inputDevices.append(Keyboard(self.settings.keyboard))

        try:
            joysticks = controller_check()
            for joystick in joysticks:
                controller = Controller(self.settings.controller, joystick)
                self.inputDevices.append(controller) 
                logger.info("Detected controller, name: %s, guid: %s", controller.name, controller.guid)
        except:
            logger.info("No controllers detected")

        logger.info("Detected %s input devices", len(self.inputDevices))
    
    # draws the window
    def draw(self):
        self.window.draw(self.players, self.entities, fill=(100, 100, 100))
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
                    self.window.change_camera(1)
                if event.key == K_LEFT:
                    self.window.change_camera(-1)

            for player in self.players:
                player.input_events(event)

    def run(self):
        self.detect_inputs()
        self.create_player((40, 20), 1, layer=1)
        self.create_player((40, 20), 0, layer=1)
        self.window.camera.set_targets(self.players.get_entity(0), self.players.get_entity(1))
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
        


