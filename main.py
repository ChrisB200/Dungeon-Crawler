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
from scripts.weapons import *
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
        self.window = Window(self.settings.resolution, flags=pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.assets = load_animations(BASE_IMG_PATH)
        self.inputDevices = []
        self.dt = 1

        # game properties
        self.entities = ModifiedSpriteGroup()
        self.players = ModifiedSpriteGroup()
        self.weapons = ModifiedSpriteGroup()
        self.cursors = ModifiedSpriteGroup()
        self.bullets = ModifiedSpriteGroup()
        self.state = "running"

        # bullets
        self.DEFAULT_BULLET = Bullet((0, 0), (5, 2), "bullet1", self.assets, 0)

        # weapons
        self.DEFAULT_WEAPON = Weapon((0, 0),(8, 0), (8, 6), "gun", self.assets, bullet=self.DEFAULT_BULLET, camLayer=5, pivot=(-6, 0))
    
    # creates a player and assigns them a controller
    def create_player(self, pos, input=0, layer=0):
        numOfPlayers = len(self.players.sprites())

        # player properties
        player = Player(numOfPlayers, pos, [24, 24], "newPlayer", self.assets, layer, animation="idle/down")
        cursor = UserCursor(pos, [9, 9], "cursor", self.assets, layer=90, isScroll=False)
        weapon = self.DEFAULT_WEAPON.copy()
        weapon.set_transform(pos)
        input = self.inputDevices[input]

        # assignment of the properties
        player.input = input
        player.cursor = cursor
        player.weapon = weapon

        # add to sprite groups
        self.players.add(player)
        self.cursors.add(cursor)
        self.weapons.add(weapon)

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

    def calculate_deltatime(self):
        self.dt = self.clock.tick() / 1000
    
    # draws the window
    def draw(self):
        self.window.draw_world(self.players, self.entities, self.weapons, self.bullets, fill=(150, 150, 150))
        self.window.draw_foreground(self.cursors)
        self.window.draw()
        pygame.display.update()
    
    def update(self):
        self.window.update()

        player: Player
        for player in self.players:
            player.update([], self.dt, self.window.world, self)
        
        for bullet in self.bullets:
            bullet.update(self.dt)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = ""

            for player in self.players:
                player.event_handler(event, self)

    def run(self):
        self.detect_inputs()
        self.create_player((200, 20), 0, layer=1)
        #self.create_player((500, 20), 0, layer=1)
        self.window.world.set_targets(*[self.players.get_entity(i) for i in range(len(self.players.sprites()))])
        while self.state == "running":
            pygame.mouse.set_visible(False)
            self.calculate_deltatime()
            self.event_handler()
            self.update()
            self.draw()
            #print(int(self.clock.get_fps()))
            
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()