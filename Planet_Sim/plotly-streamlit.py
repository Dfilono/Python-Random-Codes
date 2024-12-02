import numpy as np
import math
import plotly.graph_objects as go
import streamlit as st

# Constants and helper functions (your code)
planet_mass = { 
    'sun': 1.9891e30, 'mercury': 3.285e23, 'venus': 4.867e24,
    'earth': 5.97219e24, 'mars': 6.39e23, 'jupiter': 1.898e27,
    'saturn': 5.683e26, 'uranus': 8.681e25, 'neptune': 1.0241e26, 'pluto': 1.309e22
}

planet_radius = { 
    'sun': 180000 * 1000, 'mercury': 2439.7 * 1000, 'venus': 6051.8 * 1000,
    'earth': 6371 * 1000, 'mars': 3389.5 * 1000, 'jupiter': 69911 * 1000,
    'saturn': 58232 * 1000, 'uranus': 25362 * 1000, 'neptune': 24622 * 1000, 'pluto': 1188.3 * 1000
}

planet_distance_from_sun = {
    'sun': 0, 'mercury': 57.9, 'venus': 108.2, 'earth': 149.6, 'mars': 227.9,
    'jupiter': 778.6, 'saturn': 1433.5, 'uranus': 2872.5, 'neptune': 4495.1, 'pluto': 5906.38
}

# Function to create spheres
def spheres(size, clr, dist=0):
    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    x0 = dist + size * np.outer(np.cos(theta), np.sin(phi))
    y0 = size * np.outer(np.sin(theta), np.sin(phi))
    z0 = size * np.outer(np.ones(100), np.cos(phi))
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, clr], [1, clr]])
    trace.update(showscale=False)
    return trace

# Function to create orbits
def orbits(dist, offset=0, clr='white', w=2):
    x_coords = [(round(np.cos(math.radians(i)), 5)) * dist + offset for i in range(0, 361)]
    y_coords = [(round(np.sin(math.radians(i)), 5)) * dist for i in range(0, 361)]
    z_coords = [0 for _ in range(0, 361)]
    trace = go.Scatter3d(x=x_coords, y=y_coords, z=z_coords, marker=dict(size=0.1), line=dict(color=clr, width=w))
    return trace

# Streamlit app
st.title("Solar System Simulator")
st.write("This is a 3D simulation of the solar system using Plotly.")

# Interactive sliders
distance_scale = st.slider("Scale Distance from Sun (AU)", 0.1, 1.0, 0.5)
planet_distance = {k: v * distance_scale for k, v in planet_distance_from_sun.items()}

# Create speheres for planets and orbits
diameter_km = {key: value * 2 / 1000 for (key, value) in planet_radius.items()}
diameter = {k: (v / diameter_km['earth']) * 2 for (k, v) in diameter_km.items()}
traces = [
    spheres(diameter['sun'], '#ffff00', planet_distance['sun']),
    spheres(diameter['mercury'], '#87877d', planet_distance['mercury']),
    spheres(diameter['venus'], '#d23100', planet_distance['venus']),
    spheres(diameter['earth'], '#325bff', planet_distance['earth']),
    spheres(diameter['mars'], '#b20000', planet_distance['mars']),
    spheres(diameter['jupiter'], '#ebebd2', planet_distance['jupiter']),
    spheres(diameter['saturn'], '#ebcd82', planet_distance['saturn']),
    spheres(diameter['uranus'], '#37ffda', planet_distance['uranus']),
    spheres(diameter['neptune'], '#2500ab', planet_distance['neptune']),
    spheres(diameter['pluto'], '#fff1d5', planet_distance['pluto']),
    orbits(planet_distance['mercury']),
    orbits(planet_distance['venus']),
    orbits(planet_distance['earth']),
    orbits(planet_distance['mars']),
    orbits(planet_distance['jupiter']),
    orbits(planet_distance['saturn']),
    orbits(planet_distance['uranus']),
    orbits(planet_distance['neptune']),
    orbits(planet_distance['pluto'])
]

# Plot
fig = go.Figure(data=traces)
fig.update_layout(
    title="Solar System",
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor='black',
    scene=dict(
        xaxis=dict(backgroundcolor='black', color='white', gridcolor='gray'),
        yaxis=dict(backgroundcolor='black', color='white', gridcolor='gray'),
        zaxis=dict(backgroundcolor='black', color='white', gridcolor='gray'),
    )
)
st.plotly_chart(fig)
