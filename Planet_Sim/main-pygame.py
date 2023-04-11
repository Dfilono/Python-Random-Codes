import pygame as pg
import math

# Initialize pygame
pg.init()

# Global Variables
FPS = 60
WIDTH, HEIGHT = 1920, 1040 
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Solar System Simulation")

# Colors
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = [80, 80, 80]
GREEN = (0, 160, 0)
ORANGE = (255, 165, 0)
DARK_YELLOW = (139, 128, 0)
LIGHT_BLUE = (173, 216, 230)
NEPTUNE = (44, 78, 81)
LIGHT_PURPLE = (203, 195, 227)

FONT = pg.font.SysFont("comicsans", 16)

# Planet data
planet_mass = { # in kg
    'sun' : 1.9891e30,
    'mercury' : 3.285e23,
    'venus' : 4.867e24,
    'earth' : 5.97219e24,
    'mars' : 6.39e23,
    'jupiter' : 1.898e27,
    'saturn' : 5.683e26,
    'uranus' : 8.681e25,
    'neptune' : 1.0241e26,
    'pluto' : 1.309e22
}

planet_relative_radius = {
    'sun' : 30,
    'mercury' : 3,
    'venus' : 9,
    'earth' : 10,
    'mars' : 5,
    'jupiter' : 20,
    'saturn' : 17,
    'uranus' : 15,
    'neptune' : 14,
    'pluto' : 1
}

planet_vel = { # m/s (y velocites)
    'mercury' : -47.4 * 1000,
    'venus' : -35.02 * 1000,
    'earth' : -29.783 * 1000,
    'mars' : -24.077 * 1000,
    'jupiter' : -13.07 * 1000,
    'saturn' : -9.69 * 1000,
    'uranus' : -6.81 * 1000,
    'neptune' : -5.43 * 1000,
    'pluto' : -4.74 * 1000
}

class Planet:
    # Class variables
    AU = 149.6e6 * 1000 # astronomical units (in meters) (~distance from earth to sun)
    G = 6.67428e-11 # gravity constant
    TIMESTEP = 3600 * 24 # seconds in a day
    SCALE = input('Enter a number between 0 and 500, with 0 being most zoomed out, and 500 being most zoomed in: ')

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.scale = int(self.SCALE) / self.AU # 1 AU == 100 pixels

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.scale + WIDTH / 2
        y = self.y * self.scale + HEIGHT / 2
        
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                a, b = point
                a = a * self.scale + WIDTH / 2
                b = b * self.scale + HEIGHT / 2
                updated_points.append((a, b))

            pg.draw.lines(win, self.color, False, updated_points, 2)

        pg.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f'{round(self.distance_to_sun/1000/1000/1000, 1)}Gm', 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height() /2))

    def force_of_attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.force_of_attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        

def main():
    run = True
    clock = pg.time.Clock()

    # Planets
    sun = Planet(0, 0, planet_relative_radius['sun'], YELLOW, planet_mass['sun'])
    sun.sun = True

    mercury = Planet(0.387*Planet.AU, 0, planet_relative_radius['mercury'], GREY, planet_mass['mercury'])
    mercury.y_vel = planet_vel['mercury']

    venus = Planet(0.723*Planet.AU, 0, planet_relative_radius['venus'], GREEN, planet_mass['venus'])
    venus.y_vel = planet_vel['venus']

    earth = Planet(1*Planet.AU, 0, planet_relative_radius['earth'], BLUE, planet_mass['earth'])
    earth.y_vel = planet_vel['earth']

    mars = Planet(1.524*Planet.AU, 0, planet_relative_radius['mars'], RED, planet_mass['mars'])
    mars.y_vel = planet_vel['mars']

    jupiter = Planet(5.2 * Planet.AU, 0, planet_relative_radius['jupiter'], ORANGE, planet_mass['jupiter'])
    jupiter.y_vel = planet_vel['jupiter']

    saturn = Planet(9.5 * Planet.AU, 0, planet_relative_radius['saturn'], DARK_YELLOW, planet_mass['saturn'])
    saturn.y_vel = planet_vel['saturn']

    uranus = Planet(19.8 * Planet.AU, 0, planet_relative_radius['uranus'], LIGHT_BLUE, planet_mass['uranus'])
    uranus.y_vel = planet_vel['uranus']

    neptune = Planet(30 * Planet.AU, 0, planet_relative_radius['neptune'], NEPTUNE, planet_mass['neptune'])
    neptune.y_vel = planet_vel['neptune']

    pluto = Planet(39 * Planet.AU, 0, planet_relative_radius['pluto'], LIGHT_PURPLE, planet_mass['pluto'])
    pluto.y_vel = planet_vel['pluto']

    planets = [pluto, neptune, uranus, saturn, jupiter, mars, earth, venus, mercury, sun]

    while run:
        clock.tick(FPS)
        WIN.fill(BACKGROUND)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        for planet in planets:
            planet.update(planets)
            planet.draw(WIN)
        
        pg.display.update()

    pg.quit()

main()