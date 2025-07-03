import matplotlib.pyplot as plt

# Environment parameters
target_position = 10
initial_position = 0
steps = 20


# --- OPEN LOOP CONTROLLER ---
def open_loop_control():
    # Fixed action plan: assume +0.5 per step will get us to target
    planned_actions = [0.5] * steps
    position = initial_position
    trajectory = [position]

    for action in planned_actions:
        position += action
        trajectory.append(position)

    return trajectory


# --- CLOSED LOOP CONTROLLER ---
def closed_loop_control():
    position = initial_position
    trajectory = [position]

    for _ in range(steps):
        # Proportional controller (simple feedback)
        error = target_position - position
        action = 0.1 * error  # gain of 0.1
        position += action
        trajectory.append(position)

    return trajectory


print("The example uses a perfectly tuned open-loop plan (0.5 steps × 20 = 10), so it hits the target exactly. Meanwhile, the closed-loop controller uses a low gain (0.1), which makes it converge slowly, and in just 20 steps it doesn't reach the target. That setup unintentionally favors the open-loop system — which defeats the point of the example.")

# Run both controllers
open_loop_traj = open_loop_control()
closed_loop_traj = closed_loop_control()

# Plotting
plt.plot(open_loop_traj, label='Open Loop')
plt.plot(closed_loop_traj, label='Closed Loop')
plt.axhline(target_position, color='gray', linestyle='--', label='Target')
plt.xlabel('Time Step')
plt.ylabel('Position')
plt.title('Open-loop vs Closed-loop Controller')
plt.legend()
plt.grid(True)
plt.show()
