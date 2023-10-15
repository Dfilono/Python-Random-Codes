import pygame as pg
import math

pg.init()

# Constants
WIDTH, HEIGHT = 800, 600
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Gravitational Slingshot Simulation")

PLANET_MASS = 100
OBJ_MASS = 5
GRAVITY = 5
FPS = 60
PLANET_RADIUS = 50
OBJ_RADIUS = 5
VEL_SCALE = 100

# Import Images
BG = pg.transform.scale(pg.image.load('background.jpg'), (WIDTH, HEIGHT))
PLANET = pg.transform.scale(pg.image.load('jupiter.png'), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(PLANET, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS))

class MovingObj:
    def __init__(self, x, y, velX, velY, mass):
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.mass = mass

    def draw(self):
        pg.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_RADIUS)

    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (GRAVITY * self.mass * planet.mass) / distance**2

        acc = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        accX = acc * math.cos(angle)
        accY = acc * math.sin(angle)

        self.velX += accX
        self.velY += accY

        self.x += self.velX
        self.y += self.velY

def createObj(loc, mouse):
    tX, tY = loc
    mX, mY = mouse

    velX = (mX - tX) / VEL_SCALE
    velY = (mY - tY) / VEL_SCALE

    obj = MovingObj(tX, tY, velX, velY, OBJ_MASS)
    return obj

def main():
    run = True
    clock = pg.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)

    objs = []
    tempObjPos = None

    while run:
        clock.tick(FPS)

        mousePos = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if tempObjPos:
                    obj = createObj(tempObjPos, mousePos)
                    objs.append(obj)
                    tempObjPos = None
                else:
                    tempObjPos = mousePos

        win.blit(BG, (0, 0))
        
        if tempObjPos:
            pg.draw.line(win, WHITE, tempObjPos, mousePos, 2)
            pg.draw.circle(win, RED, tempObjPos, OBJ_RADIUS)

        for i in objs[:]:
            i.draw()
            i.move(planet)
            
            offScreen = i.x < 0 or i.x > WIDTH or i.y < 0 or i.y > HEIGHT
            collided = math.sqrt((i.x - planet.x)**2 + (i.y - planet.y)**2) <= PLANET_RADIUS

            if offScreen or collided:
                objs.remove(i)

        planet.draw()

        pg.display.update()

    pg.quit()

if __name__ == "__main__":
    main()