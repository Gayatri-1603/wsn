
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import random

# Simulation Parameters
N = 8               # Number of nodes
AREA = 10           # Area size
SLOTS = 15          # Total time slots before auto stop
TX_TIME = 3         # Transmission duration
P_GEN = 0.15        # Packet generation probability

# Initialize Network
np.random.seed(1)
random.seed(1)

positions = np.random.rand(N, 2) * AREA
bs_pos = np.array([AREA / 2, AREA / 2])

states = ["idle"] * N
queue = [0] * N
tx_remaining = [0] * N
lines = [None] * N

# Colors for visualization
colors = {
    "idle": "blue",
    "transmitting": "red",
    "waiting": "orange"
}

# Statistics Counters
total_transmissions = 0
total_collisions = 0
total_success = 0

# Visualization Setup
fig, ax = plt.subplots(figsize=(6, 6))

ax.set_xlim(0, AREA)
ax.set_ylim(0, AREA)
ax.set_title("MAC Protocol Simulation (Auto Stop at 15 Slots)")

ax.scatter(
    bs_pos[0], bs_pos[1],
    s=200, marker="*", color="black",
    label="Base Station"
)

nodes_plot = ax.scatter(
    positions[:, 0], positions[:, 1], s=100
)

labels = [
    ax.text(
        positions[i, 0] + 0.2,
        positions[i, 1] + 0.2,
        "",
        fontsize=8
    )
    for i in range(N)
]

ax.legend(loc="upper right")

# Simulation Logic per Slot
def update(frame):
    global queue, states, tx_remaining, lines
    global total_transmissions, total_collisions, total_success

    # Auto-stop after defined slots
    if frame >= SLOTS:
        print("\nSimulation completed.")
        print("----- SUMMARY -----")
        print(f"Total time slots: {SLOTS}")
        print(f"Total transmission attempts: {total_transmissions}")
        print(f"Successful transmissions: {total_success}")
        print(f"Collisions: {total_collisions}")

        plt.close(fig)
        return nodes_plot,

    print(f"\n--- Time Slot {frame + 1} ---")

    # Packet Generation
    for i in range(N):
        if random.random() < P_GEN:
            queue[i] += 1

    # Handle Ongoing Transmissions
    for i in range(N):
        if states[i] == "transmitting":
            tx_remaining[i] -= 1

            if tx_remaining[i] <= 0:
                print(f"Node {i} finished transmission successfully.")

                queue[i] = max(0, queue[i] - 1)
                states[i] = "idle"
                total_success += 1

                if lines[i] is not None:
                    lines[i].remove()
                    lines[i] = None

    # Find Nodes Ready to Send
    ready_nodes = [
        i for i in range(N)
        if queue[i] > 0 and states[i] == "idle"
    ]

    # Handle Transmissions or Collisions
    if len(ready_nodes) == 1:
        i = ready_nodes[0]

        states[i] = "transmitting"
        tx_remaining[i] = TX_TIME
        total_transmissions += 1

        print(f"Node {i} is transmitting to the base station.")

        lines[i] = ax.plot(
            [positions[i, 0], bs_pos[0]],
            [positions[i, 1], bs_pos[1]],
            "r--",
            alpha=0.7
        )[0]

    elif len(ready_nodes) > 1:
        total_collisions += 1

        print(
            f"Collision! Nodes {ready_nodes} "
            "tried to transmit together."
        )

        for i in ready_nodes:
            states[i] = "waiting"

            if lines[i] is not None:
                lines[i].remove()
                lines[i] = None

    # Random Backoff Recovery
    for i in range(N):
        if states[i] == "waiting" and random.random() < 0.3:
            states[i] = "idle"

    # Update Visualization
    node_colors = [
        colors.get(states[i], "gray")
        for i in range(N)
    ]

    nodes_plot.set_color(node_colors)

    for i, t in enumerate(labels):
        t.set_text(
            f"{i}:{states[i][0].upper()} q={queue[i]}"
        )

    ax.set_xlabel(f"Time Slot: {frame + 1}")

    return nodes_plot, *labels

# Run Animation
ani = FuncAnimation(
    fig,
    update,
    frames=SLOTS + 1,
    interval=500,
    repeat=False,
    blit=False
)

plt.tight_layout()
plt.show()
