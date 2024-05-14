import pygame
from dataclasses import dataclass

@dataclass
class Controls:
    moveRight: int
    moveLeft: int
    moveDown: int
    moveUp: int
    dash: int
    jump: int
    pause: int
    shoot: int

class Controller:
    def __init__(self, controls:Controls, joystick):
        self.controls = controls
        self.joystick = joystick
        self.leftStick = [0, 0]
        self.rightStick = [0, 0]
        self.deadzone = 0.1

    # Controls the deadzone - input below deadzone value is set to 0 to stop mouse drift
    def control_deadzone(self, deadzone, *axes):
        newAxes = []
        for axis in axes:
            if abs(axis) < deadzone:
                axis = 0
            newAxes.append(axis)

        return newAxes

    # Calculate sticks movement
    def calculate_sticks(self):
        self.leftStick = self.control_deadzone(self.deadzone, self.joystick.get_axis(0), self.joystick.get_axis(1))
        self.rightStick = self.control_deadzone(self.deadzone, self.joystick.get_axis(2), self.joystick.get_axis(3))

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