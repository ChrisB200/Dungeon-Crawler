import pygame
from pygame.constants import *
import logging

logger = logging.getLogger(__name__)

class UserInterface:
    def __init__(self, resolution):
        self.menus = {}
        self.screen = pygame.Surface(resolution, pygame.SRCALPHA | pygame.HWSURFACE)

    def update(self):
        for menu in self.menus.values():
            menu.update()

    def event_handler(self, event):
        for menu in self.menus.values():
            menu.event_handler(event)

    def draw(self):
        self.screen.fill((0, 0, 0, 0))  # Clear the screen with transparency
        for menu in sorted(self.menus.values(), key=lambda menu: menu.uiLayer):
            if menu.visible:
                menu.draw(self.screen)

    def add_menu(self, child):
        self.menus[child.name] = child

    def remove_menu(self, childName):
        self.menus.pop(childName, None)

class Menu:
    def __init__(self, name, transform, size, uiLayer=1):
        self.name = name
        self.transform = pygame.math.Vector2(transform)
        self.size = size
        self.children = {}
        self.surface = pygame.Surface(size, pygame.SRCALPHA | pygame.HWSURFACE)
        self.uiLayer = uiLayer
        self.active = False
        self.visible = True

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))  # Clear the surface with transparency
        for child in sorted(self.children.values(), key=lambda child: child.uiLayer):
            self.surface.blit(child.image, child.globalTransform(self.transform))
        screen.blit(self.surface, self.transform)

    def update(self):
        for child in self.children.values():
            child.update()

    def event_handler(self, event):
        for child in self.children.values():
            child.event_handler(event)

    def add_child(self, child):
        self.children[child.name] = child

    def remove_child(self, childName):
        self.children.pop(childName, None)

class Element(pygame.sprite.Sprite):
    def __init__(self, name, transform, image, text=None, uiLayer=1):
        super().__init__()
        self.name = name
        self.transform = pygame.math.Vector2(transform)
        self.image = image
        self.text = text
        self.rect = self.image.get_rect(topleft=self.transform)
        self.uiLayer = uiLayer

    def update(self):
        self.rect.x, self.rect.y = self.transform.x, self.transform.y

    def globalTransform(self, menuTransform):
        return self.transform + menuTransform

    def event_handler(self, event):
        pass

# Example usage:
pygame.init()
resolution = (800, 600)
ui = UserInterface(resolution)

window = pygame.display.set_mode(resolution)

menu = Menu('main_menu', (50, 50), (700, 500))

button_image = pygame.Surface((200, 50))
button_image.fill((255, 0, 0))
button = Element('button', (100, 100), button_image, "Button")

button_image2 = pygame.Surface((200, 100))
button_image2.fill((0, 255, 0))
button2 = Element('button2', (200, 150), button_image2, "Button2")

button_image3 = pygame.Surface((100, 200))
button_image3.fill((0, 0, 255))
button3 = Element('button3', (300, 200), button_image3, "Button3")

menu.add_child(button)
menu.add_child(button2)
menu.add_child(button3)
ui.add_menu(menu)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        ui.event_handler(event)
    
    window.fill((100, 100, 100))
    ui.update()
    ui.draw()
    window.blit(ui.screen, (0, 0))
    pygame.display.flip()

pygame.quit()
