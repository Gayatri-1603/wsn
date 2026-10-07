import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
from matplotlib.animation import FuncAnimation

# -----------------------------
# MANET Configuration
# -----------------------------

N = 8                  # Number of nodes
R = 0.3                # Communication range
speed = 0.005         # Node movement speed

# Randomly select source and destination
src, dst = random.sample(range(N), 2)

# -----------------------------
# Initialize node positions
# and velocities
# -----------------------------

pos = {i: np.random.rand(2) for i in range(N)}

vel = {
    i: np.random.uniform(-1, 1, 2) * speed
    for i in range(N)
}

# -----------------------------
# Update node positions
# -----------------------------

def update_pos():

    for i in range(N):

        pos[i] += vel[i]

        # Bounce nodes back when
        # they reach the boundary
        for d in range(2):

            if pos[i][d] < 0 or pos[i][d] > 1:

                vel[i][d] *= -1

                pos[i][d] = np.clip(
                    pos[i][d],
                    0,
                    1
                )


# -----------------------------
# Create MANET graph
# -----------------------------

def graph():

    G = nx.Graph()

    # IMPORTANT:
    # Add all nodes even if
    # they have no connections
    G.add_nodes_from(range(N))

    for i in range(N):

        for j in range(i + 1, N):

            # Calculate distance between nodes
            distance = np.linalg.norm(
                pos[i] - pos[j]
            )

            # Create wireless link
            # if nodes are within range
            if distance <= R:

                G.add_edge(i, j)

    return G


# -----------------------------
# BFS Route Discovery
# -----------------------------

def path(G):

    from collections import deque

    # Make sure source and destination exist
    if src not in G or dst not in G:
        return []

    # BFS queue
    q = deque([src])

    # Parent dictionary
    p = {src: None}

    while q:

        n = q.popleft()

        for nb in G[n]:

            if nb not in p:

                p[nb] = n

                q.append(nb)

                # Destination found
                if nb == dst:

                    r = [dst]

                    # Reconstruct route
                    while r[-1] != src:

                        r.append(
                            p[r[-1]]
                        )

                    return r[::-1]

    # No route available
    return []


# -----------------------------
# Create animation window
# -----------------------------

fig, ax = plt.subplots()


# -----------------------------
# Animation function
# -----------------------------

def animate(f):

    # Move all nodes
    update_pos()

    # Create current network
    G = graph()

    # Find route using BFS
    p = path(G)

    # Clear previous frame
    ax.clear()

    # Set simulation area
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Remove axes
    ax.axis("off")

    # -------------------------
    # Draw network
    # -------------------------

    nx.draw(
        G,
        pos,
        node_color="skyblue",
        with_labels=True,
        ax=ax
    )

    # -------------------------
    # Draw source
    # Green = Source
    # -------------------------

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[src],
        node_color="green",
        node_size=500,
        ax=ax
    )

    # -------------------------
    # Draw destination
    # Red = Destination
    # -------------------------

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[dst],
        node_color="red",
        node_size=500,
        ax=ax
    )

    # -------------------------
    # Packet movement
    # -------------------------

    if p and len(p) > 1:

        # Create edges of the route
        edges = [
            (p[i], p[i + 1])
            for i in range(len(p) - 1)
        ]

        # Select current edge
        edge_index = (f // 20) % len(edges)

        # Position of packet
        t = (f % 20) / 20

        a, b = edges[edge_index]

        pa = pos[a]
        pb = pos[b]

        # Interpolate packet position
        x = pa[0] * (1 - t) + pb[0] * t
        y = pa[1] * (1 - t) + pb[1] * t

        # Draw packet
        ax.plot(
            x,
            y,
            'o',
            color='blue',
            markersize=10
        )

    # Display source/destination information
    ax.set_title(
        f"MANET Packet Animation | "
        f"Source: Node {src} → Destination: Node {dst}"
    )


# -----------------------------
# Start animation
# -----------------------------

ani = FuncAnimation(
    fig,
    animate,
    frames=400,
    interval=100
)

plt.show()