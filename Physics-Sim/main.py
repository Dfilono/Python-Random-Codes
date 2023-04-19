import pygame as pg
import pymunk as pk
import pymunk.pygame_util
import math

pg.init()

# Global vars
WIDTH, HEIGHT = 1000, 800
win = pg.display.set_mode((WIDTH, HEIGHT))

# Draw function
def draw(space, window, draw_options, line):
    window.fill("white")

    if line:
        pg.draw.line(window, "black", line[0], line[1], 3)

    space.debug_draw(draw_options)

    pg.display.update()

def create_ball(space, radius, mass, pos):
    body = pk.Body(body_type = pk.Body.STATIC)
    body.position = pos # position of body
    shape = pk.Circle(body, radius) # shape of body
    shape.mass = mass # mass of body
    shape.color = (255, 0, 0, 100) # color of body (R, G, B alpha)
    shape.elasticity = 0.9
    shape.friction = 0.4
    space.add(body, shape)
    
    return shape

def set_boundaries(space, w, h):
    rects = [
        [(w / 2, h - 10), (w, 20)], # Floor
        [(w / 2, 10), (w, 20)], # Top
        [(10, h / 2), (20, h)], # Left wall
        [(w - 10, h / 2), (20, h)] # Right wall
    ]

    for pos, size in rects:
        body = pk.Body(body_type = pk.Body.STATIC)
        body.position = pos
        shape = pk.Poly.create_box(body, size)
        shape.color = (0, 0, 255, 100)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0]))

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def create_structure(space, w, h):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(600, h - 120), (40, 200), BROWN, 100],
        [(900, h - 120), (40, 200), BROWN, 100],
        [(750, h - 240), (340, 40), BROWN, 150],
    ]

    for pos, size, color, mass in rects:
        body = pk.Body()
        body.position = pos
        shape = pk.Poly.create_box(body, size, radius = 1)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        space.add(body, shape)

def create_swinging_ball(space):
    rotation_center_body = pk.Body(body_type = pk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    body = pk.Body()
    body.position = (300, 300)
    line = pk.Segment(body, (0, 0), (255, 0), 5)
    circle = pk.Circle(body, 40, (255, 0))
    line.friction = 1
    circle.friction = 1
    line.mass = 8
    circle.mass = 30
    circle.elasticity = 0.95

    rotation_center_joint = pk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    space.add(circle, line, body, rotation_center_joint)

# Game loop
def run(window, w, h):
    on = True
    clock = pg.time.Clock()
    fps = 60
    dt = 1 / fps

    # Pymunk space init
    space = pk.Space()
    space.gravity = (0, 981)

    set_boundaries(space, w, h)
    create_structure(space, w, h)
    create_swinging_ball(space)
    
    # Drawing the sim
    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None
    ball = None
    draw_line = None

    while on:
        line = None
        if ball and draw_line:
            line = [pressed_pos, pg.mouse.get_pos()]
        # Event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                on = False

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if not ball:
                    pressed_pos = pg.mouse.get_pos()
                    ball = create_ball(space, 30, 10, pressed_pos)
                    draw_line = True

                elif pressed_pos and event.button == 1 and draw_line:
                    ball.body.body_type = pk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 100
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    draw_line = False

                elif pressed_pos and event.button == 1 and not draw_line:
                    ball.body.apply_impulse_at_local_point((10000, 0), (0, 0))
                    
                
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                pressed_pos = None
                space.remove(ball, ball.body)
                ball = None
                line = None
                    
        
        draw(space, window, draw_options, line)

        # FPS control
        space.step(dt)
        clock.tick(fps)

    pg.quit()

if __name__ == "__main__":
    run(win, WIDTH, HEIGHT)