import matplotlib.pyplot as plt
import numpy as np

# Settings
initial_pos = np.array([0.0, 0.0])
target_pos = np.array([2.0, 10.0])
steps = 50
step_size = 0.3

def open_loop_control():
    direction = (target_pos - initial_pos)
    direction = direction / np.linalg.norm(direction)  # unit vector
    planned_action = direction * step_size

    pos = initial_pos.copy()
    trajectory = [pos.copy()]
    errors = [np.linalg.norm(target_pos - pos)]

    for _ in range(steps):
        # Add noise to simulate imperfect movement
        noise = np.random.normal(loc=0.0, scale=0.05, size=2)
        actual_action = planned_action + noise
        pos += actual_action
        trajectory.append(pos.copy())
        errors.append(np.linalg.norm(target_pos - pos))

    return np.array(trajectory), errors

def closed_loop_control():
    pos = initial_pos.copy()
    trajectory = [pos.copy()]
    errors = [np.linalg.norm(target_pos - pos)]

    for _ in range(steps):
        error_vec = target_pos - pos
        direction = error_vec / np.linalg.norm(error_vec)
        action = direction * step_size
        pos += action
        trajectory.append(pos.copy())
        errors.append(np.linalg.norm(target_pos - pos))

    return np.array(trajectory), errors

print("""
A basic 2D robot controller (no physics engine) that moves from an initial position toward a target (x, y) position.

We'll compare:

    Open-loop controller: Follows a fixed set of precomputed actions (no feedback).

    Closed-loop controller: Uses feedback at each step to steer toward the goal.

We’ll add noise to the open-loop controller to highlight how it drifts without correction, and we’ll plot both trajectories and the error (distance to goal) over time.

What You’ll See:

    Left plot: The open-loop trajectory drifts due to noise; the closed-loop trajectory adjusts and homes in on the goal.

    Right plot: Error decreases rapidly in the closed-loop case, but may stagnate or increase in the open-loop one.
      """)

# Run simulations
np.random.seed(42)
open_loop_traj, open_loop_errors = open_loop_control()
closed_loop_traj, closed_loop_errors = closed_loop_control()

# Plot trajectories
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(open_loop_traj[:, 0], open_loop_traj[:, 1], 'r--', label='Open Loop')
plt.plot(closed_loop_traj[:, 0], closed_loop_traj[:, 1], 'g-', label='Closed Loop')
plt.plot(target_pos[0], target_pos[1], 'bo', label='Target')
plt.title('2D Trajectory')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.axis('equal')
plt.grid(True)

# Plot error over time
plt.subplot(1, 2, 2)
plt.plot(open_loop_errors, 'r--', label='Open Loop Error')
plt.plot(closed_loop_errors, 'g-', label='Closed Loop Error')
plt.title('Distance to Target Over Time')
plt.xlabel('Time Step')
plt.ylabel('Euclidean Distance')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
