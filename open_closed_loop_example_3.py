import matplotlib.pyplot as plt
import numpy as np

# Simulation setup
target_position = 10
initial_position = 0
steps = 40

def open_loop_control():
    planned_action = 0.5
    position = initial_position
    trajectory = [position]
    errors = [target_position - position]

    for _ in range(steps):
        actual_action = planned_action * np.random.normal(0.9, 0.05)
        position += actual_action
        trajectory.append(position)
        errors.append(target_position - position)

    return trajectory, errors

def closed_loop_control():
    position = initial_position
    trajectory = [position]
    errors = [target_position - position]

    for _ in range(steps):
        error = target_position - position
        action = 0.3 * error
        position += action
        trajectory.append(position)
        errors.append(target_position - position)

    return trajectory, errors

print("""

 What You’ll See:

    Open-loop error may increase or drift over time.

    Closed-loop error decays toward zero as it self-corrects.
""")

# Run simulations
np.random.seed(42)
open_loop_traj, open_loop_errors = open_loop_control()
closed_loop_traj, closed_loop_errors = closed_loop_control()

# Plot position
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(open_loop_traj, label='Open Loop')
plt.plot(closed_loop_traj, label='Closed Loop')
plt.axhline(target_position, color='gray', linestyle=':')
plt.title('Position Over Time')
plt.xlabel('Time Step')
plt.ylabel('Position')
plt.legend()
plt.grid(True)

# Plot error
plt.subplot(1, 2, 2)
plt.plot(open_loop_errors, label='Open Loop Error')
plt.plot(closed_loop_errors, label='Closed Loop Error')
plt.axhline(0, color='gray', linestyle=':')
plt.title('Error Over Time')
plt.xlabel('Time Step')
plt.ylabel('Error (Target - Position)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
