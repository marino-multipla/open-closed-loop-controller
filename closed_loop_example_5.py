import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.animation import FuncAnimation, PillowWriter

# Settings
initial_pos = np.array([0.0, 0.0])
target_pos = np.array([10.0, 10.0])
steps = 100
WIND_VECTOR = np.array([0.05, -0.02])

OBSTACLES = [
    {"center": np.array([5.0, 5.0]), "radius": 1.5},
    {"center": np.array([7.0, 8.0]), "radius": 1.0}
]


def closed_loop_with_orientation():
    pos = initial_pos.copy()
    theta = 0.0
    velocity = 0.5
    trajectory = [pos.copy()]
    headings = [theta]

    for _ in range(steps):
        to_target = target_pos - pos
        angle_to_target = np.arctan2(to_target[1], to_target[0])
        angle_diff = np.arctan2(np.sin(angle_to_target - theta), np.cos(angle_to_target - theta))
        theta += 0.1 * angle_diff

        move = np.array([velocity * np.cos(theta), velocity * np.sin(theta)]) + WIND_VECTOR
        pos += move

        trajectory.append(pos.copy())
        headings.append(theta)

    return np.array(trajectory), headings


# Run controller
trajectory, headings = closed_loop_with_orientation()

# Setup plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1, 12)
ax.set_ylim(-2, 12)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Closed-loop control with heading and wind")

# Plot target and obstacles
ax.plot(target_pos[0], target_pos[1], 'bo', label='Target')
for obs in OBSTACLES:
    ax.add_patch(Circle(obs["center"], obs["radius"], color='gray', alpha=0.3))

# Robot and heading
robot_dot, = ax.plot([], [], 'ro', markersize=6, label='Robot')
trajectory_line, = ax.plot([], [], 'r-', alpha=0.6, linewidth=1)
arrow = FancyArrowPatch((0, 0), (0, 0), color='red', arrowstyle='->', mutation_scale=15)
ax.add_patch(arrow)

positions = []

def init():
    robot_dot.set_data([], [])
    trajectory_line.set_data([], [])
    arrow.set_positions((0, 0), (0, 0))
    return robot_dot, trajectory_line, arrow

def update(frame):
    x, y = trajectory[frame]
    theta = headings[frame]

    robot_dot.set_data([x], [y])
    positions.append((x, y))
    xs, ys = zip(*positions)
    trajectory_line.set_data(xs, ys)

    # Update arrow
    dx, dy = 0.8 * np.cos(theta), 0.8 * np.sin(theta)
    arrow.set_positions((x, y), (x + dx, y + dy))
    return robot_dot, trajectory_line, arrow

ani = FuncAnimation(fig, update, frames=len(trajectory), init_func=init, blit=True, interval=100)

# Save as GIF
ani.save("robot_simulation_5.gif", writer=PillowWriter(fps=10))
print("✅ Saved as 'robot_simulation_5.gif'")
