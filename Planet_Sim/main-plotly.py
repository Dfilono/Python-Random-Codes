import numpy as np
import math
import plotly.graph_objects as go

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

planet_radius = { # in meters
    'sun' : 180000 * 1000, # True Value = 6.96e5 * 1000,
    'mercury' : 2439.7 * 1000,
    'venus' : 6051.8 * 1000,
    'earth' : 6371 * 1000,
    'mars' : 3389.5 * 1000,
    'jupiter' : 69911 * 1000,
    'saturn' : 58232 * 1000,
    'uranus' : 25362 * 1000,
    'neptune' : 24622 * 1000,
    'pluto' : 1188.3 * 1000
}

planet_distance_from_sun = { # millions of km
    'sun' : 0,
    'mercury' : 57.9,
    'venus' : 108.2,
    'earth' : 149.6,
    'mars' : 227.9,
    'jupiter' : 778.6,
    'saturn' : 1433.5,
    'uranus' : 2872.5,
    'neptune' : 4495.1,
    'pluto' :  5906.38
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

# define spheres
def spheres(size, clr, dist = 0):
    # set 100 points, first do angles
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, np.pi, 100)

    # set up coordiantes for points on sphere
    x0 = dist + size * np.outer(np.cos(theta), np.sin(phi))
    y0 = size * np.outer(np.sin(theta), np.sin(phi))
    z0 = size * np.outer(np.ones(100), np.cos(phi))

    # set up trace
    trace = go.Surface(x = x0, y = y0, z = z0, colorscale=[[0, clr], [1, clr]])
    trace.update(showscale = False)

    return trace


def orbits(dist, offset = 0, clr = 'white', w = 2):
    # Init empty list fo eachs et of coords
    x_coords = []
    y_coords = []
    z_coords = []

    # Calculate coords
    for i in range(0, 361):
        x_coords = x_coords + [(round(np.cos(math.radians(i)), 5)) * dist + offset]
        y_coords = y_coords + [(round(np.sin(math.radians(i)), 5)) * dist]
        z_coords = z_coords + [0]

    trace = go.Scatter3d(x = x_coords, y = y_coords, z = z_coords, marker = dict(size = 0.1), line = dict(color = clr, width = w))
    
    return trace

def annotate(x_coord, z_coord, txt, x_pos = 'center'):
    msg = dict(showarrow = False, x = x_coord, y = 0, z = z_coord, text = txt, xanchor = x_pos, font = dict(color = 'white', size = 12))

    return msg

diameter_km = {key: value*2/1000 for (key, value) in planet_radius.items()}
diameter = {k:(v/diameter_km['earth'])*2 for (k, v) in diameter_km.items()}

# Create speheres for the Sun and planets
trace0 = spheres(diameter['sun'], '#ffff00', planet_distance_from_sun['sun']) # Sun
trace1 = spheres(diameter['mercury'], '#87877d', planet_distance_from_sun['mercury']) # Mercury
trace2 = spheres(diameter['venus'], '#d23100', planet_distance_from_sun['venus']) # Venus
trace3 = spheres(diameter['earth'], '#325bff', planet_distance_from_sun['earth']) # Earth
trace4 = spheres(diameter['mars'], '#b20000', planet_distance_from_sun['mars']) # Mars
trace5 = spheres(diameter['jupiter'], '#ebebd2', planet_distance_from_sun['jupiter']) # Jupiter
trace6 = spheres(diameter['saturn'], '#ebcd82', planet_distance_from_sun['saturn']) # Saturn
trace7 = spheres(diameter['uranus'], '#37ffda', planet_distance_from_sun['uranus']) # Uranus
trace8 = spheres(diameter['neptune'], '#2500ab', planet_distance_from_sun['neptune']) # Neptune
trace9 = spheres(diameter['pluto'], '#fff1d5', planet_distance_from_sun['pluto']) # Pluto

# Orbit traces
trace11 = orbits(planet_distance_from_sun['mercury'])
trace12 = orbits(planet_distance_from_sun['venus'])
trace13 = orbits(planet_distance_from_sun['earth'])
trace14 = orbits(planet_distance_from_sun['mars'])
trace15 = orbits(planet_distance_from_sun['jupiter'])
trace16 = orbits(planet_distance_from_sun['saturn'])
trace17 = orbits(planet_distance_from_sun['uranus'])
trace18 = orbits(planet_distance_from_sun['neptune'])
trace19 = orbits(planet_distance_from_sun['pluto'])

# Rings for Saturn
trace161 = orbits(23, planet_distance_from_sun['saturn'], '#827962', 3) 
trace162 = orbits(24, planet_distance_from_sun['saturn'], '#827962', 3) 
trace163 = orbits(25, planet_distance_from_sun['saturn'], '#827962', 3)
trace164 = orbits(26, planet_distance_from_sun['saturn'], '#827962', 3) 
trace165 = orbits(27, planet_distance_from_sun['saturn'], '#827962', 3) 
trace166 = orbits(28, planet_distance_from_sun['saturn'], '#827962', 3)

layout = go.Layout(title = 'Solar System', showlegend = False, margin = dict(l = 0, r = 0, t = 0, b = 0),
                   paper_bgcolor = 'black',
                   scene = dict(xaxis = dict(title = 'Distance from the Sun',
                                             titlefont_color = 'black',
                                             range = [-9000, 9000],
                                             backgroundcolor = 'black',
                                             color = 'black',
                                             gridcolor = 'black'),
                                yaxis = dict(title = 'Distance from the Sun',
                                             titlefont_color = 'black',
                                             range = [-9000, 9000],
                                             backgroundcolor = 'black',
                                             color = 'black',
                                             gridcolor = 'black'),
                                zaxis = dict(title = '',
                                             range = [-9000, 9000],
                                             backgroundcolor = 'black',
                                             color = 'white',
                                             gridcolor = 'black'),
                                annotations = [
                                    annotate(planet_distance_from_sun['sun'], 40, 'Sun', x_pos = 'left'),
                                    annotate(planet_distance_from_sun['mercury'], 5, 'Mercury'),
                                    annotate(planet_distance_from_sun['venus'], 9, 'Venus'),
                                    annotate(planet_distance_from_sun['earth'], 9, 'Earth'),
                                    annotate(planet_distance_from_sun['mars'], 7, 'Mars'),
                                    annotate(planet_distance_from_sun['jupiter'], 30, 'Jupiter'),
                                    annotate(planet_distance_from_sun['saturn'], 28, 'Saturn'),
                                    annotate(planet_distance_from_sun['uranus'], 20, 'Uranus'),
                                    annotate(planet_distance_from_sun['neptune'], 20, 'Neptune'),
                                    annotate(planet_distance_from_sun['pluto'], 5, 'Pluto')
                                ]
                            )
                    )

fig = go.Figure(data = [trace0, trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8,
                        trace11, trace12, trace13, trace14, trace15, trace16, trace17, trace18, trace19,
                        trace161, trace162, trace163, trace164, trace165, trace166],
                layout = layout)

fig.show()