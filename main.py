import os
import time
import random
import pygame
import numpy as np

LENGTH = 750
WIDTH = 250
SCREEN = pygame.display.set_mode((LENGTH, WIDTH))
SPRITE_IMAGE = pygame.image.load("sprite.png")
SPRITE_WIDTH = 50
GOAL_IMAGE = pygame.image.load("flag.png")
GOAL_WIDTH = 50

BRIDGE_COLOR = "#571818"
BRIDGE_WIDTH = WIDTH/2
BRIDGE_LENGTH = LENGTH

# global arameters
SPEED = 10
# balanced
WIND_VALUES = [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
#unbalanced
#WIND_VALUES = [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5, -6, -7, -8, -9]
# heavy few
#WIND_VALUES = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, -20, 40, -40]
# heavy often
#WIND_VALUES = [0, 0, 0, 0, 0, 20, -20, 40, -40]
# TODO FRCITION (prior moves linger? new direction with less speed? new direction gets delayed?)

class Bridge:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.length = BRIDGE_LENGTH
        self.width = BRIDGE_WIDTH
        self.color = BRIDGE_COLOR
        self.rect_bridge = self.draw_bridge()

    def draw_bridge(self):
        return pygame.draw.rect(SCREEN, self.color, (0, self.width-self.width/2, self.length, self.width))

class Agent:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.rect_agent = SPRITE_IMAGE.get_rect(topleft=(self.x, self.y))

    def draw_agent(self):
        SCREEN.blit(SPRITE_IMAGE, (self.x, self.y))

    def detect_fall(self, x, y):
        if x > LENGTH or y > WIDTH:
            return True
    # only action so far is going right
    def move(self, action):
        x = self.x
        y = self.y
        if action == "right":
            x += SPEED
        if not self.detect_fall(x, y):
            self.x = x
            self.y = (y + get_wind())
            self.pos = (self.x, self.y)
            self.rect_agent = SPRITE_IMAGE.get_rect(topleft=(self.x, self.y))
        else:
            print("Out of bounds")
            exit()


class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.rect_goal = GOAL_IMAGE.get_rect(topleft=(self.x, self.y))
    def draw_goal(self):
        SCREEN.blit(GOAL_IMAGE, (self.x, self.y))


class Env:
    def __init__(self, agent, goal, bridge):
        self.render_delay = 0.2
        self.agent = agent
        self.goal = goal
        self.bridge = bridge

    def step(self, actions=[]):
        self.render()

    def render(self, delay=False):
        SCREEN.fill("white")
        if delay:
            time.sleep(self.render_delay)
        self.bridge.draw_bridge()
        self.agent.draw_agent()
        self.goal.draw_goal()
        pygame.display.update()


def get_wind():
    return random.choice(WIND_VALUES)


def check_collision(sprite_1, sprite_2):
    if sprite_1.colliderect(sprite_2):
        return True
    else:
        return False


def main():
    b = Bridge()
    a = Agent(0, WIDTH/2-SPRITE_WIDTH/2)
    g = Goal(LENGTH-50, WIDTH/2-GOAL_WIDTH/2)
    e = Env(a, g, b)
    for i in range(0, 100):
        a.move("right")
        e.render(True)
        if check_collision(a.rect_agent, g.rect_goal):
            print("Win")
            exit()
        if not check_collision(b.rect_bridge, a.rect_agent):
            print("Fell off")
            exit()



if __name__ == "__main__":
    main()
