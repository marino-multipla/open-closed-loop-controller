import matplotlib.pyplot as plt
import numpy as np

# Simulation parameters
target_position = 10
initial_position = 0
steps = 40  # increased to give closed-loop time to converge


# --- OPEN LOOP CONTROLLER ---
def open_loop_control():
    planned_action = 0.5  # assumes perfect movement
    position = initial_position
    trajectory = [position]

    for _ in range(steps):
        # Add execution error/noise to simulate real-world mismatch
        actual_action = planned_action * np.random.normal(0.9, 0.05)
        position += actual_action
        trajectory.append(position)

    return trajectory


# --- CLOSED LOOP CONTROLLER ---
def closed_loop_control():
    position = initial_position
    trajectory = [position]

    for _ in range(steps):
        error = target_position - position
        action = 0.3 * error  # Higher gain to reach target faster
        position += action
        trajectory.append(position)

    return trajectory

print("""
Key Changes:
  - Introduce noise or a mismatch in the open-loop assumption
    (e.g., robot doesn't move exactly as planned).
  - Increase gain in the closed-loop controller to make it more responsive.

What We Want to Show:
  - Open-loop suffers when reality doesn't match its assumptions
    (e.g., motor is weak or noisy).
  - Closed-loop adapts and still reaches the target — that's the power of feedback.

What You’ll Observe Now:
  - Open-loop will deviate due to noise or slight underperformance. It doesn’t recover.
  - Closed-loop will automatically correct itself at every step and converge reliably to the target.
""")


# Run both controllers
np.random.seed(42)  # for reproducibility
open_loop_traj = open_loop_control()
closed_loop_traj = closed_loop_control()

# Plotting
plt.plot(open_loop_traj, label='Open Loop (with error)', linestyle='--')
plt.plot(closed_loop_traj, label='Closed Loop (feedback)', linestyle='-')
plt.axhline(target_position, color='gray', linestyle=':', label='Target')
plt.xlabel('Time Step')
plt.ylabel('Position')
plt.title('Open-loop vs Closed-loop Controller (with noise)')
plt.legend()
plt.grid(True)
plt.show()
