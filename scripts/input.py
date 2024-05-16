import pygame
from dataclasses import dataclass

@dataclass
class Controls:
    moveRight: int
    moveLeft: int
    moveDown: int
    moveUp: int
    dash: int
    pause: int
    shoot: int

class Controller:
    def __init__(self, controls:Controls, joystick):
        self.controls = controls
        self.joystick = joystick
        self.leftStick = pygame.math.Vector2()
        self.rightStick = pygame.math.Vector2()
        self.deadzone = 0.1

    # Controls the deadzone - input below deadzone value is set to 0 to stop stick drift
    def control_deadzone(self, deadzone, *axes):
        newAxes = []
        for axis in axes:
            if abs(axis) < deadzone:
                axis = 0
            newAxes.append(axis)

        return newAxes

    # Calculate sticks movement
    def calculate_sticks(self):
        leftStick = self.control_deadzone(self.deadzone, self.joystick.get_axis(0), self.joystick.get_axis(1))
        rightStick = self.control_deadzone(self.deadzone, self.joystick.get_axis(2), self.joystick.get_axis(3))
        self.leftStick.x = leftStick[0]
        self.leftStick.y = leftStick[1]
        self.rightStick.x = rightStick[0]
        self.rightStick.y = rightStick[1]

    def update(self):
        self.calculate_sticks()
    
class Keyboard:
    def __init__(self, controls:Controls):
        self.controls = controls

    def update(self):
        pass

# Checks for controllers and initialises them
def controller_check():
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
    return joysticks
