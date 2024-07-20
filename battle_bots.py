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

boundaries = []
boundaries.append(pymunk.Segment(space.static_body, (-100, 490), (1000, 490), 10))
# boundaries.append(pymunk.Segment(space.static_body, (0, 0), (0, 490), 10))
# boundaries.append(pymunk.Segment(space.static_body, (990, 0), (990, 490), 10))
for x in boundaries:
    x.friction = 1.0
    space.add(x)


class car_bodies:
    def __init__(self, base_hp, shape, mass, hole1, hole2, wheel_coords=0) -> None:
        self.base_hp = base_hp
        self.shape = shape
        self.mass = mass
        self.hole1 = hole1
        self.hole2 = hole2
        self.wheel_cords = wheel_coords


class wheels:
    def __init__(self, radius, drawing, circle=None) -> None:
        self.radius = radius
        self.mass = radius * 3.3
        self.hp = radius
        self.drawing = drawing
        self.circle = circle

    def draw(
            self,
    ):
        return pygame.draw.circle(*self.drawing)

    def get_touching(self, value):
        return value.collidepoint(pygame.mouse.get_pos())

def car(
        space,
        car_,
        start,
        direction,
):
    car = car_[0]
    wheel_l = car_[2] if direction == 1 else car_[1]
    wheel_r = car_[1] if direction == 1 else car_[2]
    pos = Vec2d(start, 500)
    # Left WHEEl
    wheel_color = *black, 255
    mass = 100
    radius_l = wheel_l.radius
    moment = pymunk.moment_for_circle(mass, 20, radius_l)
    wheel_left_b = pymunk.Body(mass, moment)
    wheel_left_s = pymunk.Circle(wheel_left_b, radius_l)
    wheel_left_s.friction = 2
    wheel_left_s.color = wheel_color
    space.add(wheel_left_b, wheel_left_s)
    # Right Wheel
    mass = 100
    radius_r = wheel_r.radius
    moment = pymunk.moment_for_circle(mass, 20, radius_r)
    wheel_right_b = pymunk.Body(mass, moment)
    wheel_right_s = pymunk.Circle(wheel_right_b, radius_r)
    wheel_right_s.friction = 2
    wheel_right_s.color = wheel_color
    space.add(wheel_right_b, wheel_right_s)
    # CAR BODY
    mass = car.mass
    car_body = pymunk.Body(mass, 150000)  # 150000
    # car_shape = pymunk.Poly.create_box(car_body, size)
    car_shape = pymunk.Poly(
        car_body,
        car.shape
        if direction == 1
        else list(map(lambda x: (x[0] * direction, x[1]), car.shape)),
    )
    car_shape.color = *brown, 50
    space.add(car_body, car_shape)
    top_left, top_right, bottom_right, bottom_left = car_shape.get_vertices()

    car_body.position = pos + (0, -80)
    wheel_left_b.position = pos - (
        car.hole1[0] * direction,
        car.hole1[1],
    )
    wheel_right_b.position = pos + (
        car.hole2[0] * direction,
        car.hole2[1],
    )

    space.add(
        pymunk.PinJoint(wheel_left_b, car_body, (0, 0), (top_right)),
        pymunk.PinJoint(wheel_left_b, car_body, (0, 0), (bottom_left)),
        pymunk.PinJoint(wheel_right_b, car_body, (0, 0), (top_left)),
        pymunk.PinJoint(wheel_right_b, car_body, (0, 0), (bottom_right)),
    )

    speed = mass / 25 * direction * (30 / radius_l)
    m1, m2 = (
        pymunk.SimpleMotor(
            wheel_left_b,
            car_body,
            speed * (radius_r / radius_l) if radius_l < radius_r else speed,
        ),
        pymunk.SimpleMotor(
            wheel_right_b,
            car_body,
            speed * (radius_l / radius_r) if radius_r < radius_l else speed,
        ),
    )
    max = 100000
    m1.collide_bodies = False
    m2.collide_bodies = False

    space.add(m1, m2)
    return car_shape

small_wheel, medium_wheel, large_wheel = (
    wheels(10, (window, black, (700, 400), 10)),
    wheels(20, (window, black, (770, 400), 20)),
    wheels(30, (window, black, (860, 400), 30)),
)

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

    total_time = 0

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
