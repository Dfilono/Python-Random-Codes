import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Helper functions
def spheres(size, clr, dist=0):
    theta = np.linspace(0, 2 * np.pi, 50)  # Longitude
    phi = np.linspace(0, np.pi, 50)        # Latitude
    x0 = dist + size * np.outer(np.sin(phi), np.cos(theta))
    y0 = size * np.outer(np.sin(phi), np.sin(theta))
    z0 = size * np.outer(np.cos(phi), np.ones_like(theta))
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, clr], [1, clr]], showscale=False)
    return trace

def orbits(dist, clr='white', w=2):
    theta = np.linspace(0, 2 * np.pi, 361)
    x_coords = dist * np.cos(theta)
    y_coords = dist * np.sin(theta)
    z_coords = np.zeros_like(theta)
    trace = go.Scatter3d(x=x_coords, y=y_coords, z=z_coords, marker=dict(size=0.1), line=dict(color=clr, width=w))
    return trace

def calculate_aspect_ratio(x, y, z):
    range_x = max(x) - min(x)
    range_y = max(y) - min(y)
    range_z = max(z) - min(z)
    max_range = max(range_x, range_y, range_z)
    return dict(x=range_x / max_range, y=range_y / max_range, z=range_z / max_range)

# Streamlit app
st.title("Solar System Simulator")
st.write("Explore a simplified 3D simulation of the solar system!")

# Interactive scaling slider
distance_scaling_factor = st.slider("Scale Distance from Sun", 0.01, 1.0, 0.1)

# Constants for planets
planet_radius = {'sun': 10, 'mercury': 0.4, 'venus': 0.95, 'earth': 1, 'mars': 0.5, 
                 'jupiter': 11, 'saturn': 9.5, 'uranus': 4, 'neptune': 3.9, 'pluto': 0.18}
planet_distance = {'mercury': 57.9, 'venus': 108.2, 'earth': 149.6, 'mars': 227.9,
                   'jupiter': 778.6, 'saturn': 1433.5, 'uranus': 2872.5, 'neptune': 4495.1, 'pluto': 5906.38}
planet_distance_scaled = {k: v * distance_scaling_factor for k, v in planet_distance.items()}

# Create traces for planets and orbits
traces = [
    spheres(planet_radius['sun'], '#ffff00', 0),  # Sun
    spheres(planet_radius['mercury'], '#87877d', planet_distance_scaled['mercury']),  # Mercury
    spheres(planet_radius['venus'], '#d23100', planet_distance_scaled['venus']),  # Venus
    spheres(planet_radius['earth'], '#325bff', planet_distance_scaled['earth']),  # Earth
    spheres(planet_radius['mars'], '#b20000', planet_distance_scaled['mars']),  # Mars
    spheres(planet_radius['jupiter'], '#ebebd2', planet_distance_scaled['jupiter']),  # Jupiter
    spheres(planet_radius['saturn'], '#ebcd82', planet_distance_scaled['saturn']),  # Saturn
    spheres(planet_radius['uranus'], '#37ffda', planet_distance_scaled['uranus']),  # Uranus
    spheres(planet_radius['neptune'], '#2500ab', planet_distance_scaled['neptune']),  # Neptune
    spheres(planet_radius['pluto'], '#fff1d5', planet_distance_scaled['pluto']),  # Pluto,
    orbits(planet_distance_scaled['mercury']),
    orbits(planet_distance_scaled['venus']),
    orbits(planet_distance_scaled['earth']),
    orbits(planet_distance_scaled['mars']),
    orbits(planet_distance_scaled['jupiter']),
    orbits(planet_distance_scaled['saturn']),
    orbits(planet_distance_scaled['uranus']),
    orbits(planet_distance_scaled['neptune']),
    orbits(planet_distance_scaled['pluto']),
]

# Collect data points for aspect ratio
x_values, y_values, z_values = [], [], []
for trace in traces:
    if isinstance(trace, go.Surface):
        x_values.extend(trace.x.flatten())
        y_values.extend(trace.y.flatten())
        z_values.extend(trace.z.flatten())
    elif isinstance(trace, go.Scatter3d):
        x_values.extend(trace.x)
        y_values.extend(trace.y)
        z_values.extend(trace.z)

# Calculate aspect ratio
aspect_ratio = calculate_aspect_ratio(x_values, y_values, z_values)

# Plot the figure
fig = go.Figure(data=traces)
fig.update_layout(
    title="Solar System Simulation",
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor='black',
    scene=dict(
        aspectmode="manual",
        aspectratio=aspect_ratio,  # Apply calculated aspect ratio
        xaxis=dict(backgroundcolor="black", color="white", gridcolor="gray"),
        yaxis=dict(backgroundcolor="black", color="white", gridcolor="gray"),
        zaxis=dict(backgroundcolor="black", color="white", gridcolor="gray"),
    )
)
st.plotly_chart(fig)
