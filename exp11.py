
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
from matplotlib.animation import FuncAnimation

# Configuration
N = 8
R = 0.3
speed = 0.005

src, dst = random.sample(range(N), 2)

# Initialize positions and velocities
pos = {i: np.random.rand(2) for i in range(N)}
vel = {
    i: np.random.uniform(-1, 1, 2) * speed
    for i in range(N)
}

# Update node positions
def update_pos():
    for i in range(N):
        pos[i] += vel[i]

        for d in range(2):
            if pos[i][d] < 0 or pos[i][d] > 1:
                vel[i][d] *= -1
                pos[i][d] = np.clip(pos[i][d], 0, 1)

# Create network graph
def graph():
    G = nx.Graph()

    for i in range(N):
        for j in range(i + 1, N):
            if np.linalg.norm(pos[i] - pos[j]) <= R:
                G.add_edge(i, j)

    return G

# Find route using BFS
def path(G):
    from collections import deque

    q = deque([src])
    p = {src: None}

    while q:
        n = q.popleft()

        for nb in G[n]:
            if nb not in p:
                p[nb] = n
                q.append(nb)

                if nb == dst:
                    r = [dst]

                    while r[-1] != src:
                        r.append(p[r[-1]])

                    return r[::-1]

    return []

# Initialize visualization
fig, ax = plt.subplots(figsize=(7, 6))

# Animation function
def animate(f):
    update_pos()
    G = graph()
    p = path(G)

    ax.clear()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(
        f"Mobile Ad-hoc Network | Source: {src} | Destination: {dst}"
    )
    ax.axis("off")

    # Draw network nodes and links
    nx.draw(
        G, pos,
        node_color="skyblue",
        with_labels=True,
        node_size=600,
        ax=ax
    )

    # Highlight source and destination
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[src],
        node_color="green",
        node_size=700,
        ax=ax
    )

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[dst],
        node_color="red",
        node_size=700,
        ax=ax
    )

    # Animate packet along discovered route
    if p and len(p) > 1:
        e = [
            (p[i], p[i + 1])
            for i in range(len(p) - 1)
        ]

        i = (f // 20) % len(e)
        t = (f % 20) / 20

        a, b = e[i]
        pa, pb = pos[a], pos[b]

        x = pa[0] * (1 - t) + pb[0] * t
        y = pa[1] * (1 - t) + pb[1] * t

        ax.plot(
            x, y,
            'o',
            color="blue",
            markersize=12
        )

    elif f % 20 == 0:
        print("No route found between source and destination.")

# Start animation
ani = FuncAnimation(
    fig,
    animate,
    frames=400,
    interval=100,
    repeat=True
)

plt.tight_layout()
plt.show()
