import sys
import time
import math
import pygame
import pymunk
import pymunk.autogeometry
import pymunk.pygame_util
from pymunk import Vec2d

fps = 60
pygame.init()
width, height = 1000, 500
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
player_turn = 1
assembling = True
white = (255, 255, 255)
green = (50, 168, 82)
black = (0, 0, 0)
red = (200, 0, 0)
grey = (189, 174, 174)
blue = (55, 112, 153)
brown = (133, 64, 65)
FONT = pygame.font.Font(None, 40)
### Physics stuff
space = pymunk.Space()
space.gravity = 0, 900
space.sleep_time_threshold = 0.3

draw_options = pymunk.pygame_util.DrawOptions(window)
pymunk.pygame_util.positive_y_is_up = False

class car_bodies:
    def __init__(self, base_hp, shape, mass, hole1, hole2, wheel_coords=0) -> None:
        self.base_hp = base_hp
        self.shape = shape
        self.mass = mass
        self.hole1 = hole1
        self.hole2 = hole2
        self.wheel_cords = wheel_coords

# MAKING CAR BODIES
classic = car_bodies(
    150, [(60, 0), (120, 50), (-40, 50), (-40, 0)], 100, (40, 30), (70, -30), -80
)
surfer = car_bodies(
    200, [(120, 0), (60, 50), (-40, 50), (-40, 0)], 150, (40, 30), (70, -30), -80
)
titan = car_bodies(
    300, [(40, 50), (-40, 50), (-40, -100), (40, -100)], 200, (40, 30), (40, -30), 0
)


def main():

    while True:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and (event.key in [pygame.K_ESCAPE, pygame.K_q])
            ):
                sys.exit(0)

        space.step(1.0 / fps)
        window.fill(pygame.Color("white"))

        space.debug_draw(draw_options)



        pygame.display.flip()
        dt = clock.tick(fps)
        total_time += 1


if __name__ == "__main__":
    main()
